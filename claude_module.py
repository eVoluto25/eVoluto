
import logging

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
    """

    return html

def elabora_relazione_claude(caratteristiche_azienda, url_output_gpt, bandi_filtrati):
    return genera_relazione_con_claude(caratteristiche_azienda, url_output_gpt, bandi_filtrati)
