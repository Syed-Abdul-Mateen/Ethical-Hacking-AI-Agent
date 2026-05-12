import os
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import socketio
from backend.database.models import init_db, AsyncSessionLocal, ScanJob, FindingModel, UserModel
from backend.engine.agent import AsyncAgent
from src.utils.logger import get_logger
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, status
import jwt
from datetime import timedelta
from passlib.context import CryptContext

logger = get_logger(__name__)

# ─── Authentication Setup ───────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_enterprise_key_change_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserModel).where(UserModel.username == username))
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user


# Initialize FastAPI
app = FastAPI(title="Ethical Hacking AI Agent - API v2.0")

# Setup Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Global agent instance
agent = AsyncAgent(sio)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database initialized and ready.")

# ─── Socket.IO Events ───────────────────────────────────────────────────────

@sio.event
async def connect(sid, environ):
    logger.info(f"WebSocket client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"WebSocket client disconnected: {sid}")

# ─── Authentication Routes ──────────────────────────────────────────────────

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(UserModel).where(UserModel.username == form_data.username))
        user = result.scalar_one_or_none()
        if not user or not pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

# ─── Scan Routes ────────────────────────────────────────────────────────────

@app.post("/scan/start")
async def start_scan(target_url: str, background_tasks: BackgroundTasks, current_user: UserModel = Depends(get_current_user)):
    """Start a new async security scan."""
    scan_id = str(uuid.uuid4())

    # Persist initial scan record to DB
    async with AsyncSessionLocal() as session:
        new_scan = ScanJob(
            id=scan_id,
            target_url=target_url,
            status="pending",
            progress=0
        )
        session.add(new_scan)
        await session.commit()

    # Trigger the async scan engine in the background
    background_tasks.add_task(agent.run_scan_async, scan_id, target_url)

    return {"scan_id": scan_id, "status": "started", "message": "Scan initiated successfully."}

@app.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str, current_user: UserModel = Depends(get_current_user)):
    """Get full status and findings for a scan."""
    async with AsyncSessionLocal() as session:
        scan = await session.get(ScanJob, scan_id)
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")

        # Load associated findings
        result = await session.execute(
            select(FindingModel).where(FindingModel.scan_id == scan_id)
        )
        findings = result.scalars().all()

        return {
            "id": scan.id,
            "target_url": scan.target_url,
            "status": scan.status,
            "progress": scan.progress,
            "created_at": scan.created_at.isoformat() if scan.created_at else None,
            "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
            "metrics": {
                "total_endpoints": scan.total_endpoints,
                "total_forms": scan.total_forms,
                "critical_findings": scan.critical_findings,
                "high_findings": scan.high_findings,
            },
            "findings": [
                {
                    "id": f.id,
                    "title": f.title,
                    "severity": f.severity,
                    "description": f.description,
                    "endpoint": f.endpoint,
                    "payload": f.payload,
                    "remediation": f.remediation,
                }
                for f in findings
            ]
        }

@app.get("/scans/history")
async def get_scan_history(current_user: UserModel = Depends(get_current_user)):
    """Get all past scans for the history panel."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ScanJob).order_by(ScanJob.created_at.desc()).limit(10)
        )
        scans = result.scalars().all()
        return [
            {
                "id": s.id,
                "target_url": s.target_url,
                "status": s.status,
                "critical_findings": s.critical_findings,
                "high_findings": s.high_findings,
                "created_at": s.created_at.isoformat() if s.created_at else None,
            }
            for s in scans
        ]

@app.get("/scan/{scan_id}/report/pdf")
async def download_pdf_report(scan_id: str, current_user: UserModel = Depends(get_current_user)):
    """Download the PDF security report for a scan."""
    # Reports are saved under data/scans/<scan_id>/
    report_path = Path(f"./data/scans/{scan_id}/report.pdf")
    if not report_path.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF report not yet generated. Ensure scan has completed."
        )
    return FileResponse(
        path=str(report_path),
        media_type="application/pdf",
        filename=f"security_report_{scan_id[:8]}.pdf"
    )

@app.get("/scan/{scan_id}/report/sarif")
async def download_sarif_report(scan_id: str, current_user: UserModel = Depends(get_current_user)):
    """Download the SARIF report for CI/CD integration."""
    report_path = Path(f"./data/scans/{scan_id}/report.sarif.json")
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="SARIF report not found.")
    return FileResponse(
        path=str(report_path),
        media_type="application/json",
        filename=f"security_{scan_id[:8]}.sarif.json"
    )

# ─── Helper ─────────────────────────────────────────────────────────────────

async def emit_log(scan_id: str, message: str, level: str = "INFO"):
    """Broadcast a log event via WebSocket."""
    await sio.emit('scan_log', {
        'scan_id': scan_id,
        'message': message,
        'level': level,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
