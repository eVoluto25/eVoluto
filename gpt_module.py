import openai
import logging
from blocchi_utils import suddividi_blocchi_coerenti
from relazione_gpt import genera_relazione_gpt

def chiedi_gpt_blocchi(testo, modello="gpt-3.5-turbo"):
    blocchi = suddividi_blocchi_coerenti(testo)
    risposte = []

    for i, blocco in enumerate(blocchi):
        prompt = (
            f"Analizza l'estratto del bilancio seguente (blocco {i+1}):\n\n{blocco}\n\n"
            "Estrai i principali indici economici in JSON (ROE, ROS, EBITDA, PFN, DSCR ecc.), "
            "includi una valutazione sintetica, una percentuale di bancabilità e indicazioni ESG."
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
    """
    Unisce le risposte in un unico testo formattato.
    """
    return "\n\n".join(risposte)

def genera_output_gpt(dati_input):
    testo_completo = dati_input["contenuto"]
    risposte = chiedi_gpt_blocchi(testo_completo)
    testo_unito = unisci_output_gpt(risposte)
    return genera_relazione_gpt(testo_unito, dati_input)
