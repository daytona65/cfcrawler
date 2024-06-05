import os
import sys
import requests
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
webhook_url = os.getenv('WEBHOOK_URL')
system_id = os.getenv('SYSTEM_ID')
headers = {
    "Content-Type": "application/json"
}

file_path = os.path.join(os.path.dirname(sys.argv[0]), 'docs.txt')
file = open(file_path, 'r')
Docs = file.readlines()

# Updating the docs
for doc in Docs:
    command = ''
    if 'confluence.shopee.io' in doc:
        command = '/add_cf_public'
    elif 'docs.google.com' in  doc:
        command = '/add_web_public'
    body = {
            "tag": "text",
            "text": {
                "content": f"<mention-tag target=\"seatalk://user?id={system_id}\"/> {command} {doc}"
        }
    }
    response = requests.post(url=webhook_url, headers=headers, json=body)
    time.sleep(5)

# Prompt engineering
# TODO: Google apps script to read prompts off sheets