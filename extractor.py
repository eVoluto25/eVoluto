
import fitz  # PyMuPDF
import logging

def estrai_blocchi_da_pdf(percorso_pdf, max_caratteri=3000):
    blocchi = []
    testo = ""

    with fitz.open(percorso_pdf) as doc:
        for pagina in doc:
            testo += pagina.get_text("text")

    logging.info(f"🧩 Testo totale PDF: {len(testo)} caratteri")

    while len(testo) > max_caratteri:
        split_point = testo[:max_caratteri].rfind(".")
        blocchi.append(testo[:split_point + 1].strip())
        testo = testo[split_point + 1:]

    if testo.strip():
        blocchi.append(testo.strip())

    logging.info(f"📦 Diviso in {len(blocchi)} blocchi")

    return blocchi
