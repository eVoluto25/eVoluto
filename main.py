import httpx
import os
import logging
from fastapi import FastAPI, UploadFile, Form
from fastapi import File
from extractor import estrai_blocchi_da_pdf
from gpt_module import chiedi_gpt_blocchi, unisci_output_gpt
from relazione_claude import genera_relazione_con_claude
from report_generator import costruisci_payload
from email_handler import invia_email_risultato
from aggiorna_bandi import aggiorna_bandi
from make_webhook import invia_a_make

logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
def root_head():
    return {"status": "✅ eVoluto backend attivo", "version": "1.0"}

@app.post("/analizza-pdf/")
async def analizza_pdf(
    file_url: str = Form(..., alias="upload_1"),
    nome_amministratore: str = Form(..., alias="name_2"),
    email: str = Form(..., alias="email_1"),
    telefono: str = Form(..., alias="phone_1")
):
    logging.info("🔁 Entrata nella funzione analizza_pdf")
    logging.info(f"📥 Nome file ricevuto: {file.filename if file else 'Nessun file'}")
    logging.info(f"👤 Amministratore: {nome_amministratore}")
    logging.info(f"📧 Email: {email}")
    logging.info(f"📞 Telefono: {telefono}")
    logging.info("🚀 Ricevuta richiesta per analisi PDF")

    response = requests.get(file_url)
    response.raise_for_status()
    file_bytes = response.content

    response = httpx.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Errore nel download del file PDF")
    file_bytes = response.content
    
    blocchi = estrai_blocchi_da_pdf(response.content)
    logging.info(f"📄 Estratti {len(blocchi)} blocchi dal PDF")

    logging.info("🤖 Chiamata a GPT per analisi blocchi...")
    risposte_gpt = chiedi_gpt_blocchi(blocchi)
    dati_estratti = unisci_output_gpt(risposte_gpt)
    logging.info("✅ Analisi GPT completata")

    logging.info("📄 Generazione HTML bancabile da GPT")
    html_gpt = costruisci_playroad(dati_estratti)
    url_gpt = upload_html_to_supabase(html_gpt, "relazione_gpt.html")
    logging.info(f"✅ Relazione GPT caricata: {url_gpt}")

    logging.info("🔎 Aggiornamento bandi disponibili...")
    bandi_filtrati = aggiorna_bandi()

    logging.info("🧠 Generazione relazione Claude")
    html_claude = genera_relazione_con_claude(
        caratteristiche_azienda={
            "nome": nome_azienda,
            "email": email,
            "telefono": telefono,
            "partita_iva": partita_iva,
            "codice_ateco": codice_ateco
        },
        url_output_gpt=url_gpt,
        bandi_filtrati=bandi_filtrati
    )
    url_claude = upload_html_to_supabase(html_claude, "relazione_claude.html")
    logging.info(f"✅ Relazione Claude caricata: {url_claude}")

    logging.info("📦 Invio email con risultati")
    invia_email_risultato(email, url_gpt, url_claude)

    logging.info("🔁 Invio a scenario Make")
    invia_a_make({
        "azienda": nome_azienda,
        "email": email,
        "telefono": telefono,
        "relazione_gpt": url_gpt,
        "relazione_claude": url_claude
    })

    return {"message": "Analisi completata con successo", "relazione_gpt": url_gpt, "relazione_claude": url_claude}
