#!/usr/bin/env python3
"""
Example scraper for quotes.toscrape.com

This demonstrates:
- Extending BaseScraper
- Using RequestClient for HTTP requests
- Parsing HTML with HTMLParser
- Extracting structured data
- Saving results as JSON/CSV
"""

import sys
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import List, Dict, Any
from src.core.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    """
    Scraper for quotes.toscrape.com
    
    Extracts quotes, authors, and tags from the website
    """
    
    def scrape(self, url: str) -> List[Dict[str, Any]]:
        """
        Scrape quotes from the given URL
        
        Args:
            url: URL to scrape (e.g., https://quotes.toscrape.com/)
        
        Returns:
            List of quote dictionaries
        """
        quotes_data = []
        
        # Fetch and parse the HTML
        html = self.fetch_html(url)
        parser = self.parse_html(html)
        
        # Find all quote containers
        quote_divs = parser.find_all('div', class_='quote')
        
        self.logger.info(f"Found {len(quote_divs)} quotes on the page")
        
        for quote_div in quote_divs:
            try:
                # Extract quote text
                quote_text_elem = quote_div.find('span', class_='text')
                quote_text = parser.get_text(quote_text_elem) if quote_text_elem else ""
                
                # Extract author
                author_elem = quote_div.find('small', class_='author')
                author = parser.get_text(author_elem) if author_elem else ""
                
                # Extract tags
                tag_elems = quote_div.find_all('a', class_='tag')
                tags = [parser.get_text(tag) for tag in tag_elems]
                
                # Build quote dictionary
                quote_data = {
                    "quote": quote_text,
                    "author": author,
                    "tags": tags
                }
                
                quotes_data.append(quote_data)
                self.logger.debug(f"Extracted quote by {author}")
            
            except Exception as e:
                self.logger.error(f"Error extracting quote: {str(e)}")
                continue
        
        return quotes_data


def main():
    """Main function to run the scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape quotes from quotes.toscrape.com")
    parser.add_argument(
        "--url",
        default="https://quotes.toscrape.com/",
        help="URL to scrape (default: https://quotes.toscrape.com/)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--output",
        default="quotes",
        help="Output filename without extension (default: quotes)"
    )
    parser.add_argument(
        "--playwright",
        action="store_true",
        help="Use Playwright instead of requests (for JS-rendered pages)"
    )
    
    args = parser.parse_args()
    
    # Add extension to output filename
    output_filename = f"{args.output}.{args.format}"
    
    # Create and run scraper
    scraper = QuotesScraper(use_playwright=args.playwright)
    
    print(f"\n{'='*60}")
    print(f"ScrapeForge - Quotes Scraper")
    print(f"{'='*60}")
    print(f"URL: {args.url}")
    print(f"Output: {output_filename}")
    print(f"Method: {'Playwright' if args.playwright else 'Requests'}")
    print(f"{'='*60}\n")
    
    try:
        data = scraper.run(
            url=args.url,
            save_format=args.format,
            output_filename=output_filename
        )
        
        print(f"\n{'='*60}")
        print(f"✓ Successfully scraped {len(data)} quotes!")
        print(f"✓ Saved to: output/{output_filename}")
        print(f"{'='*60}\n")
        
        # Display first 3 quotes as preview
        if data:
            print("Preview of scraped data:\n")
            for i, quote in enumerate(data[:3], 1):
                print(f"{i}. \"{quote['quote']}\"")
                print(f"   - {quote['author']}")
                print(f"   Tags: {', '.join(quote['tags'])}\n")
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

