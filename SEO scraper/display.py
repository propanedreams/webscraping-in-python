import os
import sqlite3

# Database path
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "seo_data.db")

def display_data():
    """Retrieve and display all SEO data from the SQLite database."""
    # Check if the database exists
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}. Run the scraper first to create the database.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query to retrieve all data
    cursor.execute("SELECT * FROM seo_data")
    rows = cursor.fetchall()

    # Display the results
    if not rows:
        print("No data found in the database.")
    else:
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"URL: {row[1]}")
            print(f"Canonical URL: {row[2]}")
            print(f"Meta Description: {row[3]}")
            print(f"Meta Keywords: {row[4]}")
            print(f"Open Graph Title: {row[5]}")
            print(f"Open Graph Description: {row[6]}")
            print(f"Open Graph URL: {row[7]}")
            print(f"Twitter Title: {row[8]}")
            print(f"Twitter Description: {row[9]}")
            print(f"Twitter URL: {row[10]}")
            print(f"Alternate Links: {row[11]}")
            print(f"Internal Links: {row[12]}")
            print(f"External Links: {row[13]}")
            print("-" * 50)

    # Close the database connection
    conn.close()

# Call the display function
display_data()
