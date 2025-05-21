import logging
import pdfplumber
from blocchi_utils import suddividi_blocchi_coerenti

def estrai_blocchi_da_pdf(percorso_pdf, max_caratteri=3000):
    testo = ""

    try:
        with pdfplumber.open(percorso_pdf) as pdf:
            for i, pagina in enumerate(pdf.pages):
                testo_pagina = pagina.extract_text()
                logging.info(f"📄 Pagina {i+1}: {len(testo_pagina or '')} caratteri")
                if testo_pagina:
                    testo += testo_pagina + "\n\n"
    except Exception as e:
        logging.error(f"❌ Errore lettura PDF: {e}")

    logging.info(f"📜 Testo totale PDF: {len(testo)} caratteri")

    blocchi = suddividi_blocchi_coerenti(testo, max_caratteri)
    logging.info(f"📦 Diviso in {len(blocchi)} blocchi coerenti")

    return blocchi
