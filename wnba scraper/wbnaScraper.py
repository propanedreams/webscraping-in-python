import time
import sqlite3
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "wnba_stats.db")

def initialize_db():
    """Initialize the SQLite database and create the table."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create a table for storing player stats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            player_name TEXT,
            games_played INTEGER,
            minutes_per_game REAL,
            points_per_game REAL,
            field_goals_made REAL,
            field_goals_attempted REAL,
            field_goal_percentage REAL,
            rebounds REAL,
            assists REAL,
            steals REAL,
            blocks REAL,
            turnovers REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(player_stats):
    """Save player stats to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert player stats into the database
    for player in player_stats:
        cursor.execute('''
            INSERT INTO player_stats (rank, player_name, games_played, minutes_per_game,
                                      points_per_game, field_goals_made, field_goals_attempted,
                                      field_goal_percentage, rebounds, assists, steals, blocks, turnovers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player['rank'], player['player_name'], player['games_played'], player['minutes_per_game'],
            player['points_per_game'], player['field_goals_made'], player['field_goals_attempted'],
            player['field_goal_percentage'], player['rebounds'], player['assists'], player['steals'],
            player['blocks'], player['turnovers']
        ))
    conn.commit()
    conn.close()

def scrape_wnba_stats():
    """Scrape all player stats from the WNBA Season Leaders page."""
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://stats.wnba.com/leaders/"
    driver.get(url)

    # Allow time for JavaScript to load content
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Find the table containing player stats
    table = soup.find('table')
    if not table:
        print("No table found on the page.")
        return []

    # Extract headers (if needed, for debugging purposes)
    headers = [th.text.strip() for th in table.find_all('th')]

    # Extract rows of player stats
    player_stats = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        columns = row.find_all('td')
        if len(columns) < 13:  # Ensure the row has enough data
            continue
        try:
            player_stats.append({
                "rank": int(columns[0].text.strip()),
                "player_name": columns[1].text.strip(),
                "games_played": int(columns[2].text.strip()),
                "minutes_per_game": float(columns[3].text.strip()),
                "points_per_game": float(columns[4].text.strip()),
                "field_goals_made": float(columns[5].text.strip()),
                "field_goals_attempted": float(columns[6].text.strip()),
                "field_goal_percentage": float(columns[7].text.strip()),
                "rebounds": float(columns[11].text.strip()),
                "assists": float(columns[12].text.strip()),
                "steals": float(columns[13].text.strip()),
                "blocks": float(columns[14].text.strip()),
                "turnovers": float(columns[15].text.strip())
            })
        except Exception as e:
            print(f"Error parsing row: {e}")

    return player_stats

if __name__ == "__main__":
    # Initialize the database
    initialize_db()

    # Scrape WNBA stats
    print("Scraping WNBA stats...")
    stats = scrape_wnba_stats()

    if stats:
        print(f"Scraped stats for {len(stats)} players.")
        save_to_db(stats)
        print("Player stats saved to the database.")
    else:
        print("No stats found.")
