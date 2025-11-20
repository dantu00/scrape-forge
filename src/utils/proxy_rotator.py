"""
Proxy rotation utility
"""

import random
from typing import List, Optional

from src.core.config import Config
from src.core.logger import setup_logger


class ProxyRotator:
    """
    Rotates through a list of proxy servers
    """
    
    def __init__(self, proxy_list: Optional[List[str]] = None):
        """
        Initialize the proxy rotator
        
        Args:
            proxy_list: Optional list of proxy URLs (format: http://host:port or http://user:pass@host:port)
                       If not provided, will attempt to load from config
        """
        self.logger = setup_logger(__name__)
        
        if proxy_list:
            self.proxies = proxy_list
        else:
            self.proxies = Config.get_proxy_list()
        
        if not self.proxies:
            self.logger.warning("No proxies configured. Proxy rotation will be disabled.")
    
    def get_random(self) -> Optional[str]:
        """
        Get a random proxy from the pool
        
        Returns:
            Random proxy URL or None if no proxies available
        """
        if not self.proxies:
            return None
        
        return random.choice(self.proxies)
    
    def add_proxy(self, proxy: str):
        """
        Add a proxy to the pool
        
        Args:
            proxy: Proxy URL to add
        """
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            self.logger.info(f"Added proxy: {proxy}")
    
    def remove_proxy(self, proxy: str):
        """
        Remove a proxy from the pool
        
        Args:
            proxy: Proxy URL to remove
        """
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self.logger.info(f"Removed proxy: {proxy}")
    
    def get_all(self) -> List[str]:
        """
        Get all proxies in the pool
        
        Returns:
            List of all proxy URLs
        """
        return self.proxies.copy()
    
    def count(self) -> int:
        """
        Get the number of proxies in the pool
        
        Returns:
            Number of proxies
        """
        return len(self.proxies)

