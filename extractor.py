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

def estrai_caratteristiche_azienda(percorso_pdf):
    import pdfplumber
    caratteristiche = {}

    try:
        with pdfplumber.open(percorso_pdf) as pdf:
            testo = ""
            for pagina in pdf.pages:
                testo += pagina.extract_text() + "\n"

        def trova_valore(label):
            for riga in testo.splitlines():
                if label.lower() in riga.lower():
                    parti = riga.split(":")
                    return parti[-1].strip() if len(parti) > 1 else ""
            return ""

        caratteristiche = {
            "denominazione": trova_valore("Denominazione"),
            "amministratore": trova_valore("Amministratore"),
            "codice_ateco": trova_valore("ATECO"),
            "forma_giuridica": trova_valore("Forma giuridica"),
            "cap": trova_valore("CAP"),
            "provincia": trova_valore("Provincia"),
        }

    except Exception as e:
        logging.error(f"Errore estrazione caratteristiche azienda: {e}")

    return caratteristiche
