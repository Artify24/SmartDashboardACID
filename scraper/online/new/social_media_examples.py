"""
Social Media Intelligence Integration Examples
Shows how to use the social media scraper with the main application
"""

from social_media_scraper import (
    SocialMediaIntelligenceScraper,
    scrape_social_media,
    TwitterScraper,
    InstagramScraper,
    RedditScraper,
    LinkedInScraper
)
from utils import setup_logger
import json
from pathlib import Path

logger = setup_logger(__name__)


def example_1_basic_scraping():
    """
    Example 1: Basic social media scraping
    Scrape all platforms for a business
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 1: Basic Social Media Scraping")
    logger.info("=" * 80)
    
    scraper = SocialMediaIntelligenceScraper()
    
    # Scrape all platforms
    intelligence = scraper.scrape_all_platforms(
        business_name="Acme Corporation",
        twitter_handle="acmecorp",
        instagram_handle="acmecorp_official",
        reddit_handle="acmecorp",
        linkedin_company="Acme Corporation",
        post_limit=10
    )
    
    # Generate report
    report = scraper.generate_business_analysis_report(intelligence)
    print(report)
    
    # Save data
    output_file = Path("./social_media_data/acme_intelligence.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(intelligence.to_dict(), f, indent=2, default=str)
    
    logger.info(f"Data saved to {output_file}")


def example_2_single_platform():
    """
    Example 2: Scrape a single platform in detail
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 2: Single Platform Deep Dive")
    logger.info("=" * 80)
    
    # Scrape only Twitter
    twitter_scraper = TwitterScraper("techcrunch")
    profile = twitter_scraper.scrape_profile()
    
    if profile:
        logger.info(f"\nProfile: {profile.display_name}")
        logger.info(f"Followers: {profile.followers:,}")
        logger.info(f"URL: {profile.profile_url}")
        
        # Get recent posts
        posts = twitter_scraper.scrape_recent_posts(limit=10)
        analytics = twitter_scraper.calculate_analytics(profile, posts)
        
        logger.info(f"\nAnalytics:")
        logger.info(f"Average Engagement Rate: {analytics.average_engagement_rate:.2f}%")
        logger.info(f"Posting Frequency: {analytics.posting_frequency:.2f} posts/day")
        logger.info(f"Total Engagement: {analytics.total_engagement:,}")
        
        if analytics.best_post:
            logger.info(f"Best Post Engagement: {analytics.best_post.engagement_rate:.2f}%")
        if analytics.worst_post:
            logger.info(f"Worst Post Engagement: {analytics.worst_post.engagement_rate:.2f}%")


def example_3_competitor_analysis():
    """
    Example 3: Compare multiple competitors
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 3: Competitor Analysis")
    logger.info("=" * 80)
    
    competitors = [
        {"name": "Company A", "twitter": "companya", "instagram": "company_a"},
        {"name": "Company B", "twitter": "companyb", "instagram": "company_b"},
        {"name": "Company C", "twitter": "companyc", "instagram": "company_c"},
    ]
    
    scraper = SocialMediaIntelligenceScraper()
    all_data = []
    
    for competitor in competitors:
        logger.info(f"\nAnalyzing {competitor['name']}...")
        
        intelligence = scraper.scrape_all_platforms(
            business_name=competitor['name'],
            twitter_handle=competitor.get('twitter'),
            instagram_handle=competitor.get('instagram'),
            post_limit=10
        )
        
        all_data.append(intelligence.to_dict())
    
    # Save comparison data
    comparison_file = Path("./social_media_data/competitor_comparison.json")
    comparison_file.parent.mkdir(parents=True, exist_ok=True)
    with open(comparison_file, "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    
    logger.info(f"\nComparison data saved to {comparison_file}")


def example_4_instagram_specific():
    """
    Example 4: Deep dive into Instagram metrics
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 4: Instagram Performance Analysis")
    logger.info("=" * 80)
    
    instagram_scraper = InstagramScraper("instagram")
    profile = instagram_scraper.scrape_profile()
    
    if profile:
        logger.info(f"\nProfile: {profile.display_name}")
        logger.info(f"Bio: {profile.bio}")
        logger.info(f"Followers: {profile.followers:,}")
        logger.info(f"Following: {profile.following:,}")
        logger.info(f"Total Posts: {profile.total_posts:,}")
        logger.info(f"Verified: {profile.verification_status}")
        
        posts = instagram_scraper.scrape_recent_posts(limit=10)
        
        logger.info(f"\nRecent Posts Performance:")
        for i, post in enumerate(posts, 1):
            logger.info(f"Post {i}: {post.likes:,} likes, {post.comments} comments, "
                       f"Engagement: {post.engagement_rate:.2f}%")


