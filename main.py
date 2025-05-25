import requests
import httpx
import os
import threading
import logging
logging.basicConfig(level=logging.INFO)
from fastapi.responses import JSONResponse
from fastapi import Body
from pydantic import BaseModel
from fastapi import FastAPI, Form
from extractor import estrai_blocchi_da_pdf
from gpt_module import chiedi_gpt_blocchi, unisci_output_gpt
from relazione_claude import genera_relazione_con_claude
from report_generator import costruisci_payload 
from email_handler import invia_email_risultato
from aggiorna_bandi import aggiorna_bandi
from make_webhook import invia_a_make
from dossier_pdf import compila_dossier_pdf
from extractor import estrai_caratteristiche_azienda
from bandi_utils import seleziona_bandi_priori
from io import BytesIO
from gestore_processo import (
    aggiorna_stato,
    mostra_stato,
    salva_blocchi_gpt,
    salva_blocchi_claude
)

app = FastAPI()

class InputData(BaseModel):
    file_url: str
    name: str
    phone: str
    email: str

@app.api_route("/", methods=["GET", "HEAD"])
def root_head():
    return {"status": "✅ eVoluto backend attivo", "version": "1.0"}

@app.post("/analizza-pdf/")
async def analizza_pdf(data: InputData = Body(...)):
    logging.info("📥 Richiesta inviata a `analizza_pdf`, avvio elaborazione asincrona.")
    
    threading.Thread(target=elabora_pdf, args=(data,)).start()

    return JSONResponse(content={"status": "🧠 Analisi in corso"}, status_code=202)

