import requests
from bs4 import BeautifulSoup
import sqlite3
import os
# Step 1: Fetch the webpage
def fetch_weather_data():
    url = 'https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/2-1850147/Japan/Tokyo/Tokyo'
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return response.text

# Step 2: Parse the HTML content
def parse_weather_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    weather_data = []

    # Locate the table with weather data
    forecast_items = soup.find_all('li', class_='daily-weather-list-item')
    for item in forecast_items:
        # Extract date
        date = item.find('time').get_text(strip=True)

        # Extract temperatures
        temperature = item.find('div', class_='daily-weather-list-item__temperature').get_text(strip=True)

        # Extract precipitation
        precipitation_element = item.find('div', class_='daily-weather-list-item__precipitation')
        precipitation = precipitation_element.get_text(strip=True) if precipitation_element else '0 mm'

        # Extract wind speed
        wind_element = item.find('div', class_='daily-weather-list-item__wind')
        wind = wind_element.get_text(strip=True) if wind_element else 'N/A'

        # Extract weather conditions
        weather_conditions = [symbol.img['alt'] for symbol in item.find_all('li', class_='daily-weather-list-item__symbol')]

        weather_data.append((date, temperature, ', '.join(weather_conditions), precipitation, wind))

    return weather_data

# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "dmi_weather.db")

# Step 3: Save data to SQLite
def save_to_database(weather_data):
    conn = sqlite3.connect('weather_forecast.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokyo_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            temperature TEXT,
            weather_conditions TEXT,
            precipitation TEXT,
            wind TEXT
        )
    ''')

    # Insert data
    cursor.executemany('''
        INSERT INTO tokyo_weather (date, temperature, weather_conditions, precipitation, wind)
        VALUES (?, ?, ?, ?, ?)
    ''', weather_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print("Weather data has been successfully saved to 'weather_forecast.db'.")

# Step 4: Main script logic
def main():
    print("Fetching weather data...")
    html = fetch_weather_data()

    print("Parsing weather data...")
    weather_data = parse_weather_data(html)

    print("Saving data to SQLite database...")
    save_to_database(weather_data)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
