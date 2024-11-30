from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3

# Initialize SQLite Database
def initialize_db():
    conn = sqlite3.connect('nba_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            player_name TEXT,
            team TEXT,
            games_played INTEGER,
            minutes_per_game REAL,
            points_per_game REAL,
            rebounds_per_game REAL,
            assists_per_game REAL,
            steals_per_game REAL,
            blocks_per_game REAL,
            turnovers_per_game REAL
        )
    ''')
    conn.commit()
    conn.close()

# Save player stats to the database
def save_to_db(player_stats):
    conn = sqlite3.connect('nba_stats.db')
    cursor = conn.cursor()
    for player in player_stats:
        cursor.execute('''
            INSERT INTO player_stats (rank, player_name, team, games_played, minutes_per_game, 
                                       points_per_game, rebounds_per_game, assists_per_game, 
                                       steals_per_game, blocks_per_game, turnovers_per_game)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player['rank'], player['player_name'], player['team'], player['games_played'], 
            player['minutes_per_game'], player['points_per_game'], player['rebounds_per_game'], 
            player['assists_per_game'], player['steals_per_game'], player['blocks_per_game'], 
            player['turnovers_per_game']
        ))
    conn.commit()
    conn.close()

# Scrape NBA player stats
def scrape_nba_stats():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.nba.com/stats/leaders"
    driver.get(url)

    # Wait for table to load
    driver.implicitly_wait(10)

    player_stats = []
    try:
        # Find all rows in the stats table
        rows = driver.find_elements(By.XPATH, '//tr[td[@class="Crom_text__NpR1_ Crom_stickyRank__aN66p"]]')
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            player_stats.append({
                "rank": int(columns[0].text),
                "player_name": columns[1].text,
                "team": columns[2].text,
                "games_played": int(columns[3].text),
                "minutes_per_game": float(columns[4].text),
                "points_per_game": float(columns[5].text),
                "rebounds_per_game": float(columns[12].text),
                "assists_per_game": float(columns[13].text),
                "steals_per_game": float(columns[14].text),
                "blocks_per_game": float(columns[15].text),
                "turnovers_per_game": float(columns[16].text)
            })
    except Exception as e:
        print("Error scraping stats:", e)

    driver.quit()
    return player_stats

# Main script
if __name__ == "__main__":
    initialize_db()
    print("Scraping NBA stats...")
    stats = scrape_nba_stats()
    if stats:
        print(f"Scraped stats for {len(stats)} players.")
        save_to_db(stats)
        print("Stats saved to the database.")
    else:
        print("No stats found.")
