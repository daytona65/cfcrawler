import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
start_urls = []
with open("inoutput/starters.txt", "r") as file:
    start_urls = file.readlines()
file.close()
pat = os.getenv('PERSONAL_ACCESS_TOKEN')
max_depth = 3
headers = {
    "Authorization": f"Bearer {pat}",
    "Content-Type": "application/json"
}

def is_valid_SPO(url):
    valid = 'https://confluence.shopee.io/display/SPO/'
    if valid in url:
        return True

def is_valid(url):
    valid_substrings=['https://confluence.shopee.io/pages/viewpage.action?pageId=', 'docs.google.com/document/']
    invalid_substrings = ['#', '@', '.action', 'draftId=', '/plugins/', '/diffpagesbyversion/', '/spaces/', 'dopeopledirectorysearch', '/diffpages', 'pageworkflow', '/users/', '/exportword?', '/courses/', '/dashboard/']
    for invalid in invalid_substrings:
        if invalid in url:
            if invalid == '.action' and ('viewpage.action' in url or '/pages.action' in url):
                return True
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
    links = list(map(lambda x : x.strip(), filter(is_valid, [urljoin(url, link['href']) for link in soup.find_all('a', href=True)])))
    invalid_links += list(map(lambda x : x.strip(), filter(lambda x : not is_valid(x), [urljoin(url, link['href']) for link in soup.find_all('a', href=True)])))
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

        links, invalid_links = extract_links(current_url)
        if len(links) > 0:
            visited.add(current_url)
        invalid_visited.update(invalid_links)

        for i, link in enumerate(tqdm(links)):
            queue.append((link, current_depth + 1))

    return visited, invalid_visited

links = set()
invalid_links = set()
for starting in start_urls:
    starting = starting.strip()
    l, il = traverse_links(starting, 1)
    links.update(l)
    invalid_links.update(il)

print("Writing to docs.txt and invaliddocs.txt.........")
with open("inoutput/docs.txt", "w") as file:
    to_write = '\n'.join(links)
    file.write(to_write)
file.close()

with open("inoutput/invaliddocs.txt", "w") as file:
    to_write = '\n'.join(invalid_links)
    file.write(to_write)
file.close()