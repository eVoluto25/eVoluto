
import anthropic
import logging
from blocchi_utils import suddividi_blocchi_coerenti
from relazione_claude import genera_relazione_con_claude

def carica_prompt_claude():
    with open("prompts/prompt_claude.txt", encoding="utf-8") as f:
        return f.read()

def genera_output_claude(dati_input):
    prompt_base = carica_prompt_claude()
    client = anthropic.Anthropic(api_key=dati_input["claude_api_key"])
    blocchi = suddividi_blocchi_coerenti(dati_input["contenuto"])
    risposte = []

    for i, blocco in enumerate(blocchi):
        try:
            logging.info(f"📤 Inviando blocco {i+1}/{len(blocchi)} a Claude, lunghezza: {len(blocco)} caratteri")
            prompt = f"{prompt_base}\n\n[Blocco {i+1}]\n\n{blocco}"
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": f"{prompt}

{blocco}"}
                ]
            )
            contenuto = response.content[0].text.strip()
            risposte.append(contenuto)
        except Exception as e:
            logging.error(f"❌ Errore Claude sul blocco {i+1}: {e}")
            risposte.append("ERRORE")

    testo = "\n\n".join(risposte)
    return genera_relazione_con_claude(testo, dati_input)
