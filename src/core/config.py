"""
Configuration management for ScrapeForge
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration class for scraping settings"""
    
    # Request settings
    DEFAULT_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_BACKOFF: float = float(os.getenv("RETRY_BACKOFF", "1.0"))
    
    # Proxy settings
    USE_PROXY: bool = os.getenv("USE_PROXY", "false").lower() == "true"
    PROXY_LIST_FILE: Optional[str] = os.getenv("PROXY_LIST_FILE")
    
    # User agent rotation
    ROTATE_USER_AGENT: bool = os.getenv("ROTATE_USER_AGENT", "true").lower() == "true"
    
    # Playwright settings
    PLAYWRIGHT_HEADLESS: bool = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
    PLAYWRIGHT_TIMEOUT: int = int(os.getenv("PLAYWRIGHT_TIMEOUT", "30000"))
    
    # Output settings
    OUTPUT_DIR: Path = Path(os.getenv("OUTPUT_DIR", "output"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    @classmethod
    def get_proxy_list(cls) -> list[str]:
        """Load proxy list from file if configured"""
        if not cls.PROXY_LIST_FILE or not os.path.exists(cls.PROXY_LIST_FILE):
            return []
        
        with open(cls.PROXY_LIST_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    
    @classmethod
    def ensure_output_dir(cls) -> Path:
        """Ensure output directory exists"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        return cls.OUTPUT_DIR

