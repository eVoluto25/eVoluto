
from jinja2 import Template
from pathlib import Path

def genera_relazione_con_claude(dati):
    # Controlli minimi sui contenuti
    if len(dati.get("strategia_bandi", "").split()) < 250:
        print("⚠️ Claude: strategia_bandi troppo breve")
        dati["strategia_bandi"] = "Sezione in fase di elaborazione. Strategia non ancora disponibile."

    if len(dati.get("lista_bandi", "").split()) < 300:
        print("⚠️ Claude: lista_bandi troppo breve")
        dati["lista_bandi"] = "Elenco dei bandi in aggiornamento."

    if len(dati.get("filtro_priorita", "").split()) < 200:
        print("⚠️ Claude: filtro_priorita troppo breve")
        dati["filtro_priorita"] = "Criteri e filtri non ancora disponibili."

    if len(dati.get("esg", "").split()) < 200:
        print("⚠️ Claude: esg troppo breve")
        dati["esg"] = "Analisi ESG non ancora disponibile."

    if len(dati.get("consigli", "").split()) < 200:
        print("⚠️ Claude: consigli troppo brevi")
        dati["consigli"] = "Suggerimenti strategici non disponibili al momento."

    # Carica il template HTML
    template_path = Path("template_relazione.html")
    with open(template_path, encoding="utf-8") as f:
        template = Template(f.read())

    # Prepara i dati per il rendering
    html = template.render(
        titolo="Analisi Strategica Claude",
        azienda=dati.get("azienda", ""),
        data=dati.get("data", ""),
        logo=dati.get("logo", ""),
        paragrafo_1="",
        paragrafo_2="",
        grafico_ebitda="",
        grafico_cashflow="",
        semaforo_bancabilita="",
        semaforo_sostenibilita="",
        semaforo_economica="",
        semaforo_successo=dati.get("semaforo_successo", "giallo"),
        commento_gpt="",
        strategia_bandi=dati.get("strategia_bandi", ""),
        lista_bandi=dati.get("lista_bandi", ""),
        filtro_priorita=dati.get("filtro_priorita", ""),
        esg=dati.get("esg", ""),
        consigli=dati.get("consigli", "")
    )

    return html
