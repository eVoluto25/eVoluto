
import os
import requests
import csv
import json
from datetime import datetime
from supabase import create_client, Client

CONFIG_PATH = "config_siti_bandi.json"
BANDI_CSV_FILE = "dataset_bandi.csv"
ETAG_CACHE_FILE = ".etag_cache.txt"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "bandi_disponibili"

def carica_url_da_config(path):
    with open(path, "r") as f:
        config = json.load(f)
    return config.get("urls", [])

def file_aggiornato(url, cache_path):
    response = requests.head(url, timeout=10)
    nuovo_etag = response.headers.get("ETag") or response.headers.get("Last-Modified")

    etag_precedente = None
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            etag_precedente = f.read().strip()

    if nuovo_etag != etag_precedente:
        with open(cache_path, "w") as f:
            f.write(nuovo_etag)
        return True
    return False

def scarica_file(url, destinazione):
    response = requests.get(url, timeout=30)
    with open(destinazione, "wb") as f:
        f.write(response.content)

def formatta_codici_ateco(codice):
    codice = codice.lower().strip()
    if "tutti" in codice or "non applicabile" in codice:
        return "TUTTI"
    if "\" in codice or "/" in codice:
        codice = codice.replace("\", "").replace("/", "")
    return codice

def carica_su_supabase(file_csv):
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError("Variabili SUPABASE_URL o SUPABASE_KEY mancanti.")

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    with open(file_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["Codici_ATECO"] = formatta_codici_ateco(row.get("Codici_ATECO", ""))
            try:
                supabase.table(SUPABASE_TABLE).insert(row).execute()
            except Exception as e:
                print(f"[✖] Errore inserimento riga: {row.get('ID_Incentivo', '?')}: {e}")

def aggiorna_bandi():
    urls = carica_url_da_config(CONFIG_PATH)
    if not urls:
        raise Exception("Nessun URL di aggiornamento trovato.")

    url = urls[0]
    if file_aggiornato(url, ETAG_CACHE_FILE):
        scarica_file(url, BANDI_CSV_FILE)
        print(f"[✔] Dataset aggiornato da {url}")
        carica_su_supabase(BANDI_CSV_FILE)
    else:
        print("[ℹ] Nessun aggiornamento necessario.")

if __name__ == "__main__":
    aggiorna_bandi()
