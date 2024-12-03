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

    # Find all weather data entries
    weather_entries = soup.find_all('div', class_='MuiAccordionSummary-content')
    weather_data = []

    for entry in weather_entries:
        try:
            # Extract data fields
            date_time = entry.find('p', class_='bold-font xl-column').text.strip()
            temperature = entry.find('span', class_='large-data').text.strip()
            precipitation = entry.find_all('p', class_='small-column column-base-style')[0].text.strip()
            wind_speed = entry.find_all('p', class_='small-column column-base-style')[1].text.strip()
            uv_index = entry.find('span', class_='uv bold-font').text.strip()
            humidity = entry.find_all('p', class_='small-column column-base-style hide-on-smaller-than-4')[1].text.strip()

            # Append to list
            weather_data.append({
                "date_time": date_time,
                "temperature": temperature,
                "precipitation": precipitation,
                "wind_speed": wind_speed,
                "uv_index": uv_index,
                "humidity": humidity
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