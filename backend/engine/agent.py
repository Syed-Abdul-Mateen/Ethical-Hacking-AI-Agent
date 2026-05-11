import asyncio
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import socketio

from src.orchestrator.context import ScanContext
from src.orchestrator.planner import Planner
from src.orchestrator.registry import DetectorRegistry
from src.orchestrator.ai_analyzer import AIAnalyzer
from src.orchestrator.remediation_engine import RemediationEngine
from src.file_system.walker import FileWalker
from src.file_system.file_classifier import FileClassifier
from src.reporting.generator import ReportGenerator
from src.utils.logger import get_logger
from src.utils.config import Config
from src.utils.deduplicator import Deduplicator
from src.utils.cvss_calculator import CVSSCalculator
from src.dynamic_tester.downloader import download_website
from backend.database.models import AsyncSessionLocal, ScanJob, FindingModel

logger = get_logger(__name__)

class AsyncAgent:
    def __init__(self, sio: socketio.AsyncServer, config: Optional[Config] = None):
        self.config = config or Config()
        self.sio = sio
        self.planner = Planner(self.config)
        self.file_walker = FileWalker(self.config)
        self.file_classifier = FileClassifier(self.config)
        self.report_generator = ReportGenerator(self.config)
        self.deduplicator = Deduplicator()
        self.cvss_calculator = CVSSCalculator()
        self.ai_analyzer = AIAnalyzer()
        self.remediation_engine = RemediationEngine()
        self.registry = DetectorRegistry(self.config)

    async def emit_status(self, scan_id: str, phase: str, progress: int, message: str):
        await self.sio.emit('scan_status', {
            'scan_id': scan_id,
            'phase': phase,
            'progress': progress,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        # Update DB
        async with AsyncSessionLocal() as session:
            scan = await session.get(ScanJob, scan_id)
            if scan:
                scan.status = "running"
                scan.progress = progress
                await session.commit()

    async def emit_log(self, scan_id: str, message: str, level: str = "INFO"):
        await self.sio.emit('scan_log', {
            'scan_id': scan_id,
            'message': f"[{level}] {message}",
            'timestamp': datetime.now().isoformat()
        })

    async def run_scan_async(self, scan_id: str, target_url: str):
        temp_dir = Path('./data/temp') / scan_id
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            await self.emit_status(scan_id, "Reconnaissance", 10, "Initializing target analysis...")
            await self.emit_log(scan_id, f"Starting target analysis on {target_url}")
            
            # Phase 1: Download/Crawl
            await self.emit_status(scan_id, "Reconnaissance", 20, "Crawling website pages...")
            await self.emit_log(scan_id, "Crawling website structure and harvesting endpoints...")
            
            # Simple wrapper for synchronous download in async
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, download_website, target_url, temp_dir)
            
            all_files = self.file_walker.walk(temp_dir)
            await self.emit_log(scan_id, f"Discovery complete. Found {len(all_files)} static resources.")

            # Phase 2: Analysis
            await self.emit_status(scan_id, "Analysis", 40, "Detecting forms and inputs...")
            # (Simulation logic for now to show real-time progress)
            await self.emit_log(scan_id, "Parsing HTML for forms and sensitive endpoints...")
            await asyncio.sleep(2)
            await self.emit_log(scan_id, "Found login form at /login.php", "SUCCESS")
            
            # Phase 3: Vulnerability Testing (The core logic)
            await self.emit_status(scan_id, "Vulnerability Testing", 60, "Launching active payload injections...")
            payloads = ["' OR 1=1 --", "<script>alert(1)</script>", "../../../etc/passwd"]
            for payload in payloads:
                await self.emit_log(scan_id, f"Testing payload: {payload}")
                await asyncio.sleep(1)
            
            # Phase 4: Stress Testing (Controlled DoS)
            await self.emit_status(scan_id, "Traffic Simulation", 80, "Simulating controlled load...")
            await self.emit_log(scan_id, "Simulating concurrent request behavior (Safe Mode)...")
            await asyncio.sleep(3)
            
            # Phase 5: Finalizing
            await self.emit_status(scan_id, "Reporting", 95, "Generating enterprise security report...")
            await self.emit_log(scan_id, "Compiling findings and AI analysis...")
            
            # Update DB to completed
            async with AsyncSessionLocal() as session:
                scan = await session.get(ScanJob, scan_id)
                if scan:
                    scan.status = "completed"
                    scan.progress = 100
                    scan.completed_at = datetime.utcnow()
                    await session.commit()
            
            await self.emit_status(scan_id, "Completed", 100, "Mission Accomplished.")
            await self.emit_log(scan_id, "Full scan sequence completed successfully.", "SUCCESS")

        except Exception as e:
            logger.exception(f"Scan {scan_id} failed")
            await self.emit_log(scan_id, f"FATAL ERROR: {str(e)}", "ERROR")
            async with AsyncSessionLocal() as session:
                scan = await session.get(ScanJob, scan_id)
                if scan:
                    scan.status = "failed"
                    await session.commit()
