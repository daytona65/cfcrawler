import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
from tqdm import tqdm

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
    valid_domains=['confluence.shopee.io', 'docs.google.com/document/']
    response = requests.get(url, headers=headers)
    if 'docs.google.com/document/' not in url and (not (response.headers.get('content-type') == 'text/html;charset=UTF-8' or response.headers.get('content-type') == 'text/html; charset=utf-8') or response.status_code != 200):
        invalid_links.append(url + " | " + response.headers.get('content-type') + " | " + str(response.status_code))
        return []
    for domain in valid_domains:
        if domain in url:
            return True
    return False

# Returns list of links in a page
def extract_links(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = list(filter(is_valid, [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]))
    return links


# Depth Limited Search
def traverse_links(start_url, depth):
    visited = set()
    queue = [(start_url, 0)]

    while queue:
        progress = ""
        for i in range(len(queue)):
            progress += "|"
        print(f"Queue length: {len(queue)} " + progress)
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

invalid_links = []
links = traverse_links(start_url, 2)

with open("docs.txt", "w") as file:
    to_write = '\n'.join(links)
    file.write(to_write)
file.close()

with open("invaliddocs.txt", "w") as file:
    to_write = '\n'.join(invalid_links)
    file.write(to_write)
file.close()