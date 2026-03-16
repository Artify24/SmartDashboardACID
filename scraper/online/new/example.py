"""
Example usage patterns for the Advanced Business Scraper
Run this file to see different ways to use the scraper
"""

import json
from pathlib import Path
from scraper import AdvancedBusinessScraper


def example_1_basic_usage():
    """Example 1: Basic scraping with default settings"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80 + "\n")
    
    scraper = AdvancedBusinessScraper(headless=False)
    
    try:
        # Scrape website
        business_data = scraper.scrape_website("https://calendly.com", max_pages=5)
        
        # Print report
        print(scraper.get_analysis_report(business_data))
    
    finally:
        scraper.close()


def example_2_context_manager():
    """Example 2: Using context manager for automatic cleanup"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Context Manager Pattern")
    print("="*80 + "\n")
    
    with AdvancedBusinessScraper(headless=True) as scraper:
        business_data = scraper.scrape_website("https://github.com", max_pages=3)
        
        summary = business_data.summary
        print(f"Company: {summary.company_name}")
        print(f"Pages Scraped: {summary.total_pages_scraped}")
        print(f"Pricing Tiers: {summary.pricing_tiers}")
        print(f"Total Features: {summary.features_count}")
        print(f"\nSocial Links: {json.dumps(summary.socials, indent=2)}")


def example_3_data_access():
    """Example 3: Accessing detailed page data"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Detailed Data Access")
    print("="*80 + "\n")
    
    with AdvancedBusinessScraper(headless=True) as scraper:
        business_data = scraper.scrape_website("https://slack.com", max_pages=4)
        
        # Access individual pages
        for page_name, page_data in business_data.pages.items():
            print(f"\n📄 Page: {page_name}")
            print(f"   Title: {page_data.title}")
            print(f"   URL: {page_data.url}")
            print(f"   Pricing Plans: {len(page_data.pricing)}")
            print(f"   Features: {len(page_data.features)}")
            print(f"   CTAs: {len(page_data.ctas)}")
            
            # Show first 2 features
            if page_data.features:
                print(f"   Sample Features:")
                for feature in page_data.features[:2]:
                    print(f"     • {feature}")


def example_4_export_data():
    """Example 4: Exporting data to files"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Exporting Data")
    print("="*80 + "\n")
    
    output_dir = Path("./scraper_output")
    output_dir.mkdir(exist_ok=True)
    
    with AdvancedBusinessScraper(headless=True) as scraper:
        business_data = scraper.scrape_website("https://notion.so", max_pages=5)
        
        # Save JSON
        json_file = output_dir / "business_data.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(business_data.to_dict(), f, indent=2, default=str)
        print(f"✅ JSON saved to: {json_file}")
        
        # Save report
        report_file = output_dir / "report.txt"
        report = scraper.get_analysis_report(business_data)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Report saved to: {report_file}")


def example_5_pricing_analysis():
    """Example 5: Analyze pricing plans"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Pricing Analysis")
    print("="*80 + "\n")
    
    with AdvancedBusinessScraper(headless=True) as scraper:
        business_data = scraper.scrape_website("https://stripe.com", max_pages=6)
        
        print(f"Found {business_data.summary.pricing_tiers} pricing tiers\n")
        
        # Collect all pricing plans
        all_plans = {}
        for page_name, page_data in business_data.pages.items():
            for plan in page_data.pricing:
                plan_name = plan.get("plan", "Unknown")
                if plan_name not in all_plans:
                    all_plans[plan_name] = {
                        "price": plan.get("price"),
                        "pages_found": 1,
                        "features": plan.get("features", [])
                    }
                else:
                    all_plans[plan_name]["pages_found"] += 1
        
        # Display pricing
        if all_plans:
            print("💰 PRICING PLANS:")
            for plan_name, plan_info in all_plans.items():
                print(f"\n  {plan_name}")
                print(f"    Price: {plan_info['price']}")
                print(f"    Found on {plan_info['pages_found']} page(s)")
                print(f"    Features: {len(plan_info['features'])}")
                for feature in plan_info['features'][:3]:
                    print(f"      • {feature}")


def example_6_competitive_analysis():
    """Example 6: Compare multiple websites"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Competitive Analysis")
    print("="*80 + "\n")
    
    websites = [
        "https://calendly.com",
        "https://acuityscheduling.com",
    ]
    
    comparison_data = {}
    
    for url in websites:
        with AdvancedBusinessScraper(headless=True) as scraper:
            business_data = scraper.scrape_website(url, max_pages=4)
            
            comparison_data[business_data.domain] = {
                "company": business_data.summary.company_name,
                "pages_scraped": business_data.summary.total_pages_scraped,
                "pricing_tiers": business_data.summary.pricing_tiers,
                "features": business_data.summary.features_count,
                "integrations": len(business_data.summary.integrations),
            }
    
    # Display comparison
    print("COMPETITIVE ANALYSIS:\n")
    print(f"{'Domain':<25} {'Company':<25} {'Pages':<8} {'Pricing':<10} {'Features':<10}")
    print("-" * 80)
    
    for domain, data in comparison_data.items():
        print(f"{domain:<25} {data['company']:<25} {data['pages_scraped']:<8} "
              f"{data['pricing_tiers']:<10} {data['features']:<10}")


def example_7_custom_timeout():
    """Example 7: Custom settings for slow websites"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Custom Timeout Settings")
    print("="*80 + "\n")
    
    # Use longer timeout for slower websites
    with AdvancedBusinessScraper(headless=True, wait_timeout=25) as scraper:
        business_data = scraper.scrape_website("https://example.com", max_pages=3)
        
        print(f"✅ Successfully scraped {business_data.domain}")
        print(f"   Total pages: {business_data.summary.total_pages_scraped}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║         Advanced Business Web Scraper - Usage Examples                     ║
    ║                                                                            ║
    ║  This script demonstrates different ways to use the scraper. Uncomment    ║
    ║  the examples you want to run and execute: python example.py              ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Uncomment the examples you want to run:
    
    # Basic usage
    # example_1_basic_usage()
    
    # Context manager pattern
    # example_2_context_manager()
    
    # Data access patterns
    # example_3_data_access()
    
    # Export data to files
    # example_4_export_data()
    
    # Pricing analysis
    # example_5_pricing_analysis()
    
    # Competitive analysis
    # example_6_competitive_analysis()
    
    # Custom timeout for slow sites
    # example_7_custom_timeout()
    
    print("\n💡 To run examples, uncomment them in this file and execute:")
    print("   python example.py\n")