def example_5_linkedin_business_intel():
    """
    Example 5: LinkedIn business intelligence
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 5: LinkedIn Business Intelligence")
    logger.info("=" * 80)
    
    linkedin_scraper = LinkedInScraper("Microsoft")
    profile = linkedin_scraper.scrape_profile()
    
    if profile:
        logger.info(f"\nCompany: {profile.display_name}")
        logger.info(f"Followers: {profile.followers:,}")
        logger.info(f"URL: {profile.profile_url}")
        
        posts = linkedin_scraper.scrape_recent_posts(limit=10)
        analytics = linkedin_scraper.calculate_analytics(profile, posts)
        
        logger.info(f"\nContent Performance:")
        logger.info(f"Total Posts Analyzed: {len(posts)}")
        logger.info(f"Average Views: {analytics.average_views:,.0f}")
        logger.info(f"Average Engagement: {analytics.average_engagement_rate:.2f}%")
        logger.info(f"Posting Frequency: {analytics.posting_frequency:.2f} posts/day")


def example_6_reddit_community_analysis():
    """
    Example 6: Reddit community analysis
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 6: Reddit Community Analysis")
    logger.info("=" * 80)
    
    reddit_scraper = RedditScraper("techsupport")
    
    posts = reddit_scraper.scrape_recent_posts(limit=10)
    
    logger.info(f"\nRecent Reddit Posts:")
    for i, post in enumerate(posts, 1):
        logger.info(f"Post {i}: {post.views:,} upvotes, {post.comments} comments")
        logger.info(f"  Content: {post.content[:60]}...")
        logger.info(f"  Engagement: {post.engagement_rate:.2f}%\n")


def example_7_full_pipeline():
    """
    Example 7: Complete pipeline from scraping to analysis
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 7: Complete Pipeline")
    logger.info("=" * 80)
    
    # Scrape
    intelligence_data = scrape_social_media(
        business_name="TechStartup",
        twitter_handle="techstartup",
        instagram_handle="techstartup_io",
        reddit_handle="techstartup",
        linkedin_company="TechStartup Inc",
        post_limit=10,
        output_dir="./social_media_data/techstartup"
    )
    
    logger.info("✅ Pipeline completed successfully!")


def example_8_custom_analysis():
    """
    Example 8: Custom analysis on scraped data
    """
    logger.info("=" * 80)
    logger.info("EXAMPLE 8: Custom Analytics")
    logger.info("=" * 80)
    
    scraper = SocialMediaIntelligenceScraper()
    
    intelligence = scraper.scrape_all_platforms(
        business_name="DataAnalyticsInc",
        twitter_handle="dataanalytics",
        instagram_handle="data_analytics_inc",
        post_limit=10
    )
    
    # Custom analysis
    logger.info("\nCustom Analysis:")
    
    # Total reach across platforms
    total_followers = 0
    if intelligence.twitter_analytics:
        total_followers += intelligence.twitter_analytics.total_followers
    if intelligence.instagram_analytics:
        total_followers += intelligence.instagram_analytics.total_followers
    if intelligence.linkedin_analytics:
        total_followers += intelligence.linkedin_analytics.total_followers
    
    logger.info(f"Total Reach (Followers): {total_followers:,}")
    
    # Most engaging platform
    platforms_engagement = []
    if intelligence.twitter_analytics:
        platforms_engagement.append(
            ("Twitter", intelligence.twitter_analytics.average_engagement_rate)
        )
    if intelligence.instagram_analytics:
        platforms_engagement.append(
            ("Instagram", intelligence.instagram_analytics.average_engagement_rate)
        )
    if intelligence.linkedin_analytics:
        platforms_engagement.append(
            ("LinkedIn", intelligence.linkedin_analytics.average_engagement_rate)
        )
    
    if platforms_engagement:
        most_engaging = max(platforms_engagement, key=lambda x: x[1])
        logger.info(f"Most Engaging Platform: {most_engaging[0]} ({most_engaging[1]:.2f}% avg engagement)")


if __name__ == "__main__":
    # Run examples
    print("\n🌐 SOCIAL MEDIA INTELLIGENCE SCRAPER - EXAMPLES\n")
    
    # Uncomment examples to run them
    # example_1_basic_scraping()
    # example_2_single_platform()
    # example_3_competitor_analysis()
    # example_4_instagram_specific()
    # example_5_linkedin_business_intel()
    # example_6_reddit_community_analysis()
    # example_7_full_pipeline()
    # example_8_custom_analysis()
    
    # Run full pipeline by default
    example_7_full_pipeline()
