import os
import sqlite3
import requests
from bs4 import BeautifulSoup

# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "seo_data.db")

def initialize_db():
    """Initialize the SQLite database and create the table."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table to store SEO data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seo_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            canonical_url TEXT,
            meta_description TEXT,
            meta_keywords TEXT,
            og_title TEXT,
            og_description TEXT,
            og_url TEXT,
            twitter_title TEXT,
            twitter_description TEXT,
            twitter_url TEXT,
            alternate_links TEXT,
            internal_links TEXT,
            external_links TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(data):
    """Save scraped SEO data to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO seo_data (
            url, canonical_url, meta_description, meta_keywords,
            og_title, og_description, og_url,
            twitter_title, twitter_description, twitter_url,
            alternate_links, internal_links, external_links
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["url"], data["canonical_url"], data["meta_description"], data["meta_keywords"],
        data["og_title"], data["og_description"], data["og_url"],
        data["twitter_title"], data["twitter_description"], data["twitter_url"],
        "\n".join(data["alternate_links"]),
        "\n".join(data["internal_links"]),
        "\n".join(data["external_links"]),
    ))
    conn.commit()
    conn.close()

def scrape_seo_info(url):
    """Scrape SEO data from the given URL."""
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract canonical link
    canonical = soup.find("link", rel="canonical")
    canonical_url = canonical["href"] if canonical else "No canonical URL found"

    # Extract alternate hreflang links
    alternate_links = [
        f"{link.get('hreflang', 'unknown')}: {link['href']}"
        for link in soup.find_all("link", rel="alternate")
        if "hreflang" in link.attrs and "href" in link.attrs
    ]

    # Extract meta tags for SEO
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})

    # Extract Open Graph meta tags
    og_title = soup.find("meta", property="og:title")
    og_description = soup.find("meta", property="og:description")
    og_url = soup.find("meta", property="og:url")

    # Extract Twitter card meta tags
    twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
    twitter_description = soup.find("meta", attrs={"name": "twitter:description"})
    twitter_url = soup.find("meta", attrs={"name": "twitter:url"})

    # Extract internal and external links
    links = [a["href"] for a in soup.find_all("a", href=True)]
    internal_links = [link for link in links if url in link or link.startswith("/")]
    external_links = [link for link in links if not (url in link or link.startswith("/"))]

    # Prepare data for saving
    data = {
        "url": url,
        "canonical_url": canonical_url,
        "meta_description": meta_description["content"] if meta_description else "No description found",
        "meta_keywords": meta_keywords["content"] if meta_keywords else "No keywords found",
        "og_title": og_title["content"] if og_title else "No OG title found",
        "og_description": og_description["content"] if og_description else "No OG description found",
        "og_url": og_url["content"] if og_url else "No OG URL found",
        "twitter_title": twitter_title["content"] if twitter_title else "No Twitter title found",
        "twitter_description": twitter_description["content"] if twitter_description else "No Twitter description found",
        "twitter_url": twitter_url["content"] if twitter_url else "No Twitter URL found",
        "alternate_links": alternate_links,
        "internal_links": internal_links[:10],  # Limit to first 10 for brevity
        "external_links": external_links[:10],  # Limit to first 10 for brevity
    }

    # Save data to the database
    save_to_db(data)
    print(f"Data saved for URL: {url}")

# Initialize the database
initialize_db()

# URL to scrape
url = "https://nordicrace.dk/"

# Call the scraper
scrape_seo_info(url)
