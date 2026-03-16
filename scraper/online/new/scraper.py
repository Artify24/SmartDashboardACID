"""
Main scraper class orchestrating the scraping process
"""

import time
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from typing import Dict, List, Optional, Any

import config
from models import PageData, SummaryData, BusinessIntelligence
from utils import (
    setup_logger, normalize_text, normalize_url, is_internal_url, 
    is_junk_url, extract_domain, get_page_key, filter_duplicates, limit_list
)
from extractors import (
    MetaExtractor, HeadingExtractor, PricingExtractor, 
    FeaturesExtractor, CTAExtractor, SocialExtractor,
    IntegrationExtractor, TrustExtractor
)


class AdvancedBusinessScraper:
    """
    Production-ready web scraper for comprehensive business intelligence
    """
    
    def __init__(self, headless: bool = False, wait_timeout: int = None):
        """
        Initialize scraper
        
        Args:
            headless: Run in headless mode
            wait_timeout: WebDriver wait timeout in seconds
        """
        self.logger = setup_logger(__name__)
        self.wait_timeout = wait_timeout or config.WAIT_TIMEOUT
        self.headless = headless
        self.visited_urls = set()
        
        self.logger.info("Initializing AdvancedBusinessScraper")
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            options = Options()
            
            if self.headless:
                options.add_argument("--headless")
            
            for arg in [
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]:
                options.add_argument(arg)
            
            options.add_argument(f"user-agent={config.CHROME_OPTIONS['user_agent']}")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, self.wait_timeout)
            
            self.logger.info("WebDriver initialized successfully")
        
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def close(self):
        """Close WebDriver"""
        try:
            self.driver.quit()
            self.logger.info("WebDriver closed")
        except Exception as e:
            self.logger.warning(f"Error closing WebDriver: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def hydrate_page(self):
        """Trigger lazy-loaded content"""
        try:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(config.SCROLL_DELAY)
            
            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(config.SCROLL_DELAY)
            
            # Click expandable sections
            for elem in self.driver.find_elements(By.TAG_NAME, "button")[:15]:
                try:
                    text = elem.text.lower()
                    if any(kw in text for kw in ["more", "expand", "details", "show", "features", "product"]):
                        self.driver.execute_script("arguments[0].click();", elem)
                        time.sleep(config.BUTTON_CLICK_DELAY)
                except:
                    pass
        
        except Exception as e:
            self.logger.debug(f"Page hydration error: {e}")
    
    def get_internal_links(self, base_url: str, limit: int = None) -> List[str]:
        """Get internal links from current page"""
        limit = limit or config.MAX_LINKS_PER_PAGE
        domain = extract_domain(base_url)
        links = set()
        
        try:
            for link in self.driver.find_elements(By.TAG_NAME, "a"):
                href = link.get_attribute("href")
                if not href:
                    continue
                
                # Make absolute URL
                href = urljoin(base_url, href)
                
                # Normalize
                href = normalize_url(href)
                
                # Check if internal
                if not is_internal_url(href, domain):
                    continue
                
                # Skip junk
                if is_junk_url(href):
                    continue
                
                links.add(href)
                if len(links) >= limit:
                    break
        
        except Exception as e:
            self.logger.debug(f"Link extraction error: {e}")
        
        return list(links)
    
    def scrape_page(self, url: str) -> Optional[PageData]:
        """
        Scrape single page
        
        Args:
            url: URL to scrape
        
        Returns:
            PageData or None
        """
        if url in self.visited_urls:
            return None
        
        self.visited_urls.add(url)
        
        try:
            self.logger.info(f"📄 Scraping: {url}")
            
            # Load page
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)
            
            # Trigger lazy loading
            self.hydrate_page()
            
            # Extract data
            meta_extractor = MetaExtractor(self.driver, self.logger)
            heading_extractor = HeadingExtractor(self.driver, self.logger)
            pricing_extractor = PricingExtractor(self.driver, self.logger)
            features_extractor = FeaturesExtractor(self.driver, self.logger)
            cta_extractor = CTAExtractor(self.driver, self.logger)
            social_extractor = SocialExtractor(self.driver, self.logger)
            integration_extractor = IntegrationExtractor(self.driver, self.logger)
            trust_extractor = TrustExtractor(self.driver, self.logger)
            
            page_data = PageData(
                url=url,
                title=meta_extractor.get_title(),
                meta_description=meta_extractor.get_meta_description(),
                headings=heading_extractor.extract_headings(),
                features=features_extractor.extract_features(),
                pricing=pricing_extractor.extract_pricing(),
                ctas=cta_extractor.extract_ctas(),
                social_links=social_extractor.extract_socials(),
                integrations=integration_extractor.extract_integrations(),
                trust_signals=trust_extractor.extract_trust_signals(),
            )
            
            return page_data
        
        except TimeoutException:
            self.logger.warning(f"⏱️  Timeout loading: {url}")
            return None
        
        except Exception as e:
            self.logger.error(f"❌ Error scraping {url}: {e}")
            return None
    
    def scrape_website(self, website_url: str, max_pages: int = None) -> BusinessIntelligence:
        """
        Scrape entire website
        
        Args:
            website_url: Starting URL
            max_pages: Maximum pages to scrape
        
        Returns:
            BusinessIntelligence object
        """
        max_pages = max_pages or config.MAX_PAGES_TO_SCRAPE
        
        self.logger.info(f"\n🚀 Starting business scrape: {website_url}\n")
        
        domain = extract_domain(website_url)
        business_data = BusinessIntelligence(
            domain=domain,
            url=website_url,
            timestamp=time.time(),
            pages={},
            summary=SummaryData(domain=domain, website_url=website_url)
        )
        
        try:
            # Scrape homepage
            homepage_data = self.scrape_page(website_url)
            if homepage_data:
                business_data.pages["homepage"] = homepage_data
                company_name = homepage_data.title.split("|")[0].split("-")[0].strip()
                business_data.summary.company_name = company_name
                business_data.summary.description = homepage_data.meta_description
            else:
                self.logger.warning("Failed to scrape homepage")
            
            # Discover internal pages
            self.logger.info("\n🔍 Discovering internal pages...")
            internal_links = self.get_internal_links(website_url, max_pages)
            
            pages_scraped = 1  # homepage
            for link in internal_links:
                if pages_scraped >= max_pages:
                    break
                
                page_data = self.scrape_page(link)
                if page_data:
                    page_key = get_page_key(link)
                    business_data.pages[page_key] = page_data
                    pages_scraped += 1
            
            # Aggregate summary
            self.logger.info("\n📊 Aggregating data...\n")
            self._aggregate_summary(business_data)
            
            self.logger.info("✅ Scraping completed successfully!\n")
        
        except Exception as e:
            self.logger.error(f"❌ Scraping failed: {e}")
        
        return business_data
    
    def _aggregate_summary(self, business_data: BusinessIntelligence):
        """Aggregate data across all pages"""
        all_pricing = []
        all_features = set()
        all_ctas = set()
        all_socials = {}
        all_integrations = set()
        all_trust_signals = {
            "testimonials": [],
            "certifications": [],
            "companies": [],
            "stats": []
        }
        
        for page in business_data.pages.values():
            if page:
                all_pricing.extend(page.pricing)
                all_features.update(page.features)
                all_ctas.update(page.ctas)
                all_socials.update(page.social_links)
                all_integrations.update(page.integrations)
                
                for key, values in page.trust_signals.items():
                    all_trust_signals[key].extend(values)
        
        # Safely extract pricing tiers (handle both dict and string formats)
        pricing_plans = set()
        for p in all_pricing:
            if isinstance(p, dict) and "plan" in p:
                pricing_plans.add(p.get("plan"))
            elif isinstance(p, str):
                pricing_plans.add(p)
        business_data.summary.pricing_tiers = len(pricing_plans)
        
        business_data.summary.features_count = len(all_features)
        business_data.summary.total_pages_scraped = len(business_data.pages)
        business_data.summary.ctas = limit_list(list(all_ctas), 5)
        business_data.summary.socials = all_socials
        business_data.summary.integrations = limit_list(list(all_integrations), config.MAX_INTEGRATIONS)
        
        # Deduplicate and limit trust signals
        for key in all_trust_signals:
            all_trust_signals[key] = limit_list(filter_duplicates(all_trust_signals[key]), 10)
        
        business_data.summary.trust_signals = all_trust_signals
    
    def get_analysis_report(self, business_data: BusinessIntelligence) -> str:
        """Generate formatted analysis report"""
        report = []
        report.append("=" * 80)
        report.append(f"BUSINESS INTELLIGENCE REPORT - {business_data.domain}")
        report.append("=" * 80)
        
        summary = business_data.summary
        
        if summary.company_name:
            report.append(f"\n🏢 COMPANY: {summary.company_name}")
        
        if summary.description:
            report.append(f"\n📝 DESCRIPTION:\n{summary.description}\n")
        
        report.append(f"\n📊 STATISTICS:")
        report.append(f"  • Pages Scraped: {summary.total_pages_scraped}")
        report.append(f"  • Pricing Tiers: {summary.pricing_tiers}")
        report.append(f"  • Unique Features: {summary.features_count}")
        
        if summary.ctas:
            report.append(f"\n📢 CALL TO ACTION:\n" + "\n".join(f"  • {cta}" for cta in summary.ctas))
        
        if summary.socials:
            report.append(f"\n🔗 SOCIAL LINKS:")
            for platform, link in summary.socials.items():
                report.append(f"  • {platform.capitalize()}: {link}")
        
        if summary.integrations:
            report.append(f"\n🔌 INTEGRATIONS/PARTNERS ({len(summary.integrations)}):\n" + 
                         "\n".join(f"  • {integ}" for integ in summary.integrations))
        
        if summary.trust_signals.get("testimonials"):
            report.append(f"\n💬 TESTIMONIALS ({len(summary.trust_signals['testimonials'])}):\n" + 
                         "\n".join(f"  • {t[:100]}..." for t in summary.trust_signals["testimonials"][:3]))
        
        if summary.trust_signals.get("certifications"):
            report.append(f"\n✅ CERTIFICATIONS:\n" + 
                         "\n".join(f"  • {c}" for c in summary.trust_signals["certifications"]))
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)