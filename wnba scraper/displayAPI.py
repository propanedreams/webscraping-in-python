from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
# Database Path
DB_FOLDER = "db"
DB_PATH = f"{DB_FOLDER}/wnba_stats.db"
# Database connection function
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)  # Replace with your database name
    conn.row_factory = sqlite3.Row  # Enable column-based access to rows
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

# Route to display data in a browser
@app.route('/')
def home():
    return '''
        <h1>Player Stats API</h1>
        <p>Visit <a href="/api/player_stats">/api/player_stats</a> to view player stats data.</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
