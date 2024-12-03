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