def elabora_pdf(data: InputData):
    file_url = data.file_url
    nome_amministratore = data.name
    email = data.email
    telefono = data.phone

    logging.info("📥 Richiesta ricevuta al webhook")
    logging.info("🔁 Entrata nella funzione analizza_pdf")
    logging.info(f"📤 File URL: {file_url}")
    logging.info(f"👤 Amministratore: {nome_amministratore}")
    logging.info(f"📧 Email: {email}")
    logging.info(f"📞 Telefono: {telefono}")
    logging.info("🚀 Ricevuta richiesta per analisi PDF")

    response = requests.get(file_url)
    response.raise_for_status()
    file_bytes = response.content

    response = httpx.get(file_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Errore nel download del file PDF")
    file_bytes = response.content
    
    # Scarica il PDF dal file_url
    response = requests.get(file_url)
    response.raise_for_status()
    file_bytes = response.content

    # Converti i byte in un oggetto simile a file
    pdf_file = BytesIO(file_bytes)
    caratteristiche_azienda = estrai_caratteristiche_azienda(pdf_file)

    # Passa il file a pdfplumber tramite la funzione di estrazione
    blocchi = estrai_blocchi_da_pdf(pdf_file)

    logging.info(f"📚 Estratti {len(blocchi)} blocchi dal PDF")

    logging.info("🤖 Chiamata a GPT per analisi blocchi...")
    risposte_gpt = chiedi_gpt_blocchi(blocchi)
    dati_estratti = unisci_output_gpt(risposte_gpt)
    blocchi_gpt = dati_estratti.split("\n\n")
    salva_blocchi_gpt(blocchi_gpt)
    aggiorna_stato("analisi_gpt_completata")
    logging.info("✅ Analisi GPT completata")
    
    logging.info("📄 Generazione HTML bancabile da GPT")
    html_gpt = costruisci_payload(caratteristiche_azienda, url_gpt, url_claude)
    url_gpt = upload_html_to_supabase(html_gpt, "relazione_gpt.html")
    aggiorna_stato("html_gpt_generato")
    logging.info(f"✅ Relazione GPT caricata: {url_gpt}")

    logging.info("🔎 Aggiornamento bandi disponibili...")
    bandi_non_filtrati = aggiorna_bandi()
    bandi_filtrati = seleziona_bandi_priori(bandi_non_filtrati)
    aggiorna_stato("bandi_filtrati_completati")

    # Calcolo del numero e importo totale dei bandi
    totale_bandi_attivi = len(bandi_compatibili)

    totale_importo_bandi = sum(
        b.get("stanziamento_incentivo", 0)
        for b in bandi_compatibili
        if isinstance(b.get("stanziamento_incentivo", 0), (int, float))
    )

    # Aggiunta al dizionario dei dati per Claude
    dati_input = {
        
        "bandi_filtrati": bandi_filtrati,
        "url_output_gpt": url_output_gpt,
        "totale_bandi_attivi": totale_bandi_attivi,
        "totale_importo_bandi": totale_importo_bandi
    }

    logging.info("🧠 Generazione relazione Claude")
    aggiorna_stato("generazione_relazione_claude_iniziata")
    html_claude = genera_relazione_con_claude(
        caratteristiche_azienda={
            "nome": nome_azienda,
            "email": email,
            "telefono": telefono,
            "partita_iva": partita_iva,
            "codice_ateco": codice_ateco
        },
        url_output_gpt=url_gpt,
        bandi_filtrati=bandi_filtrati,
        totale_bandi_attivi=totale_bandi_attivi,
        totale_importo_bandi=totale_importo_bandi
    )

    aggiorna_stato("generazione_relazione_claude_completata")
    url_claude = upload_html_to_supabase(html_claude, "relazione_claude.html")
    aggiorna_stato("html_claude_caricato")
    logging.info(f"✅ Relazione Claude caricata: {url_claude}")

    # ⚠️ Blocca l'invio se uno dei due HTML è vuoto
    if not url_gpt or not url_claude:
        logging.warning("⚠️ URL GPT o Claude vuoto. Nessuna email inviata.")
        return
        
# 📄 Generazione PDF dossier
import json
from dossier_pdf import compila_dossier_pdf

try:
    blocchi_gpt = json.loads(html_gpt)
    blocchi_claude = json.loads(html_claude)
    blocchi_pdf = {**blocchi_gpt, **blocchi_claude}

    compila_dossier_pdf(
        template_path="template/dossier_base.pdf",
        output_path="/tmp/dossier_finale.pdf",
        blocchi_dict=blocchi_pdf
    )

    logging.info("📄 PDF dossier generato con successo.")

    from storage_handler import upload_pdf_to_supabase

    try:
        # Nome file pulito per Supabase (es: dossier_rossi_srl.pdf)
        nome_file_pdf = f"dossier_{nome_azienda.lower().replace(' ', '_')}.pdf"

        # Caricamento su Supabase
        from storage_handler import upload_pdf_to_supabase

        try:
            nome_file_pdf = f"dossier_{nome_azienda.lower().replace(' ', '_')}.pdf"

            url_pdf = upload_pdf_to_supabase(
                "/tmp/dossier_finale.pdf",
                nome_file_pdf
            )
        
            logging.info(f"📤 Dossier PDF caricato su Supabase: {url_pdf}")
            logging.info("📎 Link pubblico PDF pronto per l’invio via Make o email.")
        
        except Exception as e:
            logging.warning(f"⚠️ Errore generazione dossier PDF: {e}")
            url_pdf = None

    except Exception as e:
        logging.warning(f"⚠️ Errore generazione dossier PDF: {e}")
        url_pdf = None

    # 📬 Invio risultati via email
    logging.info("📦 Invio email con risultati")
    invia_email_risultato(email, url_gpt, url_claude)

     # 🤖 Invio a scenario Make
    logging.info("🔁 Invio a scenario Make")
    invia_a_make({
        "azienda": nome_azienda,
        "email": email,
        "telefono": telefono,
        "relazione_gpt": url_gpt,
        "relazione_claude": url_claude,
        "dossier_pdf": url_pdf
    })

    return {
        "message": "Analisi completata con successo",
        "relazione_gpt": url_gpt,
        "relazione_claude": url_claude,
        "dossier_pdf": url_pdf
    }
