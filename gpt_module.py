import openai
import os
import logging
from extractor import estrai_blocchi_da_pdf
from blocchi_utils import suddividi_blocchi_coerenti
from relazione_gpt import genera_relazione_gpt

def carica_prompt_gpt():
    with open("prompt_gpt.txt", encoding="utf-8") as f:
        return f.read()

def chiedi_gpt_blocchi(testo, modello="gpt-4-0125-preview"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    blocco_grezzo = testo  # usa direttamente il testo passato in input
    blocchi = suddividi_blocchi_coerenti(blocco_grezzo)
    risposte = []

    prompt_base = carica_prompt_gpt()
    for i, blocco in enumerate(blocchi):
        prompt = f"{prompt_base}\n\n[Blocco {i+1}]\n\n{blocco}"
        logging.info(f"📤 Inviando blocco {i+1}/{len(blocchi)} a GPT, lunghezza: {len(blocco)} caratteri")

        try:
            response = client.chatcompletion.create(
                model=modello,
                messages=[
                {"role": "system", "content": "Sei un analista finanziario."},
                {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            testo_generato = response.choices[0].message.content.strip()
            risposte.append(contenuto)
        except Exception as e:
            logging.error(f"❌ Errore GPT sul blocco {i+1}: {e}")
            risposte.append(f"[Errore nel blocco {i+1}]")

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
