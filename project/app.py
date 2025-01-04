import requests
from bs4 import BeautifulSoup

base_url = 'https://arxiv.org'
search_url = 'https://arxiv.org/list/cs.CR/recent?skip=0&show=2000'

# Fetch the page content
page = requests.get(search_url)
soup = BeautifulSoup(page.content, "html.parser")

# Find all dt and dd elements
dt_elements = soup.find_all('dt')
dd_elements = soup.find_all('dd')

# Ensure there is a one-to-one correspondence
if len(dt_elements) != len(dd_elements):
    print("Mismatch in number of <dt> and <dd> elements")
    exit()

# Pair dt and dd and extract information
articles = []
for dt, dd in zip(dt_elements, dd_elements):
    article = {}
    # Extract metadata from <dt>
    title_link = dt.find('a', title="Abstract")
    pdf_link = dt.find('a', title="Download PDF")
    if title_link:
        article['id'] = title_link.text.strip()
        article['abstract_url'] = base_url + title_link['href']
    if pdf_link:
        article['pdf_url'] = base_url + pdf_link['href']
    
    # Extract detailed information from <dd>
    title_div = dd.find('div', class_='list-title')
    authors_div = dd.find('div', class_='list-authors')
    comments_div = dd.find('div', class_='list-comments')
    subjects_div = dd.find('div', class_='list-subjects')
    
    if title_div:
        article['title'] = title_div.text.replace('Title:', '').strip()
    if authors_div:
        article['authors'] = [a.text for a in authors_div.find_all('a')]
    if comments_div:
        article['comments'] = comments_div.text.replace('Comments:', '').strip()
    if subjects_div:
        article['subjects'] = subjects_div.text.replace('Subjects:', '').strip()
    
    # Append the article object to the list
    articles.append(article)

# Print the articles
for idx, article in enumerate(articles, start=1):
    print(f"Article {idx}:")
    print(f"  ID: {article.get('id', 'N/A')}")
    print(f"  Title: {article.get('title', 'N/A')}")
    print(f"  Abstract URL: {article.get('abstract_url', 'N/A')}")
    print(f"  PDF URL: {article.get('pdf_url', 'N/A')}")
    print(f"  Authors: {', '.join(article.get('authors', []))}")
    print(f"  Comments: {article.get('comments', 'N/A')}")
    print(f"  Subjects: {article.get('subjects', 'N/A')}")
    print()
