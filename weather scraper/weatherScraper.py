import time
import os
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Database setup
DB_FOLDER = "db"
DB_PATH = os.path.join(DB_FOLDER, "dmi_weather.db")

def initialize_db():
    """Initialize SQLite database and create a weather_data table."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            temperature TEXT,
            precipitation TEXT,
            wind_speed TEXT,
            uv_index TEXT,
            humidity TEXT
        )
    ''')
    conn.commit()
    conn.close()
def scrape_dmi_weather():
    """Scrape weather data from DMI's Aarhus page."""
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the DMI weather page for Aarhus
    url = "https://www.dmi.dk/lokation/show/DK/2624652/Aarhus/#9"
    driver.get(url)

    # Allow time for the page to load
    time.sleep(5)

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Debug: Print the structure of the page
    print(soup.prettify())

    # Find all weather data entries
    weather_entries = soup.find_all('div', class_='MuiAccordionSummary-content')
    if not weather_entries:
        print("No weather entries found. Check the class names or page structure.")
        return []

    weather_data = []
    for entry in weather_entries:
        try:
            # Extract data fields
            date_time = entry.find('p', class_='bold-font xl-column')
            temperature = entry.find('span', class_='large-data')
            precipitation = entry.find_all('p', class_='small-column column-base-style')[0]
            wind_speed = entry.find_all('p', class_='small-column column-base-style')[1]
            uv_index = entry.find('span', class_='uv bold-font')
            humidity = entry.find_all('p', class_='small-column column-base-style hide-on-smaller-than-4')[1]

            if not all([date_time, temperature, precipitation, wind_speed, uv_index, humidity]):
                print(f"Missing data in entry: {entry}")
                continue

            weather_data.append({
                "date_time": date_time.text.strip(),
                "temperature": temperature.text.strip(),
                "precipitation": precipitation.text.strip(),
                "wind_speed": wind_speed.text.strip(),
                "uv_index": uv_index.text.strip(),
                "humidity": humidity.text.strip()
            })
        except Exception as e:
            print(f"Error parsing entry: {e}")
            continue

    return weather_data


def save_to_db(weather_data):
    """Save weather data to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for weather in weather_data:
        cursor.execute('''
            INSERT INTO weather_data (date, time, temperature, precipitation, wind_speed, uv_index, humidity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            weather['date_time'].split(' ')[1],  # Date
            weather['date_time'].split(' ')[-1],  # Time
            weather['temperature'],
            weather['precipitation'],
            weather['wind_speed'],
            weather['uv_index'],
            weather['humidity']
        ))
    conn.commit()
    conn.close()

def display_weather_data():
    """Display all weather data stored in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Time", "Temperature", "Precipitation",
                                         "Wind Speed", "UV Index", "Humidity"])
        print(df)
    else:
        print("No weather data found in the database.")

def export_to_csv():
    """Export weather data from the database to a CSV file."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM weather_data", conn)
    output_path = os.path.join(DB_FOLDER, "dmi_weather_data.csv")
    df.to_csv(output_path, index=False)
    conn.close()
    print(f"Data exported to {output_path}")

if __name__ == "__main__":
    initialize_db()

    print("Scraping weather data from DMI...")
    weather_data = scrape_dmi_weather()

    if weather_data:
        print(f"Scraped data for {len(weather_data)} weather entries.")
        save_to_db(weather_data)
        print("Weather data saved to the database.")

        # Display the data
        display_weather_data()

        # Ask to export to CSV
        export_choice = input("Would you like to export the data to CSV? (yes/no): ").strip().lower()
        if export_choice in ['yes', 'y']:
            export_to_csv()
    else:
        print("No weather data found.")