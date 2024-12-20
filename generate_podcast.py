import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from podcastfy.client import generate_podcast
from datetime import datetime 

def read_urls_from_excel(excel_file_path):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path)
        
        # Find columns that might contain URLs
        url_columns = [col for col in df.columns if 'url' in col.lower()]
        
        if not url_columns:
            print("No columns containing 'url' found in the Excel file.")
            print("Available columns:", df.columns.tolist())
            return []
        
        all_urls = []
        # Collect URLs from each relevant column
        for column in url_columns:
            # Get URLs, skipping empty or NaN values
            urls = df[column].dropna().tolist()
            all_urls.extend(urls)
        
        # Get first 3 URLs
        first_three_urls = all_urls[:10]
        
        # Print for verification
        print("\nFirst 3 URLs:")
        print("-" * 50)
        for i, url in enumerate(first_three_urls, 1):
            print(f"{i}. {url}")
            
        # return first_three_urls
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []
    return first_three_urls
    

if __name__ == "__main__":
    # Replace this with your Excel file path
    excel_file = "exports/hackernews_articles.xlsx"
    urls_list = read_urls_from_excel(excel_file)
    print(f"\nStored URLs list: {urls_list}") 
    conversation_config = {
    "podcast_name": "Hacker News Podcast",
   }
    
    audio_file = generate_podcast(urls=urls_list, tts_model="gemini", conversation_config=conversation_config)
    if audio_file:
        print(f"\nPodcast saved")
    else:
        print("\nNo audio file was generated")