import sqlite3
from datetime import datetime
import pandas as pd
import os

def init_db():
    """Initialize the database with the articles table"""
    conn = sqlite3.connect('hackernews.db')
    c = conn.cursor()
    
    # Create articles table with basic fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            score INTEGER,
            timestamp TEXT NOT NULL,
            hn_id INTEGER UNIQUE
        )
    ''')
    
    conn.commit()
    conn.close()

def save_articles(articles):
    """Save articles to the database"""
    conn = sqlite3.connect('hackernews.db')
    c = conn.cursor()
    
    current_time = datetime.now().isoformat()
    
    for article in articles:
        try:
            c.execute('''
                INSERT OR REPLACE INTO articles 
                (title, url, score, timestamp, hn_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['url'],
                article.get('score', 0),
                current_time,
                article.get('id')
            ))
        except sqlite3.Error as e:
            print(f"Error saving article {article['title']}: {e}")
    
    conn.commit()
    conn.close()

def get_latest_articles(limit=10):
    """Retrieve the most recent articles from the database"""
    conn = sqlite3.connect('hackernews.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT title, url, score, timestamp 
        FROM articles 
        ORDER BY timestamp DESC 
        LIMIT ?
    ''', (limit,))
    
    articles = c.fetchall()
    conn.close()
    
    return [{
        'title': article[0],
        'url': article[1],
        'score': article[2],
        'timestamp': article[3]
    } for article in articles]

def export_to_excel():
    """Export all articles from the database to an Excel file"""
    conn = sqlite3.connect('hackernews.db')
    
    # Read the SQL table into a pandas DataFrame
    df = pd.read_sql_query('''
        SELECT title, url, score, timestamp, hn_id
        FROM articles
        ORDER BY timestamp DESC
    ''', conn)
    
    # Create 'exports' directory if it doesn't exist
    os.makedirs('exports', exist_ok=True)
    
    # Generate filename with current timestamp
    #timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'exports/hackernews_articles.xlsx'
    
    # Export to Excel
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Data exported to {filename}")
    
    conn.close()
    return filename