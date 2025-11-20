"""
HTTP request client with retry logic and rotation support
"""

import time
import requests
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.core.config import Config
from src.core.logger import setup_logger
from src.utils.user_agent_rotator import UserAgentRotator
from src.utils.proxy_rotator import ProxyRotator


class RequestClient:
    """
    HTTP client with built-in retry logic, user-agent rotation, and proxy support
    """
    
    def __init__(
        self,
        timeout: int = Config.DEFAULT_TIMEOUT,
        max_retries: int = Config.MAX_RETRIES,
        use_proxy: bool = Config.USE_PROXY,
        rotate_user_agent: bool = Config.ROTATE_USER_AGENT
    ):
        """
        Initialize the request client
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            use_proxy: Whether to use proxy rotation
            rotate_user_agent: Whether to rotate user agents
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = setup_logger(__name__)
        
        # Initialize rotators
        self.ua_rotator = UserAgentRotator() if rotate_user_agent else None
        self.proxy_rotator = ProxyRotator() if use_proxy else None
        
        # Create session with retry strategy
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry configuration"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=Config.RETRY_BACKOFF,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Perform a GET request with rotation and retry logic
        
        Args:
            url: Target URL
            headers: Optional custom headers
            params: Optional query parameters
            **kwargs: Additional arguments passed to requests
        
        Returns:
            Response object
        """
        return self._request("GET", url, headers=headers, params=params, **kwargs)
    
    def post(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Perform a POST request with rotation and retry logic
        
        Args:
            url: Target URL
            headers: Optional custom headers
            data: Optional form data
            json: Optional JSON data
            **kwargs: Additional arguments passed to requests
        
        Returns:
            Response object
        """
        return self._request("POST", url, headers=headers, data=data, json=json, **kwargs)
    
    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Internal method to perform requests with rotation
        
        Args:
            method: HTTP method
            url: Target URL
            headers: Optional headers
            **kwargs: Additional request arguments
        
        Returns:
            Response object
        """
        # Prepare headers with user agent
        request_headers = headers or {}
        if self.ua_rotator and "User-Agent" not in request_headers:
            request_headers["User-Agent"] = self.ua_rotator.get_random()
        
        # Prepare proxy
        proxies = None
        if self.proxy_rotator:
            proxy = self.proxy_rotator.get_random()
            if proxy:
                proxies = {"http": proxy, "https": proxy}
                self.logger.debug(f"Using proxy: {proxy}")
        
        # Set timeout if not provided
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        
        self.logger.info(f"{method} request to: {url}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                proxies=proxies,
                **kwargs
            )
            response.raise_for_status()
            self.logger.info(f"Success: {url} (Status: {response.status_code})")
            return response
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {str(e)}")
            raise
    
    def close(self):
        """Close the session"""
        self.session.close()

