import requests
from bs4 import BeautifulSoup

def scrape_generic_info(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve content: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract page title
    title = soup.title.string if soup.title else "No title found"

    # Extract meta description
    meta_description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_description = meta["content"]
    else:
        meta_description = "No meta description found"

    # Extract all headings (h1, h2, h3)
    headings = {
        "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
        "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
        "h3": [h.get_text(strip=True) for h in soup.find_all("h3")],
    }

    # Extract all links
    links = [a['href'] for a in soup.find_all("a", href=True)]

    # Extract all image URLs
    images = [img['src'] for img in soup.find_all("img", src=True)]

    # Print the results
    print(f"Title: {title}")
    print(f"Meta Description: {meta_description}")
    print("\nHeadings:")
    for level, texts in headings.items():
        print(f"  {level}: {texts}")
    print("\nLinks:")
    for link in links[:10]:  # Display the first 10 links for brevity
        print(f"  {link}")
    print("\nImages:")
    for img in images[:10]:  # Display the first 10 images for brevity
        print(f"  {img}")

# URL to scrape
url = "https://google.com"

# Call the scraper function
scrape_generic_info(url)
