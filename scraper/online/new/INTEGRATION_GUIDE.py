"""
Integration Guide: How to use Social Media Scraper with Main Application
This file shows best practices and integration patterns
"""

# ============================================================================
# PATTERN 1: Simple Integration with Existing Main
# ============================================================================

def integrate_with_main():
    """
    Pattern 1: Add social media scraping to existing main function
    """
    from social_media_scraper import scrape_social_media
    
    # After scraping website (existing code), add social media scraping
    business_name = "Acme Corp"
    
    # Existing website scraping code
    # ... (your existing scraper code) ...
    
    # NEW: Add social media scraping
    social_data = scrape_social_media(
        business_name=business_name,
        twitter_handle="acmecorp",
        instagram_handle="acmecorp_official",
        reddit_handle="acmecorp",
        linkedin_company="Acme Corporation",
        post_limit=10,
        output_dir="./business_intelligence"
    )
    
    return {
        "website_data": {},  # existing data
        "social_media_data": social_data  # new social data
    }


# ============================================================================
# PATTERN 2: Command Line Integration
# ============================================================================

def add_social_media_cli_commands():
    """
    Pattern 2: Add social media commands to CLI
    Add this to your main.py argparse section
    """
    import argparse
    from social_media_scraper import scrape_social_media
    
    parser = argparse.ArgumentParser(description="Business Intelligence Scraper")
    
    # Existing arguments
    parser.add_argument("url", help="Website URL to scrape")
    
    # NEW: Social media arguments
    parser.add_argument(
        "--social",
        action="store_true",
        help="Also scrape social media data"
    )
    
    parser.add_argument(
        "--twitter",
        type=str,
        help="Twitter handle to scrape"
    )
    
    parser.add_argument(
        "--instagram",
        type=str,
        help="Instagram handle to scrape"
    )
    
    parser.add_argument(
        "--reddit",
        type=str,
        help="Reddit username to scrape"
    )
    
    parser.add_argument(
        "--linkedin",
        type=str,
        help="LinkedIn company name to scrape"
    )
    
    parser.add_argument(
        "--posts",
        type=int,
        default=10,
        help="Number of recent posts to analyze (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Process social media if requested
    if args.social:
        scrape_social_media(
            business_name="Your Business",
            twitter_handle=args.twitter,
            instagram_handle=args.instagram,
            reddit_handle=args.reddit,
            linkedin_company=args.linkedin,
            post_limit=args.posts,
            output_dir="."
        )


# ============================================================================
# PATTERN 3: Unified Report Generation
# ============================================================================

def generate_unified_business_report(website_data, social_media_data):
    """
    Pattern 3: Generate a unified report combining website and social data
    """
    from datetime import datetime
    
    report = []
    report.append("=" * 100)
    report.append("COMPREHENSIVE BUSINESS INTELLIGENCE REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 100)
    report.append("")
    
    # Section 1: Website Analysis
    report.append("SECTION 1: WEBSITE INTELLIGENCE")
    report.append("-" * 100)
    report.append(f"Website: {website_data.get('url', 'N/A')}")
    report.append(f"Pages Scraped: {website_data.get('total_pages', 0)}")
    report.append(f"Features Found: {website_data.get('features_count', 0)}")
    report.append(f"Pricing Tiers: {website_data.get('pricing_tiers', 0)}")
    report.append("")
    
    # Section 2: Social Media Analysis
    report.append("SECTION 2: SOCIAL MEDIA INTELLIGENCE")
    report.append("-" * 100)
    
    if "twitter_analytics" in social_media_data and social_media_data["twitter_analytics"]:
        twitter = social_media_data["twitter_analytics"]
        report.append(f"Twitter Followers: {twitter['total_followers']:,}")
        report.append(f"Twitter Avg Engagement: {twitter['average_engagement_rate']:.2f}%")
    
    if "instagram_analytics" in social_media_data and social_media_data["instagram_analytics"]:
        insta = social_media_data["instagram_analytics"]
        report.append(f"Instagram Followers: {insta['total_followers']:,}")
        report.append(f"Instagram Avg Engagement: {insta['average_engagement_rate']:.2f}%")
    
    if "linkedin_analytics" in social_media_data and social_media_data["linkedin_analytics"]:
        linkedin = social_media_data["linkedin_analytics"]
        report.append(f"LinkedIn Followers: {linkedin['total_followers']:,}")
        report.append(f"LinkedIn Avg Engagement: {linkedin['average_engagement_rate']:.2f}%")
    
    report.append("")
    
    # Section 3: Recommendations
    report.append("SECTION 3: BUSINESS RECOMMENDATIONS")
    report.append("-" * 100)
    report.append("✓ Maintain consistent brand messaging across all platforms")
    report.append("✓ Focus on high-engagement content types identified in social analysis")
    report.append("✓ Align social media strategy with website offerings")
    report.append("✓ Monitor competitor social media presence")
    report.append("✓ Engage actively with audience comments")
    report.append("")
    
    report.append("=" * 100)
    
    return "\n".join(report)


# ============================================================================
# PATTERN 4: Batch Processing Multiple Businesses
# ============================================================================

def batch_scrape_businesses(businesses_list):
    """
    Pattern 4: Process multiple businesses at once
    Useful for analyzing entire industries or client portfolios
    """
    from social_media_scraper import SocialMediaIntelligenceScraper
    from pathlib import Path
    import json
    
    scraper = SocialMediaIntelligenceScraper()
    results = []
    
    for business in businesses_list:
        print(f"\nProcessing: {business['name']}")
        
        intelligence = scraper.scrape_all_platforms(
            business_name=business["name"],
            twitter_handle=business.get("twitter"),
            instagram_handle=business.get("instagram"),
            reddit_handle=business.get("reddit"),
            linkedin_company=business.get("linkedin"),
            post_limit=10
        )
        
        results.append(intelligence.to_dict())
        
        # Generate report for each
        report = scraper.generate_business_analysis_report(intelligence)
        
        # Save individual report
        output_dir = Path(f"./business_reports/{business['name']}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "report.txt", "w") as f:
            f.write(report)
        
        with open(output_dir / "data.json", "w") as f:
            json.dump(intelligence.to_dict(), f, indent=2, default=str)
    
    # Save batch comparison
    comparison_file = Path("./batch_comparison.json")
    with open(comparison_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Processed {len(results)} businesses")
    print(f"📊 Batch comparison saved to {comparison_file}")
    
    return results


# ============================================================================
# PATTERN 5: Scheduled Periodic Scraping
# ============================================================================

def setup_scheduled_scraping():
    """
    Pattern 5: Set up periodic scraping with APScheduler
    Requires: pip install apscheduler
    """
    from apscheduler.schedulers.background import BackgroundScheduler
    from social_media_scraper import scrape_social_media
    from datetime import datetime
    
    def scrape_job():
        """Job to run periodically"""
        print(f"[{datetime.now()}] Starting scheduled scrape...")
        
        try:
            scrape_social_media(
                business_name="MyBusiness",
                twitter_handle="mybusiness",
                instagram_handle="mybusiness",
                reddit_handle="mybusiness",
                linkedin_company="My Business Inc",
                post_limit=10,
                output_dir="./scheduled_reports"
            )
            print(f"[{datetime.now()}] Scrape completed successfully")
        
        except Exception as e:
            print(f"[{datetime.now()}] Error during scrape: {e}")
    
    # Create scheduler
    scheduler = BackgroundScheduler()
    
    # Schedule job to run every 24 hours
    scheduler.add_job(scrape_job, 'interval', hours=24)
    
    # Or schedule for specific times
    # scheduler.add_job(scrape_job, 'cron', hour=9, minute=0)  # 9 AM daily
    # scheduler.add_job(scrape_job, 'cron', day_of_week='mon-fri', hour=9)  # 9 AM weekdays
    
    scheduler.start()
    
    return scheduler


# ============================================================================
# PATTERN 6: Real-time Monitoring
# ============================================================================

def setup_realtime_monitoring():
    """
    Pattern 6: Set up real-time monitoring for specific platforms
    Useful for crisis management or campaign tracking
    """
    from social_media_scraper import TwitterScraper, InstagramScraper
    import time
    
    twitter = TwitterScraper("your_handle")
    instagram = InstagramScraper("your_handle")
    
    def monitor_engagement():
        """Monitor engagement in real-time"""
        
        twitter_profile = twitter.scrape_profile()
        instagram_profile = instagram.scrape_profile()
        
        print(f"\n[LIVE MONITOR] {time.strftime('%H:%M:%S')}")
        print(f"Twitter Followers: {twitter_profile.followers:,}")
        print(f"Instagram Followers: {instagram_profile.followers:,}")
        
        # Get latest posts
        twitter_posts = twitter.scrape_recent_posts(limit=3)
        insta_posts = instagram.scrape_recent_posts(limit=3)
        
        print(f"\nLatest Twitter Engagement:")
        for post in twitter_posts:
            print(f"  - {post.engagement_rate:.2f}% ({post.views:,} views)")
        
        print(f"\nLatest Instagram Engagement:")
        for post in insta_posts:
            print(f"  - {post.engagement_rate:.2f}% ({post.likes:,} likes)")
    
    # Run monitoring loop
    while True:
        monitor_engagement()
        time.sleep(300)  # Update every 5 minutes


# ============================================================================
# PATTERN 7: Data Export to CSV/Excel
# ============================================================================

def export_social_data_to_csv(intelligence_data):
    """
    Pattern 7: Export social media data to CSV format
    Useful for Excel analysis and reporting
    """
    import csv
    from pathlib import Path
    
    output_dir = Path("./exports")
    output_dir.mkdir(exist_ok=True)
    
    # Export posts data
    if intelligence_data.get("twitter_analytics"):
        twitter_posts = intelligence_data["twitter_analytics"].get("recent_posts", [])
        
        csv_file = output_dir / "twitter_posts.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'platform', 'author', 'content', 'views', 'likes', 
                'comments', 'engagement_rate', 'timestamp'
            ])
            writer.writeheader()
            
            for post in twitter_posts:
                writer.writerow({
                    'platform': post['platform'],
                    'author': post['author'],
                    'content': post['content'][:100],
                    'views': post['views'],
                    'likes': post['likes'],
                    'comments': post['comments'],
                    'engagement_rate': f"{post['engagement_rate']:.2f}%",
                    'timestamp': post['timestamp']
                })
        
        print(f"✓ Twitter posts exported to {csv_file}")
    
    # Similar exports for other platforms...
    
    return output_dir


# ============================================================================
# PATTERN 8: Custom Analytics Dashboard Data
# ============================================================================

def prepare_dashboard_data(intelligence_data):
    """
    Pattern 8: Prepare data formatted for dashboard visualization
    Returns structured data for charting libraries
    """
    
    dashboard = {
        "summary": {
            "total_followers": 0,
            "total_engagement": 0,
            "platforms": 0,
            "avg_engagement_rate": 0
        },
        "platforms": {},
        "trends": {
            "engagement_over_time": [],
            "follower_growth": [],
            "top_posts": []
        }
    }
    
    # Aggregate data
    engagement_rates = []
    
    for platform in ["twitter_analytics", "instagram_analytics", "linkedin_analytics"]:
        if platform in intelligence_data and intelligence_data[platform]:
            data = intelligence_data[platform]
            
            dashboard["summary"]["total_followers"] += data.get("total_followers", 0)
            dashboard["summary"]["total_engagement"] += data.get("total_engagement", 0)
            dashboard["summary"]["platforms"] += 1
            engagement_rates.append(data.get("average_engagement_rate", 0))
            
            platform_name = platform.replace("_analytics", "")
            dashboard["platforms"][platform_name] = {
                "followers": data.get("total_followers", 0),
                "engagement_rate": data.get("average_engagement_rate", 0),
                "posting_frequency": data.get("posting_frequency", 0),
                "posts_analyzed": len(data.get("recent_posts", []))
            }
    
    if engagement_rates:
        dashboard["summary"]["avg_engagement_rate"] = sum(engagement_rates) / len(engagement_rates)
    
    return dashboard


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("SOCIAL MEDIA SCRAPER - INTEGRATION PATTERNS")
    print("=" * 80)
    
    # Example 1: Simple integration
    print("\n1. Simple Integration")
    print("-" * 80)
    print("See integrate_with_main() function")
    
    # Example 2: Batch processing
    print("\n2. Batch Processing Multiple Businesses")
    print("-" * 80)
    businesses = [
        {"name": "Company A", "twitter": "companya", "instagram": "company_a"},
        {"name": "Company B", "twitter": "companyb", "instagram": "company_b"},
    ]
    print(f"Would process {len(businesses)} businesses")
    
    # Example 3: Scheduled scraping
    print("\n3. Scheduled Scraping")
    print("-" * 80)
    print("Would run scraping every 24 hours")
    
    print("\n" + "=" * 80)
