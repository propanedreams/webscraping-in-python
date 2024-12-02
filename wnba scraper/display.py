import sqlite3
from prettytable import PrettyTable
import pandas as pd
import os

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

def export_to_csv():
    """Export player stats from the SQLite database to a CSV file."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM player_stats", conn)
        output_path = os.path.join(DB_FOLDER, "wnba_stats.csv")
        df.to_csv(output_path, index=False)
        print(f"Data exported to {output_path}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Display the player stats
    display_players()

    # Ask the user if they want to export the data to a CSV file
    save_csv = input("Would you like to save this data to a CSV file? (yes/no): ").strip().lower()
    if save_csv in ['yes', 'y']:
        export_to_csv()
