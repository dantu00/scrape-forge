# 🔨 ScrapeForge

**A production-ready, extensible web scraping toolkit for Python**

ScrapeForge is a powerful and flexible web scraping boilerplate that provides everything you need to build robust scrapers quickly. It includes HTTP client utilities, HTML parsing helpers, proxy rotation, user-agent rotation, retry logic, Playwright integration for JavaScript-rendered pages, and a clean architecture for building maintainable scrapers.

---

## ✨ Features

- 🚀 **Ready-to-use base scraper class** - Extend `BaseScraper` and focus on your scraping logic
- 🔄 **Automatic retry logic** - Built-in exponential backoff for failed requests
- 🎭 **User-Agent rotation** - Randomize user agents to avoid detection
- 🌐 **Proxy rotation** - Optional proxy support with automatic rotation
- 🎨 **HTML parsing utilities** - BeautifulSoup4 wrapper with convenient methods
- 🎪 **Playwright fallback** - Seamlessly handle JavaScript-rendered content
- 📊 **Multiple output formats** - Save data as JSON or CSV
- 🎯 **Rich logging** - Beautiful console output with detailed logging
- ⚙️ **Environment-based configuration** - Easy configuration via `.env` files
- 🏗️ **Clean architecture** - Well-organized, maintainable codebase

---

## 📁 Project Structure

```
scrapeforge/
├── src/
│   ├── core/
│   │   ├── base_scraper.py       # Abstract base class for scrapers
│   │   ├── html_parser.py        # HTML parsing utilities
│   │   ├── request_client.py     # HTTP client with retry logic
│   │   ├── playwright_client.py  # Playwright integration
│   │   ├── logger.py             # Logging configuration
│   │   └── config.py             # Configuration management
│   └── utils/
│       ├── proxy_rotator.py      # Proxy rotation utility
│       └── user_agent_rotator.py # User-agent rotation utility
├── examples/
│   └── example_basic_scraper.py  # Example scraper implementation
├── tests/                        # Test directory
├── output/                       # Default output directory (auto-created)
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project metadata
├── .env.example                 # Example environment configuration
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip or poetry for package management

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/alperenderici/ScrapeForge.git
cd ScrapeForge
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers** (required for JavaScript rendering)

```bash
playwright install
```

5. **Configure environment** (optional)

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

---

## 📖 Usage

### Running the Example Scraper

The included example scraper demonstrates how to scrape quotes from `quotes.toscrape.com`:

```bash
# Basic usage (saves as JSON)
python examples/example_basic_scraper.py

# Save as CSV
python examples/example_basic_scraper.py --format csv

# Use Playwright for JavaScript rendering
python examples/example_basic_scraper.py --playwright

# Custom URL and output filename
python examples/example_basic_scraper.py --url "https://quotes.toscrape.com/page/2/" --output quotes_page2
```

### Creating Your Own Scraper

1. **Create a new scraper class** by extending `BaseScraper`:

```python
from src.core.base_scraper import BaseScraper
from typing import List, Dict, Any

class MyScraper(BaseScraper):
    def scrape(self, url: str) -> List[Dict[str, Any]]:
        # Fetch HTML
        html = self.fetch_html(url)
        
        # Parse HTML
        parser = self.parse_html(html)
        
        # Extract data
        data = []
        items = parser.find_all('div', class_='item')
        
        for item in items:
            data.append({
                'title': parser.get_text(item.find('h2')),
                'description': parser.get_text(item.find('p'))
            })
        
        return data
```

2. **Run your scraper**:

```python
scraper = MyScraper()
results = scraper.run(
    url="https://example.com",
    save_format="json",
    output_filename="results.json"
)
```

---

## 🔧 Advanced Features

### Using Playwright for JavaScript-Rendered Pages

When a website requires JavaScript to render content, use Playwright:

```python
from src.core.base_scraper import BaseScraper

class JSRenderedScraper(BaseScraper):
    def __init__(self):
        # Enable Playwright mode
        super().__init__(use_playwright=True)

    def scrape(self, url: str):
        html = self.fetch_html(url)
        parser = self.parse_html(html)
        # ... extract data
