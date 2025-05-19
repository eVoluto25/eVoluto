
import openai
import logging
from blocchi_utils import suddividi_blocchi_coerenti

def chiedi_gpt_blocchi(blocchi, modello="gpt-3.5-turbo"):
    blocchi = suddividi_blocchi_coerenti(blocchi)
    risposte = []

    for i, blocco in enumerate(blocchi):
        prompt = (
            f"Analizza il seguente estratto di un bilancio PDF (blocco {i+1}):\n\n{blocco}\n\n"
            "Estrai e restituisci solo i dati economico-finanziari principali in JSON, tra cui: "
            "ROE, ROS, EBITDA, Totale Attivo, Patrimonio Netto, Ricavi, PFN, DSCR (50k, 100k, 150k), "
            "PFN/EBITDA, Rating qualitativo, e Giudizio ESG sintetico."
        )

        logging.info(f"📤 Inviando blocco {i+1}/{len(blocchi)} a GPT, lunghezza: {len(blocco)} caratteri")

        try:
            response = openai.ChatCompletion.create(
                model=modello,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            contenuto = response.choices[0].message.content.strip()
            risposte.append(contenuto)
        except Exception as e:
            logging.error(f"❌ Errore GPT sul blocco {i+1}: {e}")
            risposte.append("ERRORE")

    return risposte

def unisci_output_gpt(risposte):
    """Unisce le risposte in un unico testo formattato."""
    return "\n\n".join(risposte)
