# Advanced Business Web Scraper

Production-ready Python package for comprehensive business intelligence extraction from websites using Selenium WebDriver.

## 📋 Features

- **Comprehensive Data Extraction**
  - Company information (title, description)
  - Pricing plans with features
  - Call-to-action buttons
  - Social media links
  - Integrations and partnerships
  - Trust signals (testimonials, certifications, stats)
  - Headings and content structure

- **Smart Scraping**
  - Automatic page hydration (scrolling, expanding collapsibles)
  - Internal link discovery with junk filtering
  - Anti-detection measures
  - Graceful error handling
  - Deduplication of data

- **Production Ready**
  - Modular architecture
  - Comprehensive logging
  - Structured data models
  - JSON export
  - Formatted reports

## 📁 Project Structure

```
new/
├── __init__.py              # Package initialization
├── config.py                # Configuration and constants
├── models.py                # Data models and schemas
├── utils.py                 # Utility functions
├── extractors.py            # Data extraction logic
├── scraper.py               # Main scraper class
├── main.py                  # CLI and entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to the new folder
cd online/new

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from scraper import AdvancedBusinessScraper

# Create scraper instance
scraper = AdvancedBusinessScraper(headless=False)

try:
    # Scrape website
    business_data = scraper.scrape_website("https://calendly.com", max_pages=8)
    
    # Print formatted report
    print(scraper.get_analysis_report(business_data))
    
finally:
    scraper.close()
```

### Command Line Usage

```bash
# Basic usage
python -m main https://calendly.com

# With options
python -m main https://notion.so --max-pages 15 --headless --output-dir ./results
```

## 📦 Module Overview

### `config.py`
Central configuration file containing:
- Selenium settings
- Scraping limits (max pages, pricing cards, features, etc.)
- XPath selectors for different data types
- Keyword lists for filtering
- Text length constraints

### `models.py`
Data models using Python dataclasses:
- `PricingPlan` - Pricing tier information
- `TrustSignals` - Trust indicators
- `PageData` - Single page scrape result
- `SummaryData` - Aggregated business data
- `BusinessIntelligence` - Complete scrape result

### `utils.py`
Utility functions:
- `normalize_text()` - Clean and normalize text
- `normalize_url()` - Normalize URLs
- `extract_price()` - Extract pricing from text
- `filter_duplicates()` - Remove duplicates while preserving order
- `setup_logger()` - Configure logging

### `extractors.py`
Specialized extractor classes:
- `MetaExtractor` - Title and meta description
- `HeadingExtractor` - H1, H2, H3 headings
- `PricingExtractor` - Pricing plans and features
- `FeaturesExtractor` - Main features/benefits
- `CTAExtractor` - Call-to-action buttons
- `SocialExtractor` - Social media links
- `IntegrationExtractor` - Integrations and partners
- `TrustExtractor` - Testimonials, certifications, stats

### `scraper.py`
Main `AdvancedBusinessScraper` class:
- WebDriver setup and management
- Page scraping orchestration
- Internal link discovery
- Data aggregation
- Report generation

### `main.py`
Entry point with CLI interface:
- Command-line argument parsing
- File I/O (JSON and text reports)
- Wrapper function for easy integration

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Maximum pages to scrape
MAX_PAGES_TO_SCRAPE = 10

# Data extraction limits
MAX_PRICING_CARDS = 10
MAX_FEATURES = 30
MAX_INTEGRATIONS = 20

# Selenium wait timeout
WAIT_TIMEOUT = 15

# Custom keywords for filtering
JUNK_KEYWORDS = ["privacy", "terms", ...]
CTA_KEYWORDS = ["signup", "get started", ...]
```

## 📊 Output Format

### JSON Output (`business_data.json`)

```json
{
  "domain": "example.com",
  "url": "https://example.com",
  "timestamp": 1234567890,
  "pages": {
    "homepage": {
      "url": "https://example.com",
      "title": "Example Company",
      "meta_description": "...",
      "headings": {"h1": [], "h2": [], "h3": []},
      "features": [],
      "pricing": [],
      "ctas": [],
      "social_links": {},
      "integrations": [],
      "trust_signals": {}
    }
  },
  "summary": {
    "company_name": "Example Company",
    "description": "...",
    "pricing_tiers": 3,
    "features_count": 15,
    "ctas": [],
    "socials": {},
    "integrations": []
  }
}
```

### Text Report (`business_intelligence_report.txt`)

```
================================================================================
BUSINESS INTELLIGENCE REPORT - example.com
================================================================================

🏢 COMPANY: Example Company

📝 DESCRIPTION:
This is the company description...

📊 STATISTICS:
  • Pages Scraped: 8
  • Pricing Tiers: 3
  • Unique Features: 15

📢 CALL TO ACTION:
  • Get Started
  • Start Free Trial

🔗 SOCIAL LINKS:
  • Twitter: https://twitter.com/example
  • Linkedin: https://linkedin.com/company/example

🔌 INTEGRATIONS/PARTNERS (8):
  • Stripe
  • Slack
  • ...

================================================================================
```

## 🎯 Use Cases

- **Competitive Analysis** - Extract competitor pricing and features
- **Lead Research** - Gather business information for outreach
- **Market Intelligence** - Analyze industry trends and features
- **Sales Intelligence** - Build enriched prospect databases
- **Business Development** - Research partnership opportunities

## ⚙️ Advanced Usage

### Context Manager

```python
with AdvancedBusinessScraper(headless=True) as scraper:
    data = scraper.scrape_website("https://example.com")
```

### Custom Settings

```python
scraper = AdvancedBusinessScraper(
    headless=True,
    wait_timeout=20  # Increase timeout for slow sites
)
```

### Data Access

```python
business_data = scraper.scrape_website(url)

# Access aggregated summary
summary = business_data.summary
print(f"Company: {summary.company_name}")
print(f"Features: {summary.features_count}")
print(f"Pricing Tiers: {summary.pricing_tiers}")

# Access individual pages
for page_name, page_data in business_data.pages.items():
    print(f"Page: {page_name}")
    print(f"  Pricing: {len(page_data.pricing)} plans")
    print(f"  Features: {len(page_data.features)}")
```

## 🔍 How It Works

1. **Initialization** - Set up Chrome WebDriver with anti-detection measures
2. **Homepage Scrape** - Load and scrape the main website
3. **Page Hydration** - Trigger lazy-loaded content (scrolling, clicking)
4. **Data Extraction** - Extract pricing, features, links, etc.
5. **Link Discovery** - Find internal pages to scrape
6. **Recursive Scraping** - Scrape discovered pages (up to max limit)
7. **Data Aggregation** - Combine data from all pages
8. **Report Generation** - Create formatted report and JSON export

## 🚨 Notes

- **Legal**: Ensure you have permission to scrape websites before using this tool
- **Rate Limiting**: Add delays between requests for high-volume scraping
- **Dynamic Content**: Works with JavaScript-rendered content
- **Error Handling**: Gracefully handles timeouts and missing elements

## 📝 License

This project is for educational and legitimate business purposes only.

## 🤝 Support

For issues or improvements, refer to the module documentation or modify `config.py` for custom behavior.


## start 
uvicorn api:app --host 0.0.0.0 --port 8000 --reload