"""REST API endpoints for the Ethical Hacking AI Agent."""

import json
import uuid
import threading
from pathlib import Path
from typing import Dict, Any

from flask import Blueprint, jsonify, request

from src.utils.logger import get_logger
from src.utils.config import Config

logger = get_logger(__name__)

api_blueprint = Blueprint('api', __name__)

# In-memory scan tracking (for enterprise use, replace with Redis/DB)
_scan_store: Dict[str, Dict[str, Any]] = {}
_scan_lock = threading.Lock()


def _get_config() -> Config:
    """Lazy-load config to avoid import-time errors."""
    return Config()


@api_blueprint.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "ethical-hacking-ai-agent",
        "version": "0.1.0",
    }), 200


@api_blueprint.route('/scan', methods=['POST'])
def start_scan():
    """
    Start a new security scan.

    Request body (JSON):
        - target (str): Path to local directory to scan.
        - dynamic (bool, optional): Enable dynamic testing. Default: false.
        - output_dir (str, optional): Custom output directory.

    Returns:
        JSON with scan_id and status.
    """
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Missing 'target' in request body."}), 400

    target = data['target']
    target_path = Path(target).resolve()

    if not target_path.is_dir():
        return jsonify({"error": f"Target directory does not exist: {target}"}), 400

    scan_id = str(uuid.uuid4())
    dynamic = data.get('dynamic', False)
    output_dir = data.get('output_dir')

    # Initialize scan record
    with _scan_lock:
        _scan_store[scan_id] = {
            "scan_id": scan_id,
            "status": "running",
            "target": str(target_path),
            "dynamic": dynamic,
            "summary": None,
            "error": None,
        }

    # Run scan in background thread
    def _run_scan():
        try:
            from src.orchestrator.agent import Agent

            config = _get_config()
            if dynamic:
                config._config.setdefault("dynamic", {})["enabled"] = True

            agent = Agent(config)
            out_dir = Path(output_dir) if output_dir else Path('./reports') / scan_id

            summary = agent.run_scan(
                target_path=target_path,
                output_dir=out_dir,
                dynamic=dynamic,
            )

            # Convert Path objects for JSON serialization
            serializable_summary = {}
            for k, v in summary.items():
                if isinstance(v, dict):
                    serializable_summary[k] = {
                        sk: str(sv) if isinstance(sv, Path) else sv
                        for sk, sv in v.items()
                    }
                elif isinstance(v, Path):
                    serializable_summary[k] = str(v)
                else:
                    serializable_summary[k] = v

            with _scan_lock:
                _scan_store[scan_id]["status"] = "completed"
                _scan_store[scan_id]["summary"] = serializable_summary

        except Exception as e:
            logger.exception(f"API scan {scan_id} failed: {e}")
            with _scan_lock:
                _scan_store[scan_id]["status"] = "failed"
                _scan_store[scan_id]["error"] = str(e)

    thread = threading.Thread(target=_run_scan, daemon=True)
    thread.start()

    return jsonify({
        "scan_id": scan_id,
        "status": "running",
        "message": "Scan started successfully.",
    }), 202


@api_blueprint.route('/scan/<scan_id>', methods=['GET'])
def get_scan_status(scan_id: str):
    """
    Get the status of a running or completed scan.

    Returns:
        JSON with scan status and summary (if complete).
    """
    with _scan_lock:
        scan = _scan_store.get(scan_id)

    if not scan:
        return jsonify({"error": f"Scan '{scan_id}' not found."}), 404

    return jsonify(scan), 200


@api_blueprint.route('/scan/<scan_id>/report', methods=['GET'])
def get_scan_report(scan_id: str):
    """
    Get the JSON report for a completed scan.

    Returns:
        JSON report data or error.
    """
    with _scan_lock:
        scan = _scan_store.get(scan_id)

    if not scan:
        return jsonify({"error": f"Scan '{scan_id}' not found."}), 404

    if scan["status"] != "completed":
        return jsonify({
            "error": "Scan is not yet completed.",
            "status": scan["status"],
        }), 409

    summary = scan.get("summary", {})
    reports = summary.get("reports", {})
    json_report_path = reports.get("json")

    if json_report_path and Path(json_report_path).exists():
        with open(json_report_path, "r") as f:
            report_data = json.load(f)
        return jsonify(report_data), 200
    else:
        return jsonify({"message": "JSON report not found.", "summary": summary}), 200


@api_blueprint.route('/scans', methods=['GET'])
def list_scans():
    """
    List all tracked scans.

    Returns:
        JSON array of scan summaries.
    """
    with _scan_lock:
        scans = [
            {
                "scan_id": s["scan_id"],
                "status": s["status"],
                "target": s["target"],
            }
            for s in _scan_store.values()
        ]

    return jsonify({"scans": scans, "total": len(scans)}), 200