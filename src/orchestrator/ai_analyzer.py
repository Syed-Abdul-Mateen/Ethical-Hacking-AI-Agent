"""
AI-powered vulnerability analysis engine.
Integrates with LLMs to provide deep contextual analysis and remediation.
"""

import os
from typing import List, Dict, Any, Optional
from src.detectors.base_detector import Finding
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AIAnalyzer:
    """
    Analyzes findings using AI to provide:
    1. Vulnerability Explanation (Why is this a risk?)
    2. Exploit Scenario (How could an attacker use this?)
    3. Remediation Code (How to fix it exactly?)
    """

    def __init__(self, config_path: Optional[str] = None):
        self.enabled = True
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info("AI Analyzer initialized with OpenAI integration.")
            except ImportError:
                logger.warning("OpenAI SDK not installed. Falling back to mock AI logic.")
        else:
            logger.warning("OPENAI_API_KEY not found. Falling back to mock AI logic.")

    def analyze_finding(self, finding: Finding) -> Dict[str, Any]:
        """
        Perform deep analysis on a single finding.
        If OpenAI is configured, it will dynamically generate the patch.
        Otherwise, it falls back to the simulated mock responses.
        """
        if self.client:
            return self._analyze_with_llm(finding)
            
        analysis = {
            "explanation": self._get_ai_explanation(finding),
            "exploit_scenario": self._get_exploit_scenario(finding),
            "remediation_patch": self._generate_suggested_fix(finding),
            "ai_confidence": 0.85
        }
        finding.metadata["ai_analysis"] = analysis
        if not hasattr(finding, 'remediation') or not finding.remediation:
            finding.remediation = analysis["remediation_patch"]
        return analysis

    def _analyze_with_llm(self, finding: Finding) -> Dict[str, Any]:
        """Call the actual OpenAI API to analyze the vulnerability context."""
        try:
            match_context = finding.match_content if hasattr(finding, 'match_content') else str(getattr(finding, 'match', ''))
            
            prompt = f"""
            You are an elite application security engineer. Analyze this vulnerability finding.
            
            Vulnerability: {finding.title}
            Severity: {finding.severity}
            Description: {finding.description}
            Code Match: 
            ```
            {match_context}
            ```
            
            Provide a strict JSON response with no markdown formatting containing:
            {{
                "explanation": "Brief explanation of why this specific code is vulnerable",
                "exploit_scenario": "One sentence on how an attacker exploits this",
                "remediation_patch": "The exact code snippet to fix this issue securely",
                "ai_confidence": 0.95
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a specialized DevSecOps AI. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            finding.metadata["ai_analysis"] = result
            finding.remediation = result.get("remediation_patch", finding.remediation)
            return result
            
        except Exception as e:
            logger.error(f"LLM API Call failed: {e}")
            # Fallback
            analysis = {
                "explanation": self._get_ai_explanation(finding),
                "exploit_scenario": self._get_exploit_scenario(finding),
                "remediation_patch": self._generate_suggested_fix(finding),
                "ai_confidence": 0.50
            }
            finding.remediation = analysis["remediation_patch"]
            return analysis

    def _get_ai_explanation(self, finding: Finding) -> str:
        """Simulated AI explanation logic."""
        if "SQL Injection" in finding.title:
            return "The application concatenates user-controlled variables directly into an SQL string. This allows an attacker to manipulate the database query's structure, potentially bypassing authentication or leaking the entire database."
        if "Hardcoded" in finding.title:
            return "Sensitive credentials found in source code. If this code is leaked or accessed by unauthorized users, they can gain full access to the linked services."
        return f"AI Analysis: This {finding.title} vulnerability represents a significant security risk in the current code context."

    def _get_exploit_scenario(self, finding: Finding) -> str:
        """Simulated exploit scenario logic."""
        return "An attacker could supply a specially crafted input string to trigger this vulnerability and gain unauthorized access or execute arbitrary commands."

    def _generate_suggested_fix(self, finding: Finding) -> str:
        """Simulated remediation code generation."""
        if "SQL Injection" in finding.title:
            return "# FIX: Use Parameterized Queries\ncursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
        return "# FIX: Follow security best practices for this vulnerability type."
