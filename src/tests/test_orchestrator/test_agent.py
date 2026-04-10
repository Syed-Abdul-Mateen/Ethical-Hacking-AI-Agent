"""
Unit tests for Agent.
"""

import pytest
from src.orchestrator.agent import Agent
from src.orchestrator.context import ScanContext


def test_agent_initialization():
    agent = Agent()
    assert agent.config is not None
    assert agent.context is None