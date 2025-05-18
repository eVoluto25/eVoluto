
import requests
import os

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

def invia_a_make(payload):
    if not MAKE_WEBHOOK_URL:
        raise ValueError("MAKE_WEBHOOK_URL non impostato")

    response = requests.post(MAKE_WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        return True
    else:
        raise Exception(f"Errore invio webhook: {response.status_code} - {response.text}")
