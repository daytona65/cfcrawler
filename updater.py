import os
import requests
import time

webhook_url = os.getenv('WEBHOOK_URL')
system_id = os.getenv('SYSTEM_ID')
headers = {
    "Content-Type": "application/json"
}
file = open('docs.txt', 'r')
Docs = file.readlines()

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
    time.sleep(6)
