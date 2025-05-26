
import requests
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET_NAME")
if not SUPABASE_BUCKET:
    raise EnvironmentError("❌ Variabile d'ambiente SUPABASE_BUCKET_NAME mancante.")


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

def upload_pdf_to_supabase(file_path, file_name):
    if not (SUPABASE_URL and SUPABASE_API_KEY and SUPABASE_BUCKET):
        raise EnvironmentError("⚠️ Variabili ambiente Supabase mancanti.")

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/pdf"
    }

    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_name}"

    with open(file_path, "rb") as f:
        pdf_content = f.read()

    response = requests.put(url, headers=headers, data=pdf_content)

    if response.status_code in [200, 201]:
        return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
    else:
        raise Exception(f"❌ Upload fallito PDF: {response.status_code} – {response.text}")

def salva_output(tipo, contenuto, email, indice=None):
    nome_file = f"{tipo}_{email}"
    if indice is not None:
        nome_file += f"_{indice}"
    file_name = f"{nome_file}.txt"
    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_name}"

    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "text/plain"
    }

    response = requests.put(url, headers=headers, data=contenuto.encode("utf-8"))
    if response.status_code not in [200, 201]:
        raise Exception(f"Errore nel salvataggio Supabase: {response.status_code} - {response.text}")

def recupera_output(tipo, email, indice=None):
    nome_file = f"{tipo}_{email}"
    if indice is not None:
        nome_file += f"_{indice}"
    file_name = f"{nome_file}.txt"
    url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def salva_output_blocco(modulo, email, i, contenuto):
    chiave = f"{modulo}_blocco_{i}"
    salva_output(chiave, contenuto, email)

def recupera_output_blocco(modulo, email, i):
    chiave = f"{modulo}_blocco_{i}"
    return recupera_output(chiave, email)
