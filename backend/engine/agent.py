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

            # Phase 2: Analysis & Parsing
            await self.emit_status(scan_id, "Analysis", 30, "Parsing files and extracting AST...")
            await self.emit_log(scan_id, "Classifying files and extracting abstract syntax trees...")
            
            def parse_files():
                parsed = {}
                for f in all_files:
                    parser = self.file_classifier.get_parser(f)
                    if parser:
                        try:
                            res = parser.parse(f)
                            if res: parsed[f] = res
                        except: pass
                return parsed
                
            parsed_data = await loop.run_in_executor(None, parse_files)
            await self.emit_log(scan_id, f"Successfully parsed {len(parsed_data)} files.")
            
            # Phase 3: Vulnerability Testing (Core Logic)
            await self.emit_status(scan_id, "Vulnerability Testing", 50, "Executing detector modules...")
            
            detectors_to_run = self.registry.get_enabled()
            if not detectors_to_run:
                context = ScanContext(target_path=temp_dir, config=self.config)
                detectors_to_run = self.planner.plan(context)
                
            await self.emit_log(scan_id, f"Loaded {len(detectors_to_run)} active detector modules.")
            
            def run_detectors():
                findings = []
                context = ScanContext(target_path=temp_dir, config=self.config)
                for cls in detectors_to_run:
                    try:
                        det = cls(self.config, context)
                        findings.extend(det.run(parsed_data))
                    except: pass
                return findings
                
            all_findings = await loop.run_in_executor(None, run_detectors)
            
            # Phase 4: Intelligence & Deduplication
            await self.emit_status(scan_id, "Intelligence", 80, "Correlating findings and calculating CVSS...")
            unique_findings = self.deduplicator.deduplicate(all_findings)
            
            async with AsyncSessionLocal() as session:
                for f in unique_findings:
                    f.cvss_score = self.cvss_calculator.calculate(f)
                    try:
                        self.ai_analyzer.analyze_finding(f)
                    except: pass
                    
                    # Store in Database
                    db_finding = FindingModel(
                        scan_id=scan_id,
                        rule_id=f.rule_id,
                        title=f.title,
                        severity=f.severity,
                        description=f.description,
                        file_path=str(f.file_path),
                        line_number=f.line_number,
                        match=f.match_content if hasattr(f, 'match_content') else str(f.match),
                        remediation=f.remediation
                    )
                    session.add(db_finding)
                    await self.emit_log(scan_id, f"Found {f.severity} vulnerability: {f.title}", "ERROR" if f.severity.upper() in ["HIGH", "CRITICAL"] else "WARNING")
                
                await session.commit()
            
            # Phase 5: Reporting
            await self.emit_status(scan_id, "Reporting", 95, "Generating enterprise security reports...")
            
            context = ScanContext(target_path=temp_dir, config=self.config, output_dir=Path('./data/scans') / scan_id)
            context.findings = unique_findings
            context.output_dir.mkdir(parents=True, exist_ok=True)
            report_paths = self.report_generator.generate(context)
            await self.emit_log(scan_id, f"Generated {len(report_paths)} reports in {context.output_dir}.")
            
            # Finalize ScanJob DB Record
            async with AsyncSessionLocal() as session:
                scan = await session.get(ScanJob, scan_id)
                if scan:
                    scan.status = "completed"
                    scan.progress = 100
                    scan.total_findings = len(unique_findings)
                    scan.critical_findings = sum(1 for f in unique_findings if f.severity.upper() == 'CRITICAL')
                    scan.high_findings = sum(1 for f in unique_findings if f.severity.upper() == 'HIGH')
                    scan.medium_findings = sum(1 for f in unique_findings if f.severity.upper() == 'MEDIUM')
                    scan.low_findings = sum(1 for f in unique_findings if f.severity.upper() == 'LOW')
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