```

### Proxy Rotation

1. Create a `proxies.txt` file with one proxy per line:

```
http://proxy1.example.com:8080
http://user:pass@proxy2.example.com:8080
```

2. Enable proxy rotation in `.env`:

```env
USE_PROXY=true
PROXY_LIST_FILE=proxies.txt
```

### Custom User Agents

```python
from src.utils.user_agent_rotator import UserAgentRotator

rotator = UserAgentRotator()
rotator.add_agent("Mozilla/5.0 (Custom User Agent)")
user_agent = rotator.get_random()
```

### Custom Request Headers

```python
scraper = MyScraper()
html = scraper.request_client.get(
    url="https://example.com",
    headers={
        "Authorization": "Bearer token",
        "Custom-Header": "value"
    }
)
```

---

## ⚙️ Configuration

All configuration options can be set via environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |
| `MAX_RETRIES` | `3` | Maximum retry attempts |
| `RETRY_BACKOFF` | `1.0` | Backoff factor for retries |
| `USE_PROXY` | `false` | Enable proxy rotation |
| `PROXY_LIST_FILE` | - | Path to proxy list file |
| `ROTATE_USER_AGENT` | `true` | Enable user-agent rotation |
| `PLAYWRIGHT_HEADLESS` | `true` | Run Playwright in headless mode |
| `PLAYWRIGHT_TIMEOUT` | `30000` | Playwright timeout (milliseconds) |
| `OUTPUT_DIR` | `output` | Directory for output files |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FILE` | - | Optional log file path |

---

## 📚 API Reference

### BaseScraper

The abstract base class for all scrapers.

**Methods:**
- `scrape(url: str) -> List[Dict[str, Any]]` - **Abstract method** to implement scraping logic
- `fetch_html(url: str) -> str` - Fetch HTML from URL
- `parse_html(html: str) -> HTMLParser` - Parse HTML content
- `save_json(data, filename)` - Save data as JSON
- `save_csv(data, filename)` - Save data as CSV
- `run(url, save_format, output_filename)` - Run scraper and save results

### RequestClient

HTTP client with retry logic and rotation.

**Methods:**
- `get(url, headers, params, **kwargs)` - Perform GET request
- `post(url, headers, data, json, **kwargs)` - Perform POST request
- `close()` - Close the session

### HTMLParser

HTML parsing utilities using BeautifulSoup4.

**Methods:**
- `find(tag, **kwargs)` - Find first occurrence of tag
- `find_all(tag, **kwargs)` - Find all occurrences of tag
- `select(selector)` - Find elements using CSS selector
- `select_one(selector)` - Find first element using CSS selector
- `get_text(tag, strip=True)` - Extract text from tag
- `get_attribute(tag, attr, default)` - Get attribute value
- `extract_links(base_url)` - Extract all links
- `extract_images(base_url)` - Extract all image URLs

### PlaywrightClient

Playwright integration for JavaScript-rendered pages.

**Methods:**
- `start()` - Start the browser
- `goto(url, wait_until, timeout)` - Navigate to URL
- `wait_for_selector(selector, timeout, state)` - Wait for element
- `click(selector, timeout)` - Click element
- `fill(selector, value, timeout)` - Fill input field
- `screenshot(path, full_page)` - Take screenshot
- `evaluate(script)` - Execute JavaScript
- `get_content()` - Get page HTML
- `close()` - Close browser

---

## 🧪 Testing

Run tests using pytest (when implemented):

```bash
pytest tests/
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run code formatting
black src/ examples/

# Run linting
flake8 src/ examples/

# Run type checking
mypy src/
```

---

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 ScrapeForge Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Requests](https://requests.readthedocs.io/) - HTTP library
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Playwright](https://playwright.dev/python/) - Browser automation
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

## 📧 Support

If you have questions or need help:

- 📖 Check the [documentation](https://github.com/alperenderici/ScrapeForge)
- 🐛 [Open an issue](https://github.com/alperenderici/ScrapeForge/issues)
- 💬 Start a [discussion](https://github.com/alperenderici/ScrapeForge/discussions)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Happy Scraping! 🚀**

