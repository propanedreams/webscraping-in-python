import sqlite3
import os

# Database path
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "news_details.db")
print(DB_PATH)
def display_news():
    """Display all news articles stored in the SQLite database."""
    # Check if the database exists
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Make sure to scrape news first.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve all news articles
    cursor.execute("SELECT * FROM news")
    rows = cursor.fetchall()

    if not rows:
        print("No news articles found in the database.")
    else:
        print(f"{'ID':<5} {'Headline':<50} {'Description':<70} {'Last Updated':<15} {'Category':<15} {'Site':<30}")
        print("-" * 150)
        for row in rows:
            # Replace None values with "N/A" for better readability
            id = row[0]
            headline = row[1] or "N/A"
            description = row[2] or "N/A"
            last_updated = row[3] or "N/A"
            category = row[4] or "N/A"
            site = row[5] or "N/A"
            print(f"{id:<5} {headline:<50} {description:<70} {last_updated:<15} {category:<15} {site:<30}")

    # Close the database connection
    conn.close()