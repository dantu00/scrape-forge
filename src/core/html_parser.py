"""
HTML parsing utilities using BeautifulSoup4
"""

from typing import Optional, List, Dict, Any
from bs4 import BeautifulSoup, Tag
from src.core.logger import setup_logger


class HTMLParser:
    """
    HTML parser with convenient extraction methods
    """
    
    def __init__(self, html: str, parser: str = "html.parser"):
        """
        Initialize the HTML parser
        
        Args:
            html: HTML content as string
            parser: Parser to use (html.parser, lxml, html5lib)
        """
        self.soup = BeautifulSoup(html, parser)
        self.logger = setup_logger(__name__)
    
    def find(self, tag: str, **kwargs) -> Optional[Tag]:
        """
        Find the first occurrence of a tag
        
        Args:
            tag: Tag name
            **kwargs: Additional search criteria (class_, id, attrs, etc.)
        
        Returns:
            Tag object or None
        """
        return self.soup.find(tag, **kwargs)
    
    def find_all(self, tag: str, **kwargs) -> List[Tag]:
        """
        Find all occurrences of a tag
        
        Args:
            tag: Tag name
            **kwargs: Additional search criteria
        
        Returns:
            List of Tag objects
        """
        return self.soup.find_all(tag, **kwargs)
    
    def select(self, selector: str) -> List[Tag]:
        """
        Find elements using CSS selector
        
        Args:
            selector: CSS selector string
        
        Returns:
            List of Tag objects
        """
        return self.soup.select(selector)
    
    def select_one(self, selector: str) -> Optional[Tag]:
        """
        Find first element using CSS selector
        
        Args:
            selector: CSS selector string
        
        Returns:
            Tag object or None
        """
        return self.soup.select_one(selector)
    
    def get_text(self, tag: Optional[Tag] = None, strip: bool = True) -> str:
        """
        Extract text from tag or entire document
        
        Args:
            tag: Optional tag to extract text from (uses root if None)
            strip: Whether to strip whitespace
        
        Returns:
            Extracted text
        """
        element = tag if tag else self.soup
        return element.get_text(strip=strip)
    
    def get_attribute(self, tag: Tag, attr: str, default: Any = None) -> Any:
        """
        Get attribute value from a tag
        
        Args:
            tag: Tag object
            attr: Attribute name
            default: Default value if attribute not found
        
        Returns:
            Attribute value or default
        """
        return tag.get(attr, default)
    
    def extract_links(self, base_url: Optional[str] = None) -> List[str]:
        """
        Extract all links from the document
        
        Args:
            base_url: Optional base URL to resolve relative links
        
        Returns:
            List of URLs
        """
        links = []
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            if base_url and not href.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                href = urljoin(base_url, href)
            links.append(href)
        return links
    
    def extract_images(self, base_url: Optional[str] = None) -> List[str]:
        """
        Extract all image URLs from the document
        
        Args:
            base_url: Optional base URL to resolve relative URLs
        
        Returns:
            List of image URLs
        """
        images = []
        for img in self.soup.find_all('img', src=True):
            src = img['src']
            if base_url and not src.startswith(('http://', 'https://')):
                from urllib.parse import urljoin
                src = urljoin(base_url, src)
            images.append(src)
        return images
    
    def to_dict(self, tag: Tag) -> Dict[str, Any]:
        """
        Convert a tag to a dictionary representation
        
        Args:
            tag: Tag object
        
        Returns:
            Dictionary with tag name, attributes, and text
        """
        return {
            "tag": tag.name,
            "attributes": dict(tag.attrs),
            "text": self.get_text(tag)
        }

