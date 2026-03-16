"""
Utility functions for text processing, URL handling, and logging
"""

import re
import logging
from urllib.parse import urlparse, urljoin
from typing import List, Set, Optional, Tuple
import config


def setup_logger(name: str) -> logging.Logger:
    """Setup and return a logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(config.LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def normalize_text(text: Optional[str]) -> str:
    """
    Clean and normalize text by removing extra whitespace
    
    Args:
        text: Text to normalize
    
    Returns:
        Normalized text
    """
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())


def normalize_url(url: str) -> str:
    """
    Normalize URL by removing fragment and trailing slash
    
    Args:
        url: URL to normalize
    
    Returns:
        Normalized URL
    """
    return url.split("#")[0].rstrip("/")


def is_internal_url(url: str, base_domain: str) -> bool:
    """
    Check if URL is internal to the domain
    
    Args:
        url: URL to check
        base_domain: Base domain to compare against
    
    Returns:
        True if internal, False otherwise
    """
    return base_domain in url.lower()


def is_junk_url(url: str) -> bool:
    """
    Check if URL contains junk keywords
    
    Args:
        url: URL to check
    
    Returns:
        True if junk URL, False otherwise
    """
    url_lower = url.lower()
    return any(junk in url_lower for junk in config.JUNK_KEYWORDS)


def extract_domain(url: str) -> str:
    """
    Extract domain from URL
    
    Args:
        url: Full URL
    
    Returns:
        Domain name
    """
    return urlparse(url).netloc


def extract_path(url: str) -> str:
    """
    Extract path from URL
    
    Args:
        url: Full URL
    
    Returns:
        URL path
    """
    return urlparse(url).path.strip("/")


def extract_price(text: str) -> Optional[str]:
    """
    Extract price from text using regex patterns
    
    Args:
        text: Text to search for price
    
    Returns:
        Extracted price or None
    """
    for pattern in config.PRICING_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    if "free" in text.lower():
        return "Free"
    
    return None


def extract_plan_name(text: str) -> Optional[str]:
    """
    Extract plan name from text
    
    Args:
        text: Text to extract plan name from
    
    Returns:
        Plan name or None
    """
    # Remove price indicators
    plan_text = re.sub(r'[\$€₹]|\d{2,}', '', text)
    plan_text = normalize_text(plan_text)
    
    if config.PLAN_NAME_MIN_LENGTH < len(plan_text) < config.PLAN_NAME_MAX_LENGTH:
        return plan_text
    
    return None


def filter_duplicates(items: List[str]) -> List[str]:
    """
    Remove duplicates from list while preserving order
    
    Args:
        items: List of items
    
    Returns:
        List with duplicates removed
    """
    seen = set()
    result = []
    
    for item in items:
        normalized = normalize_text(item).lower()
        if normalized not in seen:
            seen.add(normalized)
            result.append(item)
    
    return result


def limit_list(items: List[str], max_items: int) -> List[str]:
    """
    Limit list to max items
    
    Args:
        items: List of items
        max_items: Maximum number of items
    
    Returns:
        Limited list
    """
    return items[:max_items]


def validate_text_length(text: str, min_len: int = None, max_len: int = None) -> bool:
    """
    Validate text length constraints
    
    Args:
        text: Text to validate
        min_len: Minimum length (uses config default if None)
        max_len: Maximum length (uses config default if None)
    
    Returns:
        True if valid, False otherwise
    """
    min_len = min_len or config.TEXT_MIN_LENGTH
    max_len = max_len or config.TEXT_MAX_LENGTH
    
    return min_len <= len(text) <= max_len


def clean_text_for_storage(text: str) -> str:
    """
    Clean text for storage (removes special chars, normalizes)
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    # Remove control characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    
    # Normalize whitespace
    text = normalize_text(text)
    
    return text


def batch_urls(urls: List[str], batch_size: int = 5) -> List[List[str]]:
    """
    Split URLs into batches
    
    Args:
        urls: List of URLs
        batch_size: Size of each batch
    
    Returns:
        List of URL batches
    """
    return [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]


def get_page_key(url: str) -> str:
    """
    Generate a unique page key from URL
    
    Args:
        url: URL to generate key from
    
    Returns:
        Page key (safe for use as dict key)
    """
    path = extract_path(url)
    page_key = path.replace("/", "_").replace("-", "_")[:60]
    return page_key or "homepage"


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Recursively merge two dictionaries
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary to merge
    
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result
