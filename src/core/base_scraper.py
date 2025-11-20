"""
Base scraper class to be extended by specific scrapers
"""

import json
import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.core.request_client import RequestClient
from src.core.playwright_client import PlaywrightClient
from src.core.html_parser import HTMLParser
from src.core.config import Config
from src.core.logger import setup_logger


class BaseScraper(ABC):
    """
    Abstract base class for all scrapers
    
    Subclasses must implement the scrape() method
    """
    
    def __init__(
        self,
        use_playwright: bool = False,
        **kwargs
    ):
        """
        Initialize the base scraper
        
        Args:
            use_playwright: Whether to use Playwright instead of requests
            **kwargs: Additional arguments passed to RequestClient or PlaywrightClient
        """
        self.logger = setup_logger(self.__class__.__name__)
        self.use_playwright = use_playwright
        
        # Initialize appropriate client
        if use_playwright:
            self.playwright_client = PlaywrightClient(**kwargs)
            self.request_client = None
        else:
            self.request_client = RequestClient(**kwargs)
            self.playwright_client = None
        
        self.data: List[Dict[str, Any]] = []
    
    @abstractmethod
    def scrape(self, url: str) -> List[Dict[str, Any]]:
        """
        Main scraping method to be implemented by subclasses
        
        Args:
            url: URL to scrape
        
        Returns:
            List of scraped data dictionaries
        """
        pass
    
    def fetch_html(self, url: str) -> str:
        """
        Fetch HTML content from URL
        
        Args:
            url: Target URL
        
        Returns:
            HTML content as string
        """
        if self.use_playwright:
            if not self.playwright_client.browser:
                self.playwright_client.start()
            return self.playwright_client.goto(url)
        else:
            response = self.request_client.get(url)
            return response.text
    
    def parse_html(self, html: str) -> HTMLParser:
        """
        Parse HTML content
        
        Args:
            html: HTML string
        
        Returns:
            HTMLParser instance
        """
        return HTMLParser(html)
    
    def save_json(
        self,
        data: List[Dict[str, Any]],
        filename: str,
        indent: int = 2
    ) -> Path:
        """
        Save data as JSON file
        
        Args:
            data: Data to save
            filename: Output filename
            indent: JSON indentation
        
        Returns:
            Path to saved file
        """
        output_dir = Config.ensure_output_dir()
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        self.logger.info(f"Saved JSON to: {filepath}")
        return filepath
    
    def save_csv(
        self,
        data: List[Dict[str, Any]],
        filename: str
    ) -> Path:
        """
        Save data as CSV file
        
        Args:
            data: Data to save
            filename: Output filename
        
        Returns:
            Path to saved file
        """
        if not data:
            self.logger.warning("No data to save")
            return None
        
        output_dir = Config.ensure_output_dir()
        filepath = output_dir / filename
        
        # Get all unique keys from all dictionaries
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        self.logger.info(f"Saved CSV to: {filepath}")
        return filepath
    
    def run(self, url: str, save_format: Optional[str] = None, output_filename: Optional[str] = None):
        """
        Run the scraper and optionally save results
        
        Args:
            url: URL to scrape
            save_format: Output format ('json' or 'csv')
            output_filename: Custom output filename
        """
        self.logger.info(f"Starting scrape: {url}")
        
        try:
            self.data = self.scrape(url)
            self.logger.info(f"Scraped {len(self.data)} items")
            
            if save_format and output_filename:
                if save_format.lower() == 'json':
                    self.save_json(self.data, output_filename)
                elif save_format.lower() == 'csv':
                    self.save_csv(self.data, output_filename)
            
            return self.data
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.request_client:
            self.request_client.close()
        if self.playwright_client:
            self.playwright_client.close()

