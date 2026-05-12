from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass

class ScanJob(Base):
    __tablename__ = "scan_jobs"
    
    id: Mapped[str] = mapped_column(String, primary_key=True) # UUID
    target_url: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending") # pending, running, completed, failed
    progress: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Summary Metrics
    total_endpoints: Mapped[int] = mapped_column(Integer, default=0)
    total_forms: Mapped[int] = mapped_column(Integer, default=0)
    critical_findings: Mapped[int] = mapped_column(Integer, default=0)
    high_findings: Mapped[int] = mapped_column(Integer, default=0)
    
    findings: Mapped[List["FindingModel"]] = relationship(back_populates="scan", cascade="all, delete-orphan")

class FindingModel(Base):
    __tablename__ = "findings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scan_id: Mapped[str] = mapped_column(ForeignKey("scan_jobs.id"))
    
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String) # critical, high, medium, low
    endpoint: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    payload: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # AI generated content
    business_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    remediation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    scan: Mapped["ScanJob"] = relationship(back_populates="findings")

import os

# Dynamic Database Configuration
# Fallback to local SQLite if no DATABASE_URL is provided in .env
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///backend/database/ai_hacker.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
