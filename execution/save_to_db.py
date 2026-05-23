import os
import json
import sys

# Add parent dir to path to import server.db
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from server.db import get_db_connection, init_db

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
INPUT_FILE = os.path.join(TMP_DIR, 'analyzed_results.json')

def save_to_db():
    init_db()
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("No data to save.")
        return

    conn = get_db_connection()
    c = conn.cursor()

    saved_count = 0
    for post in data:
        try:
            c.execute('''
                INSERT OR REPLACE INTO posts 
                (post_id, game_name, title, url, author, view_count, upvotes, 
                 content_snippet, category, sentiment_score, reasoning, 
                 churn_risk, churn_trigger, loyalty_signal, loyalty_trigger)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                post.get('post_id'), post.get('game_name'), post.get('title'), post.get('url'),
                post.get('author'), post.get('view_count', 0), post.get('upvotes', 0),
                post.get('content_snippet', ''), post.get('category', 'Other'),
                post.get('sentiment_score', 0.0), post.get('reasoning', ''),
                int(post.get('churn_risk', False)), post.get('churn_trigger', ''),
                int(post.get('loyalty_signal', False)), post.get('loyalty_trigger', '')
            ))
            saved_count += 1
        except Exception as e:
            print(f"Error saving post {post.get('post_id')}: {e}")

    conn.commit()
    conn.close()
    print(f"Successfully saved {saved_count} posts to SQLite database.")

if __name__ == "__main__":
    save_to_db()
