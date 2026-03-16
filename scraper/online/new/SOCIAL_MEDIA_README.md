# Social Media Intelligence Scraper

A comprehensive Python tool for scraping and analyzing social media data across multiple platforms (Twitter, Instagram, Reddit, LinkedIn) for business intelligence.

## 📊 Features

### Platforms Supported
- **Twitter/X** - Extract tweets, engagement metrics, follower counts
- **Instagram** - Scrape posts, likes, comments, engagement rates
- **Reddit** - Collect community posts and discussion metrics
- **LinkedIn** - Company profile data and content analytics

### Data Collected Per Platform

#### Profile Information
- Username/Handle
- Followers count
- Following count (where available)
- Total posts
- Verification status
- Bio/Description
- Profile URL
- Profile image

#### Recent Posts (Default: Last 10 Posts)
- Post ID and content
- Timestamp
- Views/Impressions
- Likes/Reactions
- Comments count
- Shares count
- Engagement rate (calculated)
- Post URL

#### Analytics
- Posting frequency (posts per day)
- Average engagement rate
- Average views per post
- Average comments
- Best performing post
- Worst performing post
- Total engagement across recent posts
- Audience growth (where available)

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from social_media_scraper import scrape_social_media

# Scrape all platforms for a business
data = scrape_social_media(
    business_name="TechCorp",
    twitter_handle="techcorp",
    instagram_handle="techcorp_official",
    reddit_handle="techcorp",
    linkedin_company="TechCorp Inc",
    post_limit=10,
    output_dir="./social_media_data"
)
```

### Command Line Usage

```bash
# Using the social_media_examples.py
python social_media_examples.py

# Or run specific examples
python -c "from social_media_examples import example_1_basic_scraping; example_1_basic_scraping()"
```

## 📝 Usage Examples

### Example 1: Basic Multi-Platform Scraping

```python
from social_media_scraper import SocialMediaIntelligenceScraper

scraper = SocialMediaIntelligenceScraper()

intelligence = scraper.scrape_all_platforms(
    business_name="Acme Corporation",
    twitter_handle="acmecorp",
    instagram_handle="acmecorp_official",
    reddit_handle="acmecorp",
    linkedin_company="Acme Corporation",
    post_limit=10
)

# Generate comprehensive report
report = scraper.generate_business_analysis_report(intelligence)
print(report)
```

### Example 2: Single Platform Analysis

```python
from social_media_scraper import TwitterScraper

scraper = TwitterScraper("techcrunch")
profile = scraper.scrape_profile()
posts = scraper.scrape_recent_posts(limit=10)
analytics = scraper.calculate_analytics(profile, posts)

print(f"Followers: {profile.followers:,}")
print(f"Avg Engagement Rate: {analytics.average_engagement_rate:.2f}%")
```

### Example 3: Competitor Analysis

```python
from social_media_scraper import SocialMediaIntelligenceScraper
import json

scraper = SocialMediaIntelligenceScraper()
competitors = ["competitor1", "competitor2", "competitor3"]

all_data = []
for handle in competitors:
    intel = scraper.scrape_all_platforms(
        business_name=handle,
        twitter_handle=handle
    )
    all_data.append(intel.to_dict())

# Save comparison
with open("competitor_comparison.json", "w") as f:
    json.dump(all_data, f, indent=2)
```

### Example 4: Instagram Deep Dive

```python
from social_media_scraper import InstagramScraper

scraper = InstagramScraper("instagram")
profile = scraper.scrape_profile()
posts = scraper.scrape_recent_posts(limit=10)

print(f"Profile: {profile.display_name}")
print(f"Followers: {profile.followers:,}")
print(f"Total Posts: {profile.total_posts:,}")

for post in posts:
    print(f"Post: {post.likes} likes, {post.comments} comments")
```

### Example 5: LinkedIn Business Intelligence

```python
from social_media_scraper import LinkedInScraper

scraper = LinkedInScraper("Microsoft")
profile = scraper.scrape_profile()
posts = scraper.scrape_recent_posts(limit=10)
analytics = scraper.calculate_analytics(profile, posts)

print(f"Company: {profile.display_name}")
print(f"Followers: {analytics.total_followers:,}")
print(f"Avg Engagement: {analytics.average_engagement_rate:.2f}%")
```

## 📊 Output Format

### Console Report
```
================================================================================
SOCIAL MEDIA BUSINESS INTELLIGENCE REPORT
Business: TechCorp
Report Generated: 2025-12-25 14:30:00
================================================================================

