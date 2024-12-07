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

# API route to fetch player stats
@app.route('/api/player_stats', methods=['GET'])
def get_player_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all data from player_stats
        cursor.execute("""
            SELECT id, rank, player_name, games_played, minutes_per_game,
                   points_per_game, field_goals_made, field_goals_attempted,
                   field_goal_percentage, rebounds, assists, steals, blocks, turnovers
            FROM player_stats
        """)
        rows = cursor.fetchall()

        # Map rows to a list of dictionaries with proper order
        columns = [column[0] for column in cursor.description]
        player_stats = [dict(zip(columns, row)) for row in rows]

        conn.close()
        return jsonify(player_stats)  # Return the data as JSON
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)