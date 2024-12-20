import os
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from hn_fetcher import fetch_top_stories
from database import init_db, save_articles, export_to_excel

load_dotenv()

def main():
    print("HackerNews Fetcher Started!")
    
    # Delete existing database if it exists
    if os.path.exists('hackernews.db'):
        print("Removing old database...")
        os.remove('hackernews.db')
    
    # Initialize the database
    init_db()
    
    def fetch_articles():
        print(f"\nFetching articles at {datetime.now()}")
        articles = fetch_top_stories(limit=10)  # Get top 10 stories
        save_articles(articles)
        print("Articles fetched and saved!")
        
        # Export to Excel
        excel_file = export_to_excel()
        print(f"Articles exported to Excel: {excel_file}")
        
        # Print the latest articles
        for article in articles:
            print(f"\nTitle: {article['title']}")
            print(f"URL: {article['url']}")
            print("-" * 50)

    # Schedule the job to run daily at 9 AM
    schedule.every().day.at("09:00").do(fetch_articles)
    
    # Run once immediately when starting
    fetch_articles()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
