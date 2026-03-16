"""
Configuration and constants for the web scraper
"""

import logging

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# ============================================================================
# SELENIUM CONFIGURATION
# ============================================================================
WAIT_TIMEOUT = 15  # seconds
SCROLL_DELAY = 0.5  # seconds
BUTTON_CLICK_DELAY = 0.2  # seconds

# Chrome options
CHROME_OPTIONS = {
    "disable_automation": True,
    "start_maximized": True,
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
    "disable_gpu": True,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


# ============================================================================
# SCRAPING CONFIGURATION
# ============================================================================
MAX_PAGES_TO_SCRAPE = 10
MAX_PRICING_CARDS = 10
MAX_FEATURES = 30
MAX_INTEGRATIONS = 20
MAX_CTA_BUTTONS = 10
MAX_TESTIMONIALS = 10
MAX_LINKS_PER_PAGE = 50
MAX_HEADINGS = 15

# URL filtering
JUNK_KEYWORDS = [
    "privacy", "terms", "cookie", "legal", "status",
    "security", "gdpr", "careers", "press", "login",
    "signup", "auth", "about-us", "contact-us", "faq",
    "blog", "news", "sitemap", "legal", "investors"
]

# CTA keywords
CTA_KEYWORDS = [
    "signup", "sign up", "get started", "try", "start free",
    "demo", "contact", "download", "join", "create account",
    "register", "begin", "start now", "request demo"
]

# Feature keywords
FEATURE_KEYWORDS = [
    "feature", "capability", "support", "include",
    "enables", "allows", "provides", "advanced"
]

# Integration keywords
INTEGRATION_KEYWORDS = [
    "integration", "partner", "support", "connect",
    "compatible", "works with", "api"
]

# Certification keywords
CERT_KEYWORDS = [
    "iso", "soc2", "gdpr", "certified", "accredited",
    "enterprise", "trust", "security", "compliance"
]

# Price keywords
PRICE_KEYWORDS = [
    "price", "pricing", "cost", "fee", "plan",
    "subscription", "tier", "package", "billing"
]


# ============================================================================
# DATA EXTRACTION CONFIGURATION
# ============================================================================
TEXT_MIN_LENGTH = 3
TEXT_MAX_LENGTH = 200

# Pricing pattern
PRICING_PATTERNS = [
    r'[\$€₹]\s*\d+[,.]?\d*(?:/(?:month|year|mo|yr))?',
    r'(?:Rs\.?|INR)\s*\d+(?:[,\.]\d+)?(?:\s*(?:per|/)\s*(?:month|year|mo|yr))?',
    r'\d+[,.]?\d*\s*(?:per|\/)\s*(?:month|year|mo|yr)',
    r'(?:from|starting\s+at|onwards)\s+₹?\s*\d+(?:[,\.]\d+)?',
]

# Feature description min/max
FEATURE_MIN_LENGTH = 5
FEATURE_MAX_LENGTH = 150

# Plan name constraints
PLAN_NAME_MIN_LENGTH = 3
PLAN_NAME_MAX_LENGTH = 50


# ============================================================================
# XPath SELECTORS
# ============================================================================
PRICING_SELECTORS = [
    "//div[contains(@class, 'pricing')]",
    "//section[contains(@class, 'price')]",
    "//div[contains(@class, 'plan')]",
    "//article[contains(@class, 'plan')]",
    "//div[@class='plan']",
    "//div[@class='pricing-card']",
]

FEATURES_SELECTORS = [
    "//div[contains(@class, 'feature')]",
    "//section[contains(@class, 'feature')]",
    "//li[contains(@class, 'feature')]",
    "//div[@class='features']//li",
    "//section[@class='features']//li",
]

INTEGRATIONS_SELECTORS = [
    "//div[contains(@class, 'integration')]",
    "//section[contains(@class, 'integration')]",
    "//div[contains(@class, 'partner')]",
    "//img[contains(@alt, 'logo')]",
]

TESTIMONIALS_SELECTORS = [
    "//div[contains(@class, 'testimonial')]",
    "//section[contains(@class, 'testimonial')]",
    "//blockquote",
]


# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================
OUTPUT_FORMAT = "json"  # json or dict
OUTPUT_FILE = "business_data.json"
REPORT_FILE = "business_intelligence_report.txt"
