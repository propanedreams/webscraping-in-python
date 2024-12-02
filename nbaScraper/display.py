import sqlite3
import os
import csv

DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "nba_stats.db")

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
        print(f"{'Rank':<5} {'Player Name':<25} {'Team':<5} {'GP':<3} {'MPG':<5} {'PPG':<5} {'RPG':<5} {'APG':<5} {'SPG':<5} {'BPG':<5} {'TO':<5}")
        print("-" * 80)
        for row in rows:
            print(f"{row[1]:<5} {row[2]:<25} {row[3]:<5} {row[4]:<3} {row[5]:<5.1f} {row[6]:<5.1f} {row[7]:<5.1f} {row[8]:<5.1f} {row[9]:<5.1f} {row[10]:<5.1f} {row[11]:<5.1f}")

    conn.close()
    return rows

def write_to_csv(data, filename="nba_stats.csv"):
    """Write the player stats to a CSV file."""
    headers = ["Rank", "Player Name", "Team", "Games Played", "Minutes per Game",
               "Points per Game", "Rebounds per Game", "Assists per Game",
               "Steals per Game", "Blocks per Game", "Turnovers per Game"]

    # Write data to CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the header row
        for row in data:
            writer.writerow(row[1:])  # Write all columns except the `id` (row[0])

    print(f"Data successfully written to {filename}.")

if __name__ == "__main__":
    players = display_players()

    if players:
        # Prompt the user to save data to a CSV file
        save_to_csv = input("Would you like to save this data to a CSV file? (yes/no): ").strip().lower()
        if save_to_csv in ['yes', 'y']:
            write_to_csv(players)
