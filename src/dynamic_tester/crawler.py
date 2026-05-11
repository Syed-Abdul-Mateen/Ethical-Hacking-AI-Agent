"""
Simple web crawler to discover links.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, List
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Crawler:
    """Crawl a website to discover internal URLs."""

    def __init__(self, base_url: str, max_pages: int = 100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited = set()
        self.pages = []

    def crawl(self) -> List[str]:
        """Start crawling from base URL."""
        self._crawl_page(self.base_url)
        return self.pages

    def _crawl_page(self, url: str):
        if len(self.visited) >= self.max_pages:
            return
        if url in self.visited:
            return
        self.visited.add(url)
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.pages.append(url)
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Discover links
                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    full_url = urljoin(url, href)
                    if self._is_internal(full_url):
                        self._crawl_page(full_url)
                
                # Discover form actions (crucial for dynamic testing)
                for form in soup.find_all("form", action=True):
                    action = form["action"]
                    full_url = urljoin(url, action)
                    if self._is_internal(full_url):
                        self._crawl_page(full_url)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Connection error while crawling {url}: {e}")
        except Exception as e:
            logger.debug(f"Unexpected error crawling {url}: {e}")

    def _is_internal(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        base_netloc = urlparse(self.base_url).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc == target_netloc