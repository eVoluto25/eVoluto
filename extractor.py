from blocchi_utils import suddividi_blocchi_coerenti

import fitz  # PyMuPDF
import logging

def estrai_blocchi_da_pdf(percorso_pdf, max_caratteri=3000):
    blocchi = []
    testo = ""

    with fitz.open(percorso_pdf) as doc:
        for pagina in doc:
            testo += pagina.get_text("text")

    logging.info(f"🧩 Testo totale PDF: {len(testo)} caratteri")

    blocchi = suddividi_blocchi_coerenti(testo, max_caratteri)
    logging.info(f"🧱 Diviso in {len(blocchi)} blocchi coerenti")

    return blocchi
