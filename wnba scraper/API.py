from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Database Path
DB_FOLDER = "db"
DB_PATH = f"{DB_FOLDER}/wnba_stats.db"

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH) 
    conn.row_factory = sqlite3.Row 
    return conn

# Define a PlayerStats class for object mapping
class PlayerStats:
    def __init__(self, id, rank, player_name, games_played, minutes_per_game,
                 points_per_game, field_goals_made, field_goals_attempted,
                 field_goal_percentage, rebounds, assists, steals, blocks, turnovers):
        self.id = id
        self.rank = rank
        self.player_name = player_name
        self.games_played = games_played
        self.minutes_per_game = minutes_per_game
        self.points_per_game = points_per_game
        self.field_goals_made = field_goals_made
        self.field_goals_attempted = field_goals_attempted
        self.field_goal_percentage = field_goal_percentage
        self.rebounds = rebounds
        self.assists = assists
        self.steals = steals
        self.blocks = blocks
        self.turnovers = turnovers

    def to_dict(self):
        return {
            "id": self.id,
            "rank": self.rank,
            "player_name": self.player_name,
            "games_played": self.games_played,
            "minutes_per_game": self.minutes_per_game,
            "points_per_game": self.points_per_game,
            "field_goals_made": self.field_goals_made,
            "field_goals_attempted": self.field_goals_attempted,
            "field_goal_percentage": self.field_goal_percentage,
            "rebounds": self.rebounds,
            "assists": self.assists,
            "steals": self.steals,
            "blocks": self.blocks,
            "turnovers": self.turnovers,
        }

# API route to fetch player stats
@app.route('/api/player_stats', methods=['GET'])
def get_player_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all data from player_stats
        cursor.execute("""
            SELECT * FROM player_stats
        """)
        rows = cursor.fetchall()

        # Transform rows into PlayerStats objects and convert to dictionary
        player_stats = [
            PlayerStats(
                id=row["id"],
                rank=row["rank"],
                player_name=row["player_name"],
                games_played=row["games_played"],
                minutes_per_game=row["minutes_per_game"],
                points_per_game=row["points_per_game"],
                field_goals_made=row["field_goals_made"],
                field_goals_attempted=row["field_goals_attempted"],
                field_goal_percentage=row["field_goal_percentage"],
                rebounds=row["rebounds"],
                assists=row["assists"],
                steals=row["steals"],
                blocks=row["blocks"],
                turnovers=row["turnovers"]
            ).to_dict()
            for row in rows
        ]

        conn.close()
        return jsonify(player_stats)  # Return the data as JSON
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)