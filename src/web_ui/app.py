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
# from src.dynamic_tester.downloader import download_website

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
    agent_config = Config(config_path)

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
        scan_type = form.scan_type.data
        target = form.target.data.strip()
        dynamic = form.dynamic.data

        # Prepare target path
        if scan_type == 'local':
            target_path = Path(target).resolve()
            if not target_path.is_dir():
                flash('Local folder does not exist', 'error')
                return redirect(url_for('index'))
        else:  # url
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

        # Run scan in background thread (or async task)
        def run_scan_task():
            try:
                agent = Agent(agent_config)
                summary = agent.run_scan(
                    target_path=target_path,
                    output_dir=Path('./data/scans') / scan_id,
                    dynamic=dynamic
                )
                # Save summary to file
                with open(Path('./data/scans') / scan_id / 'summary.json', 'w') as f:
                    import json
                    json.dump(summary, f, indent=2, default=str)
            except Exception as e:
                logger.exception(f"Scan {scan_id} failed: {e}")

        thread = threading.Thread(target=run_scan_task)
        thread.start()

        return redirect(url_for('results', scan_id=scan_id))

    @app.route('/results/<scan_id>')
    def results(scan_id):
        scan_dir = Path('./data/scans') / scan_id
        summary_file = scan_dir / 'summary.json'
        if not summary_file.exists():
            return render_template('scan.html', scan_id=scan_id, status='pending')
        import json
        with open(summary_file) as f:
            summary = json.load(f)
        # Check if report exists
        report_html = scan_dir / f"scan_{summary.get('timestamp', '')}" / 'report.html' if summary else None
        # Actually we need to find the latest report. Simpler: look for any report.html
        report_html = list(scan_dir.glob('*/report.html'))
        report_html = report_html[0] if report_html else None
        return render_template('scan.html', scan_id=scan_id, status='complete', summary=summary, report_path=report_html)

    return app