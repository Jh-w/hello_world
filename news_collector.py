"""
News Collector Module
Collects information about "AI Sports Coach" and "AI Health Assistant" from multiple sources
"""

import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class NewsCollector:
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.bing_search_key = os.getenv('BING_SEARCH_KEY')
        self.results_per_query = int(os.getenv('RESULTS_PER_QUERY', 15))
        self.news_items = []
        
        # Search keywords in multiple languages
        self.keywords = {
            'AI Sports Coach': [
                'AI sports coach',
                'artificial intelligence fitness trainer',
                'AI personal trainer',
                '智能运动教练',
                'AI运动教练'
            ],
            'AI Health Assistant': [
                'AI health assistant',
                'artificial intelligence healthcare',
                'AI medical assistant',
                '智能健康助手',
                'AI健康助手'
            ]
        }
        
        # RSS feeds related to AI and health/fitness
        self.rss_feeds = [
            'https://feeds.reuters.com/reuters/technologyNews',
            'https://feeds.bloomberg.com/markets/news.rss',
            'https://www.techcrunch.com/feed/',
            'https://feeds.arstechnica.com/arstechnica/index',
            'https://feeds.nature.com/nbt/current_issue',
        ]
    
    def collect_from_newsapi(self) -> List[Dict]:
        """Collect news from NewsAPI"""
        articles = []
        
        if not self.news_api_key:
            print("Warning: NEWS_API_KEY not configured")
            return articles
        
        try:
            for category_name, keywords in self.keywords.items():
                for keyword in keywords:
                    url = 'https://newsapi.org/v2/everything'
                    params = {
                        'q': keyword,
                        'sortBy': 'publishedAt',
                        'language': 'en',
                        'pageSize': self.results_per_query,
                        'apiKey': self.news_api_key
                    }
                    
                    response = requests.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        for article in data.get('articles', []):
                            articles.append({
                                'source': 'NewsAPI',
                                'category': category_name,
                                'title': article.get('title'),
                                'description': article.get('description'),
                                'url': article.get('url'),
                                'image': article.get('urlToImage'),
                                'published_at': article.get('publishedAt'),
                                'source_name': article.get('source', {}).get('name')
                            })
        except requests.exceptions.RequestException as e:
            print(f"Error collecting from NewsAPI: {e}")
        
        return articles
    
    def collect_from_rss_feeds(self) -> List[Dict]:
        """Collect news from RSS feeds"""
        articles = []
        keywords_flat = [k for keywords in self.keywords.values() for k in keywords]
        
        try:
            for feed_url in self.rss_feeds:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:self.results_per_query]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    content = (title + ' ' + summary).lower()
                    
                    # Check if article matches keywords
                    matched_category = None
                    for category_name, keywords in self.keywords.items():
                        if any(keyword.lower() in content for keyword in keywords):
                            matched_category = category_name
                            break
                    
                    if matched_category:
                        articles.append({
                            'source': 'RSS Feed',
                            'category': matched_category,
                            'title': title,
                            'description': summary,
                            'url': entry.get('link', ''),
                            'image': None,
                            'published_at': entry.get('published', ''),
                            'source_name': feed.feed.get('title', 'Unknown')
                        })
        except Exception as e:
            print(f"Error collecting from RSS feeds: {e}")
        
        return articles
    
    def collect_from_google_news(self) -> List[Dict]:
        """Collect news using Google News RSS (no API key required)"""
        articles = []
        
        try:
            for category_name, keywords in self.keywords.items():
                for keyword in keywords:
                    # Google News RSS feed
                    feed_url = f'https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en'
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:self.results_per_query]:
                        articles.append({
                            'source': 'Google News',
                            'category': category_name,
                            'title': entry.get('title', ''),
                            'description': entry.get('summary', ''),
                            'url': entry.get('link', ''),
                            'image': None,
                            'published_at': entry.get('published', ''),
                            'source_name': 'Google News'
                        })
        except Exception as e:
            print(f"Error collecting from Google News: {e}")
        
        return articles
    
    def collect_all(self) -> List[Dict]:
        """Collect news from all sources"""
        all_articles = []
        
        print("Collecting news from Google News...")
        all_articles.extend(self.collect_from_google_news())
        
        if self.news_api_key:
            print("Collecting news from NewsAPI...")
            all_articles.extend(self.collect_from_newsapi())
        
        print("Collecting news from RSS feeds...")
        all_articles.extend(self.collect_from_rss_feeds())
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        for article in all_articles:
            if article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_articles.append(article)
        
        # Sort by published date and limit to ~30 items
        unique_articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        
        return unique_articles[:30]


if __name__ == '__main__':
    collector = NewsCollector()
    articles = collector.collect_all()
    
    print(f"\nCollected {len(articles)} articles:")
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Category: {article['category']}")
        print(f"   Source: {article['source_name']}")
        print(f"   URL: {article['url']}")
