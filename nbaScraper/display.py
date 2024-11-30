import sqlite3

def display_players():
    """Retrieve and display all player stats from the SQLite database."""
    conn = sqlite3.connect('nba_stats.db')
    cursor = conn.cursor()

    # Query to retrieve all player stats
    cursor.execute("SELECT * FROM player_stats")
    rows = cursor.fetchall()

    if not rows:
        print("No player stats found in the database.")
    else:
        print(f"{'Rank':<5} {'Player Name':<25} {'Team':<5} {'GP':<3} {'MPG':<5} {'PPG':<5} {'RPG':<5} {'APG':<5} {'SPG':<5} {'BPG':<5} {'TO':<5}")
        print("-" * 80)
        for row in rows:
            print(f"{row[1]:<5} {row[2]:<25} {row[3]:<5} {row[4]:<3} {row[5]:<5.1f} {row[6]:<5.1f} {row[7]:<5.1f} {row[8]:<5.1f} {row[9]:<5.1f} {row[10]:<5.1f} {row[11]:<5.1f}")

    conn.close()

if __name__ == "__main__":
    display_players()
