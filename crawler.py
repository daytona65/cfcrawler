import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()
start_url = os.getenv('START_URL')
pat = os.getenv('PERSONAL_ACCESS_TOKEN')
max_depth = 3
headers = {
    "Authorization": f"Bearer {pat}",
    "Content-Type": "application/json"
}

# Function to check if the link is a valid Confluence / Google Doc page.
def is_valid(url):
    valid_domains=['confluence.shopee.io', 'docs.google.com']
    invalid = ['plugins', 'display'] # May omit correct pages
    for domain in valid_domains:
        if domain in url:
            return True
    return False

# Returns list of links in a page
def extract_links(url):
    response = requests.get(url, headers=headers)
    if response.headers.get('content-type') is not 'text/html':
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    links = list(filter(is_valid, [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]))
    return links


# Depth Limited Search
def traverse_links(start_url, depth):
    visited = set()
    queue = [(start_url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_depth > depth:
            break

        if current_url in visited:
            continue

        links = extract_links(current_url)
        visited.add(current_url)

        for link in links:
            queue.append((link, current_depth + 1))

    return visited

links = traverse_links(start_url, 2)

with open("docs.txt", "w") as file:
    to_write = '\n'.join(links)
    file.write(to_write)
file.close()
