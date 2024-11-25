from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_bbc_news():
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the URL
    url = "https://www.bbc.com/news"
    driver.get(url)

    # Try to accept cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agree")]'))
        ).click()
    except Exception as e:
        print("Cookie banner not found or failed to click:", e)

    # Wait for the page to load fully
    driver.implicitly_wait(10)

    # Scrape the headlines with data-testid
    headlines = []
    try:
        # Find all elements with data-testid="card-headline"
        articles = driver.find_elements(By.XPATH, '//h2[@data-testid="card-headline"]')
        for article in articles:
            title = article.text  # Get the headline text
            headlines.append(title)
    except Exception as e:
        print("Failed to scrape articles:", e)

    driver.quit()
    return headlines

# Test the scraper
news = scrape_bbc_news()
for idx, item in enumerate(news[:5], 1):  # Print first 5 headlines
    print(f"{idx}. {item}")
