import json
import anthropic
import logging
from blocchi_utils import suddividi_blocchi_coerenti
from storage_handler import salva_output_blocco, recupera_output_blocco
from prompt_claude import carica_prompt_claude

def carica_prompt_claude():
    with open("prompts/prompt_claude.txt", encoding="utf-8") as f:
        return f.read()

def genera_relazione_con_claude(dati_input):
    prompt_base = carica_prompt_claude()
    email = dati_input["email"]
    client = anthropic.Anthropic(api_key=dati_input["claude_api_key"])
    blocchi = suddividi_blocchi_coerenti(dati_input["contenuto"])
    risposte = []

    for i, blocco in enumerate(blocchi):
        contenuto_salvato = recupera_output_blocco("claude", email, i)
        if contenuto_salvato:
            logging.info(f"🧠 Blocco {i+1} già analizzato. Skipping...")
            risposte.append(contenuto_salvato)
            continue

        try:
            logging.info(f"📤 Inviando blocco {i+1}/{len(blocchi)} a Claude, lunghezza: {len(blocco)} caratteri")

            prompt = (
                prompt base
                .replace("{{totale_bandi_attivi}}", str(dati_input.get("totale_bandi_attivi", 0)))
                .replace("{{totale_importo_bandi}}", f"{dati_input.get('totale_importo_bandi', 0):,.0f} €")
                + "\n\n--- ANALISI GPT ---\n"
                + dati_input.get("url_output_gpt", "")
                + "\n\n--- BANDI DISPONIBILI ---\n"
                + json.dumps(dati_input.get("bandi_filtrati", []), indent=2)
                + "\n\n[Blocco {i+1}]\n\n"
                + blocco
            )

            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )

            contenuto = response.content[0].text.strip()
            salva_output_blocco("claude", email, i, contenuto)
            risposte.append(contenuto)
            
        except Exception as e:
            logging.error(f"❌ Errore Claude sul blocco {i+1}: {e}")
            risposte.append(f"[Errore nel blocco {i+1}]")

    return "\n\n".join(risposte)
