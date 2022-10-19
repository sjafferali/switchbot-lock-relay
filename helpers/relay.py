import requests
from cfg import WEBHOOK_URL


def send_webhook(data):
    rheaders = {
        "Content-Type": "application/json",
    }
    r = requests.post(WEBHOOK_URL, json=data, headers=rheaders, timeout=5)
    r.raise_for_status()
    
