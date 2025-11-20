"""
ScrapeForge - A production-ready web scraping toolkit
"""

__version__ = "1.0.0"
__author__ = "ScrapeForge Contributors"

from src.core.base_scraper import BaseScraper
from src.core.html_parser import HTMLParser
from src.core.request_client import RequestClient
from src.core.playwright_client import PlaywrightClient
from src.core.logger import setup_logger

__all__ = [
    "BaseScraper",
    "HTMLParser",
    "RequestClient",
    "PlaywrightClient",
    "setup_logger",
]

