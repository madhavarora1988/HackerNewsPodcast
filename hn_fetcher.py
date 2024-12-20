import requests
from typing import List, Dict
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_article_content(url: str) -> str:
    """Fetch and extract text content from article URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up text: remove extra newlines and spaces
        lines = (line.strip() for line in text.splitlines())
        text = ' '.join(line for line in lines if line)
        
        # Limit text length to avoid overwhelming the model
        return text[:8000]  # Limit to first 8000 characters
        
    except Exception as e:
        print(f"   Error fetching article content: {str(e)}")
        return ""

def fetch_top_stories(limit: int = 10) -> List[Dict]:
    """Fetch top stories from Hacker News API"""
    
    print("\n=== Fetching Stories from Hacker News ===")
    
    # Get top story IDs
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()[:limit]
    
    articles = []
    for i, story_id in enumerate(story_ids, 1):
        # Get story details
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story = requests.get(story_url).json()
        
        # Only include stories with URLs
        if 'url' in story:
            print(f"\n{i}. Story Found:")
            print(f"   Title: {story.get('title')}")
            print(f"   URL: {story.get('url')}")
            print(f"   Score: {story.get('score')}")
            print("   Fetching article content...")
            
            content = get_article_content(story.get('url'))
            
            article = {
                'title': story.get('title'),
                'url': story.get('url'),
                'score': story.get('score'),
                'timestamp': story.get('time'),
                'content': content
            }
            articles.append(article)
            
        # Be nice to the API
        time.sleep(0.1)
    
    return articles 