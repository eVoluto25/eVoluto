
from fastapi import FastAPI, UploadFile, Form
from extractor import estrai_blocchi_da_pdf
from relazione_gpt import genera_relazione_gpt
from relazione_claude import genera_relazione_claude
from storage_handler import upload_html_to_supabase
from make_webhook import invia_a_make
from report_generator import costruisci_payload
import os

app = FastAPI()

@app.post("/analizza-pdf/")
async def analizza_pdf(
    file: UploadFile = Form(...),
    nome_azienda: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    partita_iva: str = Form(...),
    provincia: str = Form(...),
    regione: str = Form(...),
    codice_ateco: str = Form(...)
):
    nome_file = f"upload_{file.filename}"
    with open(nome_file, "wb") as f:
        f.write(await file.read())

    blocchi = estrai_blocchi_da_pdf(nome_file)

    # Mock dati GPT e Claude
    caratteristiche = {
        "denominazione": nome_azienda,
        "partita_iva": partita_iva,
        "provincia": provincia,
        "regione": regione,
        "email": email,
        "telefono": telefono,
        "codice_ateco": codice_ateco
    }

    relazione_gpt = genera_relazione_gpt(caratteristiche)
    url_gpt = upload_html_to_supabase(relazione_gpt, "relazione_gpt.html")

    lista_bandi = [
        {"titolo": "Bando Innovazione Lazio", "tipologia": "fondo perduto", "livello": "regionale"},
        {"titolo": "Contributo Nazionale Ricerca", "tipologia": "credito d'imposta", "livello": "nazionale"},
    ]
    valutazioni = {
        "successo": True,
        "settore": True
    }

    relazione_claude = genera_relazione_claude(caratteristiche, lista_bandi, valutazioni)
    url_claude = upload_html_to_supabase(relazione_claude, "relazione_claude.html")

    payload = costruisci_payload(
        caratteristiche=caratteristiche,
        url_gpt=url_gpt,
        url_claude=url_claude,
        altri_dati={"email": email, "telefono": telefono}
    )

    invia_a_make(payload)
    os.remove(nome_file)

    return {"status": "ok", "relazione_gpt": url_gpt, "relazione_claude": url_claude}


from aggiorna_bandi import aggiorna_bandi

@app.get("/aggiorna-bandi")
def aggiorna_bandi_job():
    try:
        aggiorna_bandi()
        return {"status": "aggiornamento completato"}
    except Exception as e:
        return {"error": str(e)}
