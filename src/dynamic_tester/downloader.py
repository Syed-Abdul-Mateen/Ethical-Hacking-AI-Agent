"""Download a website recursively for offline static analysis."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from src.utils.logger import get_logger

logger = get_logger(__name__)


def download_website(url: str, target_dir: Path, depth: int = 2) -> None:
    """
    Download a website using wget (or a Python alternative) to a local directory.

    Args:
        url: Website URL (e.g., https://example.com)
        target_dir: Directory to save the downloaded content.
        depth: Maximum recursion depth.

    Raises:
        Exception: If download fails.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    # Try wget first (common on Linux/macOS)
    wget_cmd = [
        'wget',
        '--recursive',
        '--level=' + str(depth),
        '--no-parent',
        '--page-requisites',
        '--convert-links',
        '--adjust-extension',
        '--no-check-certificate',
        '--directory-prefix=' + str(target_dir),
        '--input-file=/dev/null',
        url
    ]

    try:
        subprocess.run(wget_cmd, check=True, capture_output=True, timeout=120)
        logger.info(f"Downloaded website to {target_dir}")
        return
    except FileNotFoundError:
        logger.warning("wget not found. Trying alternative method.")
    except subprocess.CalledProcessError as e:
        logger.error(f"wget failed: {e.stderr}")
        raise Exception(f"wget failed: {e.stderr}")

    # Fallback: use Python requests and BeautifulSoup (simple implementation)
    try:
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin, urlparse

        visited = set()
        to_visit = [url]
        visited.add(url)

        while to_visit and len(visited) < 100:  # Limit for safety
            current_url = to_visit.pop(0)
            try:
                response = requests.get(current_url, timeout=10)
                if response.status_code != 200:
                    continue

                # Save the content
                parsed_url = urlparse(current_url)
                path = parsed_url.path
                if path == '' or path.endswith('/'):
                    path = path + 'index.html'
                file_path = target_dir / path.lstrip('/')
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                # Extract links
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute = urljoin(current_url, href)
                    if absolute.startswith(url) and absolute not in visited:
                        visited.add(absolute)
                        to_visit.append(absolute)
            except Exception as e:
                logger.warning(f"Error downloading {current_url}: {e}")

        logger.info(f"Downloaded {len(visited)} pages to {target_dir}")
    except ImportError:
        raise Exception("Neither wget nor requests/BeautifulSoup available. Install required packages.")