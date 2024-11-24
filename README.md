Web Scraper(s) with SQLite Persistence
This personal learning project will expand with time, different scrapers/scraping methods will be used. 

A simple Python web scraper, news scraper and SEO scraper that extracts generic information from websites (e.g., titles, meta descriptions, headings, links, and images) and stores the data in a SQLite database.
Features

    Extracts:
        Page title
        Meta description
        Headings (h1, h2, h3)
        Links (<a href>)
        Images (<img src>)
    Saves scraped data to a SQLite database (scraped_data.db) in the db/ folder.
    Automatically creates the db folder and database file if they don't exist.

How It Works

    Scraper:
        Sends an HTTP request to the target URL.
        Parses the HTML response to extract relevant data.
    Database:
        Stores the scraped data (URL, title, meta description, headings, links, images) in a SQLite database.
    Reusable:
        Works with most websites that share standard HTML structures.

Setup

    Clone the repository:

git clone https://github.com/propanedreams/webscraping-in-python.git
cd webscraping-in-python

Setup environment:
    
python -m venv .venv

Install dependencies:

pip install -r requirements.txt

Run the scraper:

    python scraper.py


Example Usage

    Scrape https://example.com:

python scraper.py

View the scraped data:

    Open the SQLite database using any SQLite client.
    Example query:

        SELECT * FROM scraped_data;

Dependencies

    requests: For sending HTTP requests.
    beautifulsoup4: For parsing HTML.
    sqlite3: Built-in Python library for database management.

License

This project is licensed under the MIT License. See the LICENSE file for details.
