import sqlite3
from prettytable import PrettyTable

def display_weather_data(db_name, table_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Fetch all records from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            # Fetch column names
            column_names = [description[0] for description in cursor.description]

            # Use PrettyTable to display data
            table = PrettyTable()
            table.field_names = column_names

            for row in rows:
                table.add_row(row)

            print(table)
        else:
            print(f"No data found in table {table_name}.")

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Specify the database name and table name
db_name = "db/weather_forecast.db"  # Update with your database name
table_name = "tokyo_weather"  # Update with your table name

# Display the data
display_weather_data(db_name, table_name)
