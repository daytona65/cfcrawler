import os
import sys
import requests
import time
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
webhook_url = os.getenv('WEBHOOK_URL')
system_account_id = os.getenv('SYSTEM_ACCOUNT_ID')
headers = {
    "Content-Type": "application/json"
}

file_path = os.path.join(os.path.dirname(sys.argv[0]), 'inoutput/docs1.txt')
file = open(file_path, 'r')
Docs = file.readlines()

# Updating the docs
for i, doc in enumerate(tqdm(Docs)):
    command = ''
    if 'confluence.shopee.io' in doc:
        command = '/add_cf_public'
    elif 'docs.google.com' in  doc:
        command = '/add_web_public'
    body = {
            "tag": "text",
            "text": {
                "content": f"<mention-tag target=\"seatalk://user?id={system_account_id}\"/> {command} {doc}"
        }
    }
    response = requests.post(url=webhook_url, headers=headers, json=body)
    time.sleep(6)
print("Updates done!")
# Prompt engineering
# TODO: Google apps script to read prompts off sheets
