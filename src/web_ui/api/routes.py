"""REST API endpoints for the agent."""

from flask import Blueprint, jsonify, request
from src.orchestrator.agent import Agent
from src.utils.config import Config

api_blueprint = Blueprint('api', __name__)
agent = Agent(Config())

@api_blueprint.route('/scan', methods=['POST'])
def start_scan():
    data = request.get_json()
    # Similar logic as in app.py, but return JSON
    # For simplicity, we just return a placeholder
    return jsonify({"message": "API scan not implemented yet"}), 501