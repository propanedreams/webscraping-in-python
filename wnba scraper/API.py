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
    conn = sqlite3.connect(DB_PATH)  # Replace with your actual database file
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return conn

# API route to fetch player stats
@app.route('/api/player_stats', methods=['GET'])
def get_player_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all data from player_stats
        cursor.execute("SELECT * FROM player_stats")
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        player_stats = [dict(row) for row in rows]

        conn.close()
        return jsonify(player_stats)  # Return the data as JSON
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)