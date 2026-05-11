"""Flask application for the web dashboard."""

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import threading
import uuid
import shutil
import subprocess
import sys

from src.web_ui.forms import ScanForm
from src.web_ui.api.routes import api_blueprint
from src.utils.logger import get_logger
from src.orchestrator.agent import Agent
from src.utils.config import Config
from src.dynamic_tester.downloader import download_website

logger = get_logger(__name__)


def create_app(config_path=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = Path('./data/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

    # Ensure upload folder exists
    app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Load agent configuration
    app.config['AGENT_CONFIG'] = Config(config_path)
    app.config['SCAN_DATA_DIR'] = Path('./data/scans')
    app.config['SCAN_DATA_DIR'].mkdir(parents=True, exist_ok=True)

    @app.route('/')
    def index():
        form = ScanForm()
        return render_template('index.html', form=form)

    @app.route('/scan', methods=['POST'])
    def scan():
        form = ScanForm()
        if not form.validate_on_submit():
            flash('Invalid input', 'error')
            return redirect(url_for('index'))

        scan_id = str(uuid.uuid4())
        target = form.target.data.strip()
        dynamic = form.dynamic.data

        # Prepare target path
        # Download website to a temporary directory
        temp_dir = Path('./data/temp') / scan_id
        temp_dir.mkdir(parents=True, exist_ok=True)
        try:
            logger.info(f"Downloading website from {target} to {temp_dir}")
            download_website(target, temp_dir)
            target_path = temp_dir
        except Exception as e:
            logger.error(f"Failed to download website: {e}")
            flash(f'Failed to download website: {e}', 'error')
            return redirect(url_for('index'))

        # Run scan in background thread
        def run_scan_task():
            try:
                # Use app context to access config
                with app.app_context():
                    config = app.config['AGENT_CONFIG']
                    agent = Agent(config)
                    
                    # Create scan directory before starting
                    scan_dir = app.config['SCAN_DATA_DIR'] / scan_id
                    scan_dir.mkdir(parents=True, exist_ok=True)
                    
                    summary = agent.run_scan(
                        target_path=target_path,
                        output_dir=scan_dir,
                        dynamic=dynamic,
                        original_target=target
                    )
                    
                    # Save summary to file
                    with open(scan_dir / 'summary.json', 'w') as f:
                        import json
                        json.dump(summary, f, indent=2, default=str)
            except Exception as e:
                logger.exception(f"Scan {scan_id} failed: {e}")

        thread = threading.Thread(target=run_scan_task)
        thread.start()
        
        # Brief delay to allow thread initialization
        import time
        time.sleep(0.5)

        return redirect(url_for('results', scan_id=scan_id))

    @app.route('/results/<scan_id>')
    def results(scan_id):
        scan_dir = app.config['SCAN_DATA_DIR'] / scan_id
        summary_file = scan_dir / 'summary.json'
        status_file = scan_dir / 'status.json'
        
        if not summary_file.exists():
            # Check for live status telemetry
            current_status = {"phase": "Initializing", "progress": 0, "message": "Starting engine..."}
            if status_file.exists():
                try:
                    with open(status_file, 'r') as f:
                        import json
                        current_status = json.load(f)
                except: pass
            
            return render_template('scan.html', 
                                 scan_id=scan_id, 
                                 status='pending', 
                                 refresh=True,
                                 live_status=current_status)
        
        with open(summary_file, 'r') as f:
            import json
            summary = json.load(f)
            
        return render_template('scan.html', 
                             scan_id=scan_id, 
                             status='complete', 
                             summary=summary,
                             report_path=summary.get('reports', {}).get('html'))

    @app.route('/download/<scan_id>/<fmt>')
    def download_report(scan_id, fmt):
        import json as _json
        from flask import send_from_directory, abort

        fmt_key = "pdf" if fmt == "pdf" else "sarif"
        filename = "report.pdf" if fmt == "pdf" else "report.sarif.json"

        # 1. Try reading exact path from summary.json
        summary_file = app.config['SCAN_DATA_DIR'] / scan_id / 'summary.json'
        if summary_file.exists():
            try:
                with open(summary_file) as f:
                    summary = _json.load(f)
                report_path = summary.get('reports', {}).get(fmt_key)
                if report_path:
                    p = Path(report_path)
                    if p.exists():
                        return send_from_directory(str(p.parent.resolve()), p.name, as_attachment=True)
            except Exception:
                pass

        # 2. Fallback: search data/scans/<scan_id>/ tree
        scan_dir = app.config['SCAN_DATA_DIR'] / scan_id
        matches = list(scan_dir.glob(f'**/{filename}'))
        if matches:
            best = max(matches, key=lambda p: p.stat().st_mtime)
            return send_from_directory(str(best.parent.resolve()), best.name, as_attachment=True)

        # 3. Fallback: search reports/ directory for any scan folder
        reports_root = Path('./reports')
        if reports_root.exists():
            matches = list(reports_root.glob(f'**/{filename}'))
            if matches:
                best = max(matches, key=lambda p: p.stat().st_mtime)
                return send_from_directory(str(best.parent.resolve()), best.name, as_attachment=True)

        flash(f"{fmt.upper()} report not found. Ensure the scan has completed.", "error")
        return redirect(url_for('results', scan_id=scan_id))

    return app