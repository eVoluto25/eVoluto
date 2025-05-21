
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import logging

app = FastAPI()

class InputData:
    file_url: str
    name: str
    email: str
    phone: str

@app.post("/analizza")
def elabora_pdf(data: InputData):
    try:
        nome_azienda = data.name
        email = data.email
        telefono = data.phone
        url_gpt = "https://example.com/gpt"
        url_claude = "https://example.com/claude"

        logging.info("📨 Invio a scenario Make")
        invia_a_make({
            "azienda": nome_azienda,
            "email": email,
            "telefono": telefono,
            "relazione_gpt": url_gpt,
            "relazione_claude": url_claude
        })

        return JSONResponse(
            content={
                "status": "success",
                "relazione_gpt": url_gpt,
                "relazione_claude": url_claude
            },
            status_code=200
        )

    except Exception as e:
        logging.error(f"❌ Errore durante l'elaborazione: {e}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
