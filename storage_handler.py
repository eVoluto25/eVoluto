
import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "evoluto")

def upload_html_to_supabase(html_content, file_name):
    if not (SUPABASE_URL and SUPABASE_API_KEY and SUPABASE_BUCKET):
        raise EnvironmentError("⚠️ Variabili ambiente Supabase mancanti.")

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "text/html"
    }

    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_name}"
    response = requests.put(url, headers=headers, data=html_content.encode("utf-8"))

    if response.status_code in [200, 201]:
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
    else:
        raise Exception(f"❌ Upload fallito: {response.status_code} - {response.text}")