📱 TWITTER ANALYSIS
--------------------------------------------------------------------------------
Handle: @techcorp
Followers: 125,000
Total Posts Analyzed: 10
Posting Frequency: 2.50 posts/day
Average Engagement Rate: 5.25%
Average Views per Post: 50,000
Average Comments per Post: 250
Total Engagement: 20,000

📸 INSTAGRAM ANALYSIS
...
```

### JSON Output

```json
{
  "business_name": "TechCorp",
  "scrape_timestamp": 1703512200.5,
  "twitter_profile": {
    "platform": "twitter",
    "username": "techcorp",
    "followers": 125000,
    ...
  },
  "twitter_analytics": {
    "platform": "twitter",
    "total_followers": 125000,
    "average_engagement_rate": 5.25,
    "posting_frequency": 2.5,
    ...
  }
}
```

## 🔧 API Integration (Optional)

For real data instead of simulated data, integrate with official APIs:

### Twitter API v2
```python
twitter_scraper = TwitterScraper("username", api_key="YOUR_API_KEY")
```

### Instagram API
```python
instagram_scraper = InstagramScraper("username", api_key="YOUR_API_KEY")
```

### Reddit API
```python
reddit_scraper = RedditScraper("username", api_key="YOUR_API_KEY")
```

### LinkedIn API
```python
linkedin_scraper = LinkedInScraper("company_name", api_key="YOUR_API_KEY")
```

## 📈 Business Intelligence Metrics

The scraper calculates the following metrics:

### Engagement Rate
```
Engagement Rate = ((Likes + Comments + Shares) / Views) × 100
```

### Posting Frequency
```
Posts per Day = (Number of Posts / 30)
```

### Performance Analysis
- Best performing post (highest engagement)
- Worst performing post (lowest engagement)
- Average metrics across all posts
- Total engagement across all posts

## 🛠️ Data Models

### SocialPost
```python
@dataclass
class SocialPost:
    platform: str
    post_id: str
    author: str
    content: str
    timestamp: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    engagement_rate: float = 0.0
    url: str = ""
```

### SocialProfile
```python
@dataclass
class SocialProfile:
    platform: str
    username: str
    display_name: str = ""
    bio: str = ""
    followers: int = 0
    following: int = 0
    total_posts: int = 0
    verification_status: bool = False
    profile_url: str = ""
    profile_image: str = ""
```

### SocialAnalytics
```python
@dataclass
class SocialAnalytics:
    platform: str
    total_followers: int = 0
    total_engagement: int = 0
    average_engagement_rate: float = 0.0
    posting_frequency: float = 0.0
    most_engaging_content_type: str = ""
    recent_posts: List[SocialPost] = field(default_factory=list)
    best_post: Optional[SocialPost] = None
    worst_post: Optional[SocialPost] = None
    average_views: float = 0.0
    average_comments: float = 0.0
    audience_growth: float = 0.0
```

## 🔐 Best Practices

1. **Rate Limiting**: Implement delays between API calls to avoid hitting rate limits
2. **API Keys**: Store API keys in environment variables, not in code
3. **Error Handling**: Always handle exceptions for failed API calls
4. **Data Validation**: Validate and clean data before analysis
5. **Privacy**: Respect platform terms of service and user privacy
6. **Caching**: Cache results to minimize API calls

## 📋 File Structure

```
social_media_scraper.py          # Main scraper module
social_media_examples.py          # Usage examples
README.md                         # This file
requirements.txt                  # Python dependencies
```

## 🚧 Future Enhancements

- [ ] TikTok integration
- [ ] YouTube analytics
- [ ] Sentiment analysis
- [ ] Hashtag tracking
- [ ] Influencer identification
- [ ] Content recommendation
- [ ] Predictive analytics
- [ ] Real-time monitoring
- [ ] Advanced filtering and search
- [ ] Export to CSV/Excel

## ⚠️ Limitations & Notes

- Some data requires official API authentication
- Current implementation provides simulated data for demonstration
- Actual API integration requires platform-specific credentials
- Rate limits apply per platform
- Data accuracy depends on platform API accuracy

## 📞 Support

For issues or questions:
1. Check the examples in `social_media_examples.py`
2. Review the data models in the code comments
3. Ensure API keys are properly configured (if using APIs)
4. Check platform-specific rate limits and restrictions

## 📄 License

This tool is provided as-is for business intelligence purposes.

## 🙏 Acknowledgments

Built using:
- Python requests library for HTTP calls
- Selenium for web scraping capabilities
- Official platform APIs (when configured)

---

**Last Updated**: December 2025
**Version**: 1.0.0
