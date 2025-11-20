"""
Playwright client for JavaScript-rendered pages
"""

from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

from src.core.config import Config
from src.core.logger import setup_logger


class PlaywrightClient:
    """
    Playwright-based client for scraping JavaScript-rendered content
    """
    
    def __init__(
        self,
        headless: bool = Config.PLAYWRIGHT_HEADLESS,
        timeout: int = Config.PLAYWRIGHT_TIMEOUT
    ):
        """
        Initialize Playwright client
        
        Args:
            headless: Whether to run browser in headless mode
            timeout: Page load timeout in milliseconds
        """
        self.headless = headless
        self.timeout = timeout
        self.logger = setup_logger(__name__)
        
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def start(self):
        """Start the browser"""
        self.logger.info("Starting Playwright browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.set_default_timeout(self.timeout)
    
    def goto(
        self,
        url: str,
        wait_until: str = "networkidle",
        timeout: Optional[int] = None
    ) -> str:
        """
        Navigate to a URL and return the page content
        
        Args:
            url: Target URL
            wait_until: When to consider navigation succeeded
                       (load, domcontentloaded, networkidle)
            timeout: Optional custom timeout in milliseconds
        
        Returns:
            Page HTML content
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.info(f"Navigating to: {url}")
        
        try:
            self.page.goto(url, wait_until=wait_until, timeout=timeout or self.timeout)
            self.logger.info(f"Successfully loaded: {url}")
            return self.page.content()
        
        except PlaywrightTimeout as e:
            self.logger.error(f"Timeout loading {url}: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading {url}: {str(e)}")
            raise
    
    def wait_for_selector(
        self,
        selector: str,
        timeout: Optional[int] = None,
        state: str = "visible"
    ):
        """
        Wait for a selector to appear
        
        Args:
            selector: CSS selector
            timeout: Optional timeout in milliseconds
            state: Element state to wait for (attached, detached, visible, hidden)
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.debug(f"Waiting for selector: {selector}")
        self.page.wait_for_selector(
            selector,
            timeout=timeout or self.timeout,
            state=state
        )
    
    def click(self, selector: str, timeout: Optional[int] = None):
        """
        Click an element
        
        Args:
            selector: CSS selector
            timeout: Optional timeout in milliseconds
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.debug(f"Clicking: {selector}")
        self.page.click(selector, timeout=timeout or self.timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None):
        """
        Fill an input field
        
        Args:
            selector: CSS selector
            value: Value to fill
            timeout: Optional timeout in milliseconds
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.debug(f"Filling {selector} with: {value}")
        self.page.fill(selector, value, timeout=timeout or self.timeout)
    
    def screenshot(self, path: str, full_page: bool = False):
        """
        Take a screenshot
        
        Args:
            path: File path to save screenshot
            full_page: Whether to capture full scrollable page
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        self.logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path, full_page=full_page)
    
    def evaluate(self, script: str) -> Any:
        """
        Execute JavaScript in the page context
        
        Args:
            script: JavaScript code to execute
        
        Returns:
            Result of the script execution
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        return self.page.evaluate(script)
    
    def get_content(self) -> str:
        """
        Get current page HTML content
        
        Returns:
            Page HTML
        """
        if not self.page:
            raise RuntimeError("Browser not started. Call start() first.")
        
        return self.page.content()
    
    def close(self):
        """Close the browser and cleanup"""
        if self.browser:
            self.logger.info("Closing Playwright browser...")
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

