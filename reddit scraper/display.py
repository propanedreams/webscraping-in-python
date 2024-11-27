import sqlite3
import csv
import os

DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "reddit_data.db")

def display_posts():
    """Display all posts stored in the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve all posts
    cursor.execute("SELECT * FROM reddit_posts")
    rows = cursor.fetchall()

    if not rows:
        print("No posts found in the database.")
    else:
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Subreddit: {row[2]}")
            print(f"Score: {row[3]}")
            print(f"Comments: {row[4]}")
            print(f"Sentiment: {row[5]:.2f}")
            print("-" * 50)

    conn.close()

def export_to_csv():
    """Export all posts to a CSV file."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Retrieve all posts
    cursor.execute("SELECT * FROM reddit_posts")
    rows = cursor.fetchall()

    if not rows:
        print("No posts found in the database. CSV not created.")
        return

    # Export to CSV
    with open("reddit_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "Subreddit", "Score", "Comments", "Sentiment"])  # Column headers
        writer.writerows(rows)

    print("Data exported to reddit_posts.csv.")
    conn.close()

if __name__ == "__main__":
    print("1. Display posts")
    print("2. Export posts to CSV")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        display_posts()
    elif choice == "2":
        export_to_csv()
    else:
        print("Invalid choice.")
