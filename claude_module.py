import logging
import openai  # Sostituire con `import anthropic` se si usa Claude via Anthropic
from blocchi_utils import suddividi_blocchi_coerenti

def chiedi_claude_blocchi(blocchi, modello="gpt-3.5-turbo"):  # Sostituire con il modello Claude se necessario
    risposte = []

    for i, blocco in enumerate(blocchi):
        prompt = (
            f"Analizza il seguente estratto aziendale (blocco {i+1}):\n\n{blocco}\n\n"
            "Fornisci suggerimenti sintetici su bandi agevolabili potenzialmente rilevanti per questa azienda."
        )

        logging.info(f"📤 Inviando blocco {i+1}/{len(blocchi)} a Claude, lunghezza: {len(blocco)} caratteri")

        try:
            response = openai.ChatCompletion.create(  # Sostituire con API call specifica per Claude
                model=modello,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            contenuto = response.choices[0].message.content
            risposte.append(contenuto)
            logging.info(f"✅ Claude ha risposto per blocco {i+1}")

        except Exception as e:
            logging.error(f"❌ Errore Claude nel blocco {i+1}: {e}")
            risposte.append("Errore nell'elaborazione di questo blocco.")

    return risposte


def genera_relazione_con_claude(caratteristiche_azienda, url_output_gpt, bandi_filtrati):
    logging.info("📥 Generazione relazione Claude")

    html = f""" 
    <html>
        <body>
            <h1>Relazione Matching Bandi Claude</h1>
            <h2>Azienda: {caratteristiche_azienda.get('denominazione')}</h2>
            <p>Codice ATECO: {caratteristiche_azienda.get('codice_ateco')}</p>
            <p>Analisi GPT: <a href="{url_output_gpt}" target="_blank">Visualizza</a></p>
            <hr>
            <h3>Bandi suggeriti:</h3>
            <ul>
                {"".join([f"<li>{bando}</li>" for bando in bandi_filtrati]) or "<li>Nessun bando disponibile</li>"}
            </ul>
        </body>
    </html>
    """.strip()

    return html


def elabora_relazione_claude(caratteristiche_azienda, testo_completo):
    logging.info("📦 Inizio elaborazione relazione Claude")

    blocchi = suddividi_blocchi_coerenti(testo_completo)
    logging.info(f"📑 Suddivisi in {len(blocchi)} blocchi")

    risposte = chiedi_claude_blocchi(blocchi)

    analisi_finale = "\n\n".join(risposte)
    logging.info("🧾 Analisi finale Claude pronta")

    return analisi_finale
