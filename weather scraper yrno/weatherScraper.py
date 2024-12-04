import requests
from bs4 import BeautifulSoup
import sqlite3

# Step 1: Fetch the webpage
url = 'https://www.yr.no/nb/v%C3%A6rvarsel/daglig-tabell/2-1850147/Japan/Tokyo/Tokyo'
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Extract weather data
# Note: The actual HTML structure should be inspected to adjust the selectors accordingly
weather_data = []
forecast_table = soup.find('table', {'class': 'yr-table yr-table-hourly'})
if forecast_table:
    for row in forecast_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if len(columns) >= 5:
            date = columns[0].get_text(strip=True)
            temperature = columns[1].get_text(strip=True)
            weather = columns[2].get_text(strip=True)
            precipitation = columns[3].get_text(strip=True)
            wind = columns[4].get_text(strip=True)
            weather_data.append((date, temperature, weather, precipitation, wind))

# Step 4: Save data to SQLite
conn = sqlite3.connect('weather_forecast.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tokyo_weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        temperature TEXT,
        weather TEXT,
        precipitation TEXT,
        wind TEXT
    )
''')

# Insert data
cursor.executemany('''
    INSERT INTO tokyo_weather (date, temperature, weather, precipitation, wind)
    VALUES (?, ?, ?, ?, ?)
''', weather_data)

# Commit and close
conn.commit()
conn.close()

print("Weather data has been successfully scraped and stored in 'weather_forecast.db'.")
