"""
Data models and schemas for the web scraper
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class PricingPlan:
    """Represents a pricing plan"""
    plan: str
    price: str = "Contact Sales"
    billing: Optional[str] = None
    features: List[str] = field(default_factory=list)
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TrustSignals:
    """Represents trust indicators"""
    testimonials: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    companies: List[str] = field(default_factory=list)
    stats: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PageData:
    """Represents scraped page data"""
    url: str
    title: str = ""
    meta_description: str = ""
    headings: Dict[str, List[str]] = field(default_factory=lambda: {"h1": [], "h2": [], "h3": []})
    features: List[str] = field(default_factory=list)
    pricing: List[Dict[str, Any]] = field(default_factory=list)
    ctas: List[str] = field(default_factory=list)
    social_links: Dict[str, str] = field(default_factory=dict)
    integrations: List[str] = field(default_factory=list)
    trust_signals: Dict[str, List[str]] = field(default_factory=lambda: {
        "testimonials": [], "certifications": [], "companies": [], "stats": []
    })
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SummaryData:
    """Represents aggregated business intelligence summary"""
    company_name: str = ""
    description: str = ""
    domain: str = ""
    website_url: str = ""
    pricing_tiers: int = 0
    features_count: int = 0
    total_pages_scraped: int = 0
    ctas: List[str] = field(default_factory=list)
    socials: Dict[str, str] = field(default_factory=dict)
    integrations: List[str] = field(default_factory=list)
    trust_signals: Dict[str, List[str]] = field(default_factory=lambda: {
        "testimonials": [], "certifications": [], "companies": [], "stats": []
    })
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BusinessIntelligence:
    """Complete business intelligence data"""
    domain: str
    url: str
    timestamp: float
    pages: Dict[str, PageData] = field(default_factory=dict)
    summary: SummaryData = field(default_factory=SummaryData)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "url": self.url,
            "timestamp": self.timestamp,
            "pages": {k: (v.to_dict() if hasattr(v, 'to_dict') else v) for k, v in self.pages.items()},
            "summary": self.summary.to_dict() if hasattr(self.summary, 'to_dict') else self.summary,
        }
