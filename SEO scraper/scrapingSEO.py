import requests
from bs4 import BeautifulSoup

def scrape_seo_info(url):
    # Send an HTTP GET request
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code != 200:
        print(f"Failed to fetch {url}: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract canonical link
    canonical = soup.find("link", rel="canonical")
    canonical_url = canonical["href"] if canonical else "No canonical URL found"

    # Extract alternate hreflang links
    alternate_links = [
        {"hreflang": link.get("hreflang", "unknown"), "href": link["href"]}
        for link in soup.find_all("link", rel="alternate")
        if "hreflang" in link.attrs and "href" in link.attrs
    ]

    # Extract meta tags for SEO
    meta_tags = {}
    for meta_name in ["description", "keywords"]:
        meta_tag = soup.find("meta", attrs={"name": meta_name})
        meta_tags[meta_name] = meta_tag["content"] if meta_tag else f"No {meta_name} found"

    # Extract Open Graph meta tags
    og_tags = {}
    for og_name in ["og:title", "og:description", "og:url"]:
        og_tag = soup.find("meta", property=og_name)
        og_tags[og_name] = og_tag["content"] if og_tag else f"No {og_name} found"

    # Extract Twitter card meta tags
    twitter_tags = {}
    for twitter_name in ["twitter:title", "twitter:description", "twitter:url"]:
        twitter_tag = soup.find("meta", attrs={"name": twitter_name})
        twitter_tags[twitter_name] = twitter_tag["content"] if twitter_tag else f"No {twitter_name} found"

    # Extract internal and external links
    links = [a["href"] for a in soup.find_all("a", href=True)]
    internal_links = [link for link in links if url in link or link.startswith("/")]
    external_links = [link for link in links if not (url in link or link.startswith("/"))]

    # Print the results
    print(f"Canonical URL: {canonical_url}")
    print("\nAlternate Links:")
    for alt in alternate_links:
        print(f"  {alt['hreflang']}: {alt['href']}")
    
    print("\nMeta Tags:")
    for name, content in meta_tags.items():
        print(f"  {name}: {content}")

    print("\nOpen Graph Tags:")
    for name, content in og_tags.items():
        print(f"  {name}: {content}")

    print("\nTwitter Tags:")
    for name, content in twitter_tags.items():
        print(f"  {name}: {content}")

    print("\nInternal Links:")
    for link in internal_links[:10]:  # Show first 10 for brevity
        print(f"  {link}")

    print("\nExternal Links:")
    for link in external_links[:10]:  # Show first 10 for brevity
        print(f"  {link}")

# URL to scrape
url = "https://nordicrace.dk/"

# Call the scraper
scrape_seo_info(url)
