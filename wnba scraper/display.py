import sqlite3
from prettytable import PrettyTable

# Database Path
DB_FOLDER = "db"
DB_PATH = f"{DB_FOLDER}/wnba_stats.db"

def display_players():
    """Retrieve and display all player stats from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query to retrieve all player stats
    cursor.execute("SELECT * FROM player_stats")
    rows = cursor.fetchall()

    if not rows:
        print("No player stats found in the database.")
    else:
        # Create a PrettyTable to display the results
        table = PrettyTable()
        table.field_names = [
            "Rank", "Player Name", "Games Played", "Minutes/Game", "Points/Game",
            "FG Made", "FG Attempted", "FG%", "Rebounds", "Assists", "Steals", "Blocks", "Turnovers"
        ]
        for row in rows:
            table.add_row([
                row[1],  # Rank
                row[2],  # Player Name
                row[3],  # Games Played
                row[4],  # Minutes/Game
                row[5],  # Points/Game
                row[6],  # FG Made
                row[7],  # FG Attempted
                row[8],  # FG%
                row[9],  # Rebounds
                row[10], # Assists
                row[11], # Steals
                row[12], # Blocks
                row[13]  # Turnovers
            ])
        print(table)

    conn.close()

if __name__ == "__main__":
    display_players()
