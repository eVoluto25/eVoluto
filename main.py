import requests
import httpx
import os
import json
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
from storage_handler import upload_html_to_supabase
from gestore_processo import (
    aggiorna_stato,
    mostra_stato,
    salva_blocchi_gpt,
    salva_blocchi_claude
)
from storage_handler import salva_output, recupera_output

app = FastAPI()

class InputData(BaseModel):
    file_url: str
    name: str
    phone: str
    email: str

def aggiorna_stato(email, stato):
    salva_output("stato", stato, email)

def recupera_stato(email):
    return recupera_output("stato", email) or ""

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

    # 🔁 Verifica stato analisi precedente
    stato_attuale = recupera_stato(email)

    if stato_attuale == "email_inviata":
        logging.info("✅ Analisi già completata. Nessuna azione necessaria.")
        return {
            "message": "Analisi già completata",
            "relazione_gpt": recupera_output("relazione_gpt", email),
            "relazione_claude": recupera_output("relazione_claude", email),
            "dossier_pdf": recupera_output("dossier_pdf", email)
        }
    elif stato_attuale == "pdf_generato":
        logging.info("🔁 Analisi GPT completata. Riprendo da Claude...")
    elif stato_attuale == "gpt_completato":
        logging.info("🔁 Analisi Claude completata. Riprendo dal PDF...")

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
    risposte_gpt = chiedi_gpt_blocchi(blocchi, email)
    dati_estratti = unisci_output_gpt(risposte_gpt)
    blocchi_gpt = dati_estratti.split("\n\n")
    salva_blocchi_gpt(blocchi_gpt)
    aggiorna_stato(email, "analisi_gpt_completata")
    logging.info("✅ Analisi GPT completata")

    url_claude = genera_relazione_con_claude({
        "caratteristiche_azienda": caratteristiche_azienda,
        "email": email
    })
    
    logging.info("📄 Generazione HTML bancabile da GPT")

    url_claude = None  # inizializzazione preventiva
    html_gpt = None
    url_gpt = None

    try:
        html_gpt = costruisci_payload(caratteristiche_azienda, None, None)
        url_gpt = upload_html_to_supabase(json.dumps(html_gpt), "relazione_gpt.html")
        aggiorna_stato(email, "html_gpt_generato")
        logging.info(f"✅ Relazione GPT caricata: {url_gpt}")
    except Exception as e:
        logging.error(f"❌ Errore salvataggio HTML GPT: {e}")
        
    if url_gpt and url_claude:
        aggiorna_stato(email, "html_gpt_generato")
        logging.info(f"✅ Relazione GPT caricata: {url_gpt}")
    else:
        logging.error("❌ URL GPT o Claude mancanti. Impossibile generare HTML finale.")

    logging.info("🔎 Aggiornamento bandi disponibili...")
    bandi_non_filtrati = aggiorna_bandi()
    bandi_filtrati = seleziona_bandi_priori(bandi_non_filtrati)
    aggiorna_stato(email, "bandi_filtrati_completati")

    # Calcolo del numero e importo totale dei bandi
    totale_bandi_attivi = len(bandi_compatibili)

    totale_importo_bandi = sum(
        b.get("stanziamento_incentivo", 0)
        for b in bandi_compatibili
        if isinstance(b.get("stanziamento_incentivo", 0), (int, float))
    )

    dati_input = {
        "bandi_filtrati": bandi_filtrati,
        "url_output_gpt": url_output_gpt,
        "totale_bandi_attivi": totale_bandi_attivi,
        "totale_importo_bandi": totale_importo_bandi
    }

    logging.info("🧠 Generazione relazione Claude")
    aggiorna_stato(email, "generazione_relazione_claude_iniziata")
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

    aggiorna_stato(email, "generazione_relazione_claude_completata")
    url_claude = upload_html_to_supabase(html_claude, "relazione_claude.html")
    aggiorna_stato(email, "html_claude_caricato")
    logging.info(f"✅ Relazione Claude caricata: {url_claude}")

    if not url_gpt or not url_claude:
        logging.warning("⚠️ URL GPT o Claude vuoto. Nessuna email inviata.")
        return
        

    try:
        blocchi_claude = json.loads(html_claude)
        salva_blocchi_claude(blocchi_claude)
        blocchi_pdf = {**blocchi_gpt, **blocchi_claude}

        nome_file_pdf = genera_nome_file(
            caratteristiche_azienda.get("nome", ""),
            caratteristiche_azienda.get("partita_iva", ""),
            caratteristiche_azienda.get("codice_ateco", ""),
            "pdf"
        )
        
        compila_dossier_pdf(
            template_path="template/dossier_eVoluto.pdf",
            output_path=f"/tmp/{nome_file_pdf}",
            blocchi_dict=blocchi_pdf
        ) 
        url_pdf = upload_file_to_supabase(f"/tmp/{nome_file_pdf}", nome_file_pdf)
        aggiorna_stato(email, "pdf_generato")
        logging.info(f"📄 Dossier PDF caricato su Supabase: {url_pdf}")
    
    except Exception as e:
        logging.warning(f"⚠️ Errore generazione dossier PDF: {e}")
        url_pdf = None

    if (
        email and url_gpt and url_claude and url_pdf
        and "Errore nel blocco" not in url_gpt
        and "Errore nel blocco" not in url_claude
    ):
        logging.info("📩 Invio email con risultati")
        invia_email_risultato(email, url_gpt, url_claude)
        aggiorna_stato("email_inviata")
    else:
        logging.warning("❌ Dati incompleti: email non inviata")

    logging.info("📩 Invio email con risultati")
    invia_email_risultato(email, url_gpt, url_claude)

    logging.info("🔁 Invio a scenario Make")
    invia_a_make({
        "azienda": nome_azienda,
        "email": email,
        "telefono": telefono,
        "relazione_gpt": url_gpt,
        "relazione_claude": url_claude,
        "dossier_pdf": url_pdf
    })
    aggiorna_stato(email, "make_inviato")

    return {
        "message": "Analisi completata con successo",
        "relazione_gpt": url_gpt,
        "relazione_claude": url_claude,
        "dossier_pdf": url_pdf
    }
