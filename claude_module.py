import anthropic
import logging
from blocchi_utils import suddividi_blocchi_coerenti

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

def chiedi_claude_blocchi(testo, modello="claude-3-opus-20240229"):
    blocchi = suddividi_blocchi_coerenti(testo)
    risposte = []

    for i, blocco in enumerate(blocchi):
        logging.info(f"🔹 Inviando blocco {i+1}/{len(blocchi)} a Claude, lunghezza: {len(blocco)} caratteri")

        prompt = (
            f"Analizza l'estratto di bilancio seguente (blocco {i+1}):\n\n{blocco}\n\n"
            "Estrai i dati economici rilevanti (ROE, ROS, EBITDA, PFN, DSCR, Totale Attivo, ecc.) "
            "e restituisci un JSON con questi valori. Includi una valutazione sintetica ESG e "
            "un'indicazione della bancabilità e della sostenibilità finanziaria complessiva."
        )

        try:
            response = client.messages.create(
                model=modello,
                max_tokens=1024,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            risposta = response.content[0].text.strip()
            risposte.append(risposta)
        except Exception as e:
            logging.error(f"❌ Errore Claude nel blocco {i+1}: {e}")
            risposte.append("")

    return risposte
