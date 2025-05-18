
import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

def upload_html_to_supabase(html_content, file_name):
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "text/html"
    }

    url = f"{SUPABASE_URL}/storage/v1/object/evoluto/{file_name}"
    response = requests.put(url, headers=headers, data=html_content.encode("utf-8"))

    if response.status_code == 200:
        return f"{SUPABASE_URL}/storage/v1/object/public/evoluto/{file_name}"
    else:
        raise Exception(f"Upload fallito: {response.text}")
