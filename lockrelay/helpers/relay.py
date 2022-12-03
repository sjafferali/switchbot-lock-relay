import requests
from cfg import WEBHOOK_URL

TIMEOUT=10

def send_webhook(data):
    rheaders = {
        "Content-Type": "application/json",
    }
    r = requests.post(WEBHOOK_URL, json=data, headers=rheaders, timeout=TIMEOUT)
    r.raise_for_status()
    
