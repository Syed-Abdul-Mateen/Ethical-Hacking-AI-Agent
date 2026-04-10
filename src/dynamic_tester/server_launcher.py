"""
Launch local web server for dynamic testing.
"""

import subprocess
import socket
import time
from pathlib import Path
from typing import Optional, Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ServerLauncher:
    """Launch a local web server based on the target folder."""

    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.process = None
        self.base_url = None

    def detect_server_type(self) -> Optional[str]:
        """Detect which server type to use based on files."""
        if (self.root_path / "index.php").exists() or any(self.root_path.glob("*.php")):
            return "php"
        if (self.root_path / "app.py").exists() or (self.root_path / "wsgi.py").exists():
            return "python"
        if (self.root_path / "package.json").exists():
            return "node"
        # Default to Python's built-in server
        return "python"

    def start(self, port: int = 8080) -> Tuple[subprocess.Popen, str]:
        """Start the server and return process and base URL."""
        server_type = self.detect_server_type()
        base_url = f"http://localhost:{port}"
        if server_type == "php":
            # Use PHP built-in server
            cmd = ["php", "-S", f"localhost:{port}", "-t", str(self.root_path)]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif server_type == "python":
            # Use Python's http.server
            cmd = ["python", "-m", "http.server", str(port), "--directory", str(self.root_path)]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif server_type == "node":
            # Assume npm start or node app.js; we'll just try to run npm start
            # This is simplistic; in practice you'd need to detect the entry point
            cmd = ["npm", "start", "--prefix", str(self.root_path)]
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            logger.error("No supported server type detected.")
            return None, None

        # Wait for server to start
        time.sleep(2)
        # Check if server is running
        try:
            with socket.create_connection(("localhost", port), timeout=2):
                self.base_url = base_url
                logger.info(f"Server started at {base_url}")
        except Exception:
            logger.error("Server failed to start.")
            return None, None

        return self.process, self.base_url

    def stop(self):
        """Stop the server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            logger.info("Server stopped.")