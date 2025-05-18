
from fastapi import FastAPI, UploadFile, Form
from modules.extractor import estrai_blocchi_da_pdf
from modules.gpt_module import elabora_relazione_gpt
from modules.claude_module import elabora_relazione_claude
from modules.storage_handler import upload_html_to_supabase
from modules.make_webhook import invia_a_make
from modules.report_generator import costruisci_payload
import os

app = FastAPI()

@app.post("/analizza-pdf/")
async def analizza_pdf(
    file: UploadFile = Form(...),
    nome_azienda: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...)
):
    nome_file = f"upload_{file.filename}"
    with open(nome_file, "wb") as f:
        f.write(await file.read())

    blocchi = estrai_blocchi_da_pdf(nome_file)
    dati_estratti = elabora_relazione_gpt(blocchi)
    url_relazione_gpt = upload_html_to_supabase(dati_estratti["html"], "relazione_gpt.html")

    url_relazione_claude = elabora_relazione_claude(
        caratteristiche_azienda=dati_estratti["caratteristiche"],
        url_output_gpt=url_relazione_gpt,
        bandi_filtrati=dati_estratti["bandi"]
    )

    payload = costruisci_payload(
        caratteristiche=dati_estratti["caratteristiche"],
        url_gpt=url_relazione_gpt,
        url_claude=url_relazione_claude,
        altri_dati={"nome": nome_azienda, "email": email, "telefono": telefono}
    )

    invia_a_make(payload)
    os.remove(nome_file)
    return {"status": "ok", "relazione_gpt": url_relazione_gpt, "relazione_claude": url_relazione_claude}
