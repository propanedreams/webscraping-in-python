import praw
from textblob import TextBlob
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "reddit_data.db")


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

def initialize_db():
    """Initialize the SQLite database and create the table."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing Reddit threads and comments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reddit_posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            subreddit TEXT NOT NULL,
            score INTEGER,
            num_comments INTEGER,
            sentiment REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reddit_comments (
            id TEXT PRIMARY KEY,
            post_id TEXT NOT NULL,
            body TEXT,
            sentiment REAL,
            FOREIGN KEY (post_id) REFERENCES reddit_posts (id)
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(posts, comments):
    """Save Reddit posts and comments to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert posts into the database
    for post in posts:
        cursor.execute('''
            INSERT OR IGNORE INTO reddit_posts (id, title, subreddit, score, num_comments, sentiment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (post['id'], post['title'], post['subreddit'], post['score'], post['num_comments'], post['sentiment']))

    # Insert comments into the database
    for comment in comments:
        cursor.execute('''
            INSERT OR IGNORE INTO reddit_comments (id, post_id, body, sentiment)
            VALUES (?, ?, ?, ?)
        ''', (comment['id'], comment['post_id'], comment['body'], comment['sentiment']))

    conn.commit()
    conn.close()

def analyze_sentiment(text):
    """Analyze sentiment of a given text using TextBlob."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

def scrape_reddit(subreddit_name, keyword=None):
    """Scrape Reddit threads and comments from a specific subreddit."""
   # Configure Reddit API
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
)

    # Access subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch hot threads
    posts = []
    comments = []
    for submission in subreddit.hot(limit=10):  # Adjust limit for more threads
        if keyword and keyword.lower() not in submission.title.lower():
            continue  # Skip posts that don't match the keyword

        post_data = {
            "id": submission.id,
            "title": submission.title,
            "subreddit": submission.subreddit.display_name,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "sentiment": analyze_sentiment(submission.title)
        }
        posts.append(post_data)

        # Fetch comments for the post
        submission.comments.replace_more(limit=0)  # Avoid "MoreComments"
        for comment in submission.comments.list():
            comment_data = {
                "id": comment.id,
                "post_id": submission.id,
                "body": comment.body,
                "sentiment": analyze_sentiment(comment.body)
            }
            comments.append(comment_data)

    return posts, comments

# Main script
initialize_db()
subreddit = "tryhackme"  # Change to your target subreddit
keyword = "how to"  # Change or set to None to fetch all threads

print(f"Scraping subreddit: {subreddit} with keyword: {keyword}")
posts, comments = scrape_reddit(subreddit, keyword)

if posts:
    print(f"Found {len(posts)} posts and {len(comments)} comments.")
    save_to_db(posts, comments)
    print("Data saved to the database.")
else:
    print("No matching posts found.")


