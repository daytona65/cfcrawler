import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
from tqdm import tqdm
import time

load_dotenv()
start_url = os.getenv('START_URL')
pat = os.getenv('PERSONAL_ACCESS_TOKEN')
max_depth = 3
headers = {
    "Authorization": f"Bearer {pat}",
    "Content-Type": "application/json"
}

def is_valid(url):
    valid_substrings=['confluence.shopee.io', 'docs.google.com/document/']
    invalid_substrings = ['#', '@', 'draftId=', '/plugins/', '/diffpagesbyversion/', '/spaces/', 'dopeopledirectorysearch', '/diffpages', 'pageworkflow', 'login.action?', '/users/']
    for invalid in invalid_substrings:
        if invalid in url:
            return False
    for domain in valid_substrings:
        if domain in url:
            return True
    return False

# Returns list of links in a page
def extract_links(url):
    links = []
    invalid_links = []
    response = requests.get(url, headers=headers)
    content_type = response.headers.get('content-type').lower().replace(" ", "")
    if 'docs.google.com/document/' not in url and (content_type != 'text/html;charset=utf-8' or response.status_code != 200):
        invalid_links.append(url + " | " + response.headers.get('content-type') + " | " + str(response.status_code))
        return links, invalid_links
    soup = BeautifulSoup(response.text, 'html.parser')
    links = list(filter(is_valid, [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]))
    invalid_links += list(filter(lambda x : not is_valid(x), [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]))
    return links, invalid_links


# Depth Limited Search
def traverse_links(start_url, depth):
    visited = set()
    invalid_visited = set()
    queue = [(start_url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_depth > depth:
            break

        if current_url in visited:
            continue
        print(current_url)
        links, invalid_links = extract_links(current_url)
        visited.add(current_url)
        invalid_visited.update(invalid_links)

        for i, link in enumerate(tqdm(links)):
            queue.append((link, current_depth + 1))
            time.sleep(0.005)

    return visited, invalid_visited

links, invalid_links = traverse_links(start_url, 2)


print("Writing to docs.txt and invaliddocs.txt.........")
with open("docs.txt", "w") as file:
    to_write = '\n'.join(links)
    file.write(to_write)
file.close()

with open("invaliddocs.txt", "w") as file:
    to_write = '\n'.join(invalid_links)
    file.write(to_write)
file.close()