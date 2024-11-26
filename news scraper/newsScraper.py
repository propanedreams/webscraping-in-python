import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "news_details.db")

def get_todays_datetime():
    """Return today's date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS



def initialize_db():
    """Initialize the SQLite database and create the table."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing news details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT NOT NULL,
            description TEXT,
            last_updated TEXT,
            category TEXT,
            site TEXT NOT NULL, 
            scrapetime TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(news_list, site, scrapetime):
    """Save a list of news details to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert news details into the database
    for news in news_list:
        cursor.execute('''
            INSERT INTO news (headline, description, last_updated, category, site, scrapetime)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (news['headline'], news['description'], news['last_updated'], news['category'], site, scrapetime))

    conn.commit()
    conn.close()

def scrape_bbc_news():
    """Scrape detailed news from BBC News."""
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    url = "https://www.bbc.com/news"
    driver.get(url)

    # # Try to accept cookies
    # try:
    #     WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agree")]'))
    #     ).click()
    # except Exception as e:
    #     print("Cookie banner not found or failed to click:", e)

    # Wait for the page to load fully
    driver.implicitly_wait(5)

    # Scrape detailed news
    news_list = []
    try:
        # Find all news cards
        news_cards = driver.find_elements(By.XPATH, '//div[@data-testid="card-text-wrapper"]')
        for card in news_cards:
            # Extract headline
            headline_element = card.find_element(By.XPATH, './/h2[@data-testid="card-headline"]')
            headline = headline_element.text

            # Extract description
            try:
                description_element = card.find_element(By.XPATH, './/p[@data-testid="card-description"]')
                description = description_element.text
            except:
                description = None  # Description might not always be available

            # Extract last updated
            try:
                last_updated_element = card.find_element(By.XPATH, './/span[@data-testid="card-metadata-lastupdated"]')
                last_updated = last_updated_element.text
            except:
                last_updated = None  # Last updated might not always be available

            # Extract category
            try:
                category_element = card.find_element(By.XPATH, './/span[@data-testid="card-metadata-tag"]')
                category = category_element.text
            except:
                category = None  # Category might not always be available

            # Add the news details to the list
            news_list.append({
                "headline": headline,
                "description": description,
                "last_updated": last_updated,
                "category": category
            })
    except Exception as e:
        print("Failed to scrape news details:", e)

    driver.quit()
    return news_list, url

# def display_news():
#     """Display all news stored in the SQLite database."""
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Retrieve all news
#     cursor.execute("SELECT * FROM news")
#     rows = cursor.fetchall()

#     if not rows:
#         print("No news articles found in the database.")
#     else:
#         for row in rows:
#             print(f"ID: {row[0]}")
#             print(f"Headline: {row[1]}")
#             print(f"Description: {row[2]}")
#             print(f"Last Updated: {row[3]}")
#             print(f"Category: {row[4]}")
#             print(f"Source: {row[5]}")
#             print("-" * 50)

#     conn.close()

# Main script
initialize_db()
print("Scraping BBC News...")
news_list, site = scrape_bbc_news()
scrapetime = get_todays_datetime()
if news_list:
    print(f"Found {len(news_list)} news articles.")
    save_to_db(news_list, site, scrapetime)
    print("News articles saved to the database.")
else:
    print("No news articles found.")

# # Display saved news
# print("\nSaved News Articles:")
# display_news()
