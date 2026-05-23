import os
import sqlite3

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
DB_PATH = os.path.join(DB_DIR, 'inven_pulse.db')

def get_db_connection():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    # Create posts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT PRIMARY KEY,
            game_name TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT,
            author TEXT,
            view_count INTEGER,
            upvotes INTEGER,
            content_snippet TEXT,
            category TEXT,
            sentiment_score REAL,
            reasoning TEXT,
            churn_risk BOOLEAN,
            churn_trigger TEXT,
            loyalty_signal BOOLEAN,
            loyalty_trigger TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
