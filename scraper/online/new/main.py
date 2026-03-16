"""
Production-ready web scraper for business analysis
Entry point and usage examples
Includes integrated social media intelligence scraping
"""

import json
import argparse
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional
from scraper import AdvancedBusinessScraper
from social_media_scraper import SocialMediaIntelligenceScraper
from utils import setup_logger


logger = setup_logger(__name__)


def scrape_business(url: str, max_pages: int = 5, headless: bool = False, output_dir: str = ".", 
                   include_social: bool = True, twitter: str = None, instagram: str = None, 
                   reddit: str = None, linkedin: str = None) -> dict:
    """
    Scrape business website and social media, return comprehensive intelligence data
    
    Args:
        url: Website URL or business name (auto-detects website)
        max_pages: Maximum pages to scrape (default: 20)
        headless: Run browser in headless mode (default: False)
        output_dir: Directory to save output files (default: current directory)
        include_social: Scrape social media data (default: True)
        twitter: Twitter handle (optional, will try to detect from website)
        instagram: Instagram handle (optional, will try to detect from website)
        reddit: Reddit username (optional, will try to detect from website)
        linkedin: LinkedIn company name (optional, will try to detect from website)
    
    Returns:
        Dictionary of business intelligence data (website + social media)
    
    Note:
        If url is a business name instead of a URL, the function will automatically
        search for and find the business website before scraping.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    scraper = AdvancedBusinessScraper(headless=headless)
    
    # Initialize all_data early to prevent UnboundLocalError
    all_data = {
        "business_name": None,
        "website_url": None,
        "website_data": None,
        "social_media_data": None,
        "timestamp": None
    }
    
    try:
        # If input is a business name (not a URL), find the website first
        actual_url = url
        if not url.startswith("http"):
            logger.info(f"\n🔍 Business name detected: '{url}'")
            logger.info("Searching for website...\n")
            actual_url = scraper._search_business_website(url)
            if not actual_url:
                logger.error(f"Could not find website for: {url}")
                return {"error": f"Website not found for: {url}"}
            logger.info(f"Using URL: {actual_url}\n")
        
        # Extract domain name for business naming
        domain = urlparse(actual_url).netloc.replace("www.", "").split(".")[0]
        business_name = domain.replace("-", " ").title()
        
        # Update all_data with actual values
        all_data.update({
            "business_name": business_name,
            "website_url": actual_url,
            "timestamp": None
        })
        
        # ====================================================================
        # PART 1: SCRAPE WEBSITE
        # ====================================================================
        logger.info("=" * 80)
        logger.info(f"🌐 SCRAPING WEBSITE: {actual_url}")
        logger.info("=" * 80)
        
        business_data = scraper.scrape_website(actual_url, max_pages=max_pages)
        all_data["website_data"] = business_data.to_dict()
        
        # Generate website report
        report = scraper.get_analysis_report(business_data)
        
        # Save website report
        report_file = output_path / "business_intelligence_report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"📄 Website report saved to: {report_file}")
        
        # Save raw website data
        data_file = output_path / "business_data.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(business_data.to_dict(), f, indent=2, default=str)
        logger.info(f"💾 Website data saved to: {data_file}")
        
    except Exception as e:
        logger.error(f"❌ Website scraping failed: {e}")
    
    finally:
        scraper.close()
    
    # ====================================================================
    # PART 2: SCRAPE SOCIAL MEDIA
    # ====================================================================
    if include_social:
        try:
            logger.info("")
            logger.info("=" * 80)
            logger.info(f"📱 SCRAPING SOCIAL MEDIA for: {business_name}")
            logger.info("=" * 80)
            
            social_scraper = SocialMediaIntelligenceScraper()
            
            # If handles not provided, try to extract social profile URLs from website data
            def _find_social_link(website_data: dict, key: str) -> Optional[str]:
                # search pages for social_links keys
                pages = website_data.get("pages", {})
                for p in pages.values():
                    sl = p.get("social_links", {}) or {}
                    # case-insensitive key match
                    for k, v in sl.items():
                        if k.lower() == key.lower() and v:
                            return v
                # try top-level socials if present
                top = website_data.get("socials") or website_data.get("social_links") or {}
                for k, v in (top.items() if isinstance(top, dict) else []):
                    if k.lower() == key.lower() and v:
                        return v
                return None

            if not any([twitter, instagram, reddit, linkedin]):
                # attempt to auto-detect URLs from scraped website data
                detected_twitter = _find_social_link(all_data["website_data"], "twitter")
                detected_instagram = _find_social_link(all_data["website_data"], "instagram")
                detected_reddit = _find_social_link(all_data["website_data"], "reddit")
                detected_linkedin = _find_social_link(all_data["website_data"], "linkedin")

                twitter = detected_twitter or None
                instagram = detected_instagram or None
                reddit = detected_reddit or None
                linkedin = detected_linkedin or None

                if any([twitter, instagram, reddit, linkedin]):
                    logger.info(f"ℹ️  Detected social links from website: twitter={twitter}, instagram={instagram}, reddit={reddit}, linkedin={linkedin}")
                else:
                    # fallback to business name handles
                    twitter = business_name.lower().replace(" ", "")
                    instagram = business_name.lower().replace(" ", "")
                    linkedin = business_name
                    logger.info(f"ℹ️  No social links found on site; using heuristic handles: twitter={twitter}, instagram={instagram}")
            
            # Scrape all platforms
            social_data = social_scraper.scrape_all_platforms(
                business_name=business_name,
                twitter_handle=twitter,
                instagram_handle=instagram,
                reddit_handle=reddit,
                linkedin_company=linkedin,
                post_limit=10
            )
            
            all_data["social_media_data"] = social_data.to_dict()
            
            # Generate social media report
            social_report = social_scraper.generate_business_analysis_report(social_data)
            
            # Append social report to website report
            full_report = report + "\n\n" + social_report
            
            # Save combined report
            report_file = output_path / "business_intelligence_report.txt"
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(full_report)
            logger.info(f"📄 Combined report saved to: {report_file}")
            
            # Save combined data
            data_file = output_path / "business_data.json"
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=2, default=str)
            logger.info(f"💾 Combined data saved to: {data_file}")
            
            # Save social media report separately
            social_report_file = output_path / "social_media_report.txt"
            with open(social_report_file, "w", encoding="utf-8") as f:
                f.write(social_report)
            logger.info(f"📱 Social media report saved to: {social_report_file}")
            
            # Save social media data separately
            social_data_file = output_path / "social_media_data.json"
            with open(social_data_file, "w", encoding="utf-8") as f:
                json.dump(social_data.to_dict(), f, indent=2, default=str)
            logger.info(f"📱 Social media data saved to: {social_data_file}")
            
        except Exception as e:
            logger.error(f"❌ Social media scraping failed: {e}")
            logger.warning("⚠️  Continuing with website data only...")
    
    return all_data


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Advanced Web Scraper for Business Intelligence with Social Media Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # By URL
  python -m new https://freshworks.com
  python -m new https://notion.so --max-pages 15 --headless
  
  # By business name (auto-finds website)
  python -m new "Freshworks"
  python -m new "GitHub" --max-pages 15 --headless
  python -m new "Notion" --output-dir ./results
  
  # With social media handles
  python -m new https://calendly.com --twitter calendly --instagram calendly
  python -m new "Calendly" --twitter calendly --instagram calendly
  python -m new https://example.com --no-social
        """
    )
    
    parser.add_argument(
        "url",
        help="Website URL or business name to scrape (e.g., https://example.com or 'Example Company')"
    )
    
    parser.add_argument(
        "--max-pages",
        type=int,
        default=20,
        help="Maximum number of pages to scrape (default: 20)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save output files (default: current directory)"
    )
    
    # NEW: Social media arguments
    parser.add_argument(
        "--no-social",
        action="store_true",
        help="Skip social media scraping (default: False, social media IS scraped)"
    )
    
    parser.add_argument(
        "--twitter",
        type=str,
        default=None,
        help="Twitter handle to scrape (optional, will attempt auto-detection)"
    )
    
    parser.add_argument(
        "--instagram",
        type=str,
        default=None,
        help="Instagram handle to scrape (optional, will attempt auto-detection)"
    )
    
    parser.add_argument(
        "--reddit",
        type=str,
        default=None,
        help="Reddit username to scrape (optional, will attempt auto-detection)"
    )
    
    parser.add_argument(
        "--linkedin",
        type=str,
        default=None,
        help="LinkedIn company name to scrape (optional, will attempt auto-detection)"
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        args.url = "https://" + args.url
    
    logger.info("=" * 80)
    logger.info("🚀 BUSINESS INTELLIGENCE SCRAPER - WEBSITE + SOCIAL MEDIA")
    logger.info("=" * 80)
    logger.info(f"Website URL: {args.url}")
    logger.info(f"Max pages: {args.max_pages}")
    logger.info(f"Headless mode: {args.headless}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Social media scraping: {'ENABLED' if not args.no_social else 'DISABLED'}")
    logger.info(f"Twitter: {args.twitter if args.twitter else 'Auto-detect'}")
    logger.info(f"Instagram: {args.instagram if args.instagram else 'Auto-detect'}")
    logger.info(f"LinkedIn: {args.linkedin if args.linkedin else 'Auto-detect'}")
    logger.info("=" * 80)
    
    try:
        result = scrape_business(
            url=args.url,
            max_pages=args.max_pages,
            headless=args.headless,
            output_dir=args.output_dir,
            include_social=not args.no_social,
            twitter=args.twitter,
            instagram=args.instagram,
            reddit=args.reddit,
            linkedin=args.linkedin
        )
        
        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ SCRAPING COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)
        logger.info(f"📁 Output directory: {Path(args.output_dir).resolve()}")
        logger.info("📄 Files generated:")
        logger.info("   - business_intelligence_report.txt (combined report)")
        logger.info("   - business_data.json (website + social data)")
        if not args.no_social:
            logger.info("   - social_media_report.txt (social media only)")
            logger.info("   - social_media_data.json (social media only)")
        logger.info("=" * 80)
    
    except Exception as e:
        logger.error(f"❌ Scraping failed: {e}")
        raise


if __name__ == "__main__":
    main()
