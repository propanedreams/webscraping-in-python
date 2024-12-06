Web Scraper(s) with SQLite Persistence
This personal learning project will expand with time, different scrapers/scraping methods will be used. 

A simple Python web scraper, NBA scraper, news scraper, weather scrapers, reddit scraper and SEO scraper that extracts generic information from websites (e.g., titles, meta descriptions, headings, links, and images) and stores the data in a SQLite database.


How they Works

    Scraper:
        Sends an HTTP request to the target URL.
        Parses the HTML response to extract relevant data.
    Database:
        Stores the scraped data (URL, title, meta description, headings, links, images) in a SQLite database.

Setup

    Clone the repository:

git clone https://github.com/propanedreams/webscraping-in-python.git
cd webscraping-in-python

Setup environment:
    
python -m venv .venv

Install dependencies:

pip install -r requirements.txt


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
