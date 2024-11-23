import os
import sqlite3
import requests
from bs4 import BeautifulSoup

# Create the database folder and initialize SQLite
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "scraped_data.db")

def initialize_db():
    # Ensure the db folder exists
    os.makedirs(DB_FOLDER, exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing scraped data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            title TEXT,
            meta_description TEXT,
            headings TEXT,
            links TEXT,
            images TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(url, title, meta_description, headings, links, images):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert scraped data into the database
    cursor.execute('''
        INSERT INTO scraped_data (url, title, meta_description, headings, links, images)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        url,
        title,
        meta_description,
        "\n".join(headings),      # Save headings as newline-separated string
        "\n".join(links),         # Save links as newline-separated string
        "\n".join(images)         # Save images as newline-separated string
    ))
    conn.commit()
    conn.close()

def scrape_generic_info(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve content: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract page title
    title = soup.title.string if soup.title else "No title found"

    # Extract meta description
    meta_description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_description = meta["content"]
    else:
        meta_description = "No meta description found"

    # Extract all headings (h1, h2, h3)
    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]

    # Extract all links
    links = [a['href'] for a in soup.find_all("a", href=True)]

    # Extract all image URLs
    images = [img['src'] for img in soup.find_all("img", src=True)]

    # Print the results (optional for debugging)
    print(f"Title: {title}")
    print(f"Meta Description: {meta_description}")
    print(f"Headings: {headings}")
    print(f"Links: {links[:5]}")  # Show first 5 links
    print(f"Images: {images[:5]}")  # Show first 5 images

    # Save the results to the database
    save_to_db(url, title, meta_description, headings, links, images)
    print("Data saved to database.")

# Initialize the database
initialize_db()

# URL to scrape
url = "https://google.com"

# Call the scraper function
scrape_generic_info(url)
