
from jinja2 import Template
from pathlib import Path

def genera_relazione_gpt(dati):
    # Controlli minimi sui contenuti
    if len(dati.get("paragrafo_1", "").split()) < 300:
        print("⚠️ GPT: paragrafo_1 troppo breve")
        dati["paragrafo_1"] = "Sezione in fase di generazione: contenuto non ancora disponibile."

    if len(dati.get("paragrafo_2", "").split()) < 450:
        print("⚠️ GPT: paragrafo_2 troppo breve")
        dati["paragrafo_2"] = "Analisi approfondita in aggiornamento. Sarà disponibile a breve."

    if len(dati.get("commento_gpt", "").split()) < 350:
        print("⚠️ GPT: commento finale troppo breve")
        dati["commento_gpt"] = "Conclusione temporaneamente non disponibile."

    # Carica il template HTML
    template_path = Path("template_relazione.html")
    with open(template_path, encoding="utf-8") as f:
        template = Template(f.read())

    # Prepara i dati per il rendering
    html = template.render(
        titolo="Analisi Finanziaria GPT",
        azienda=dati.get("azienda", ""),
        data=dati.get("data", ""),
        logo=dati.get("logo", ""),
        paragrafo_1=dati.get("paragrafo_1", ""),
        paragrafo_2=dati.get("paragrafo_2", ""),
        grafico_ebitda=dati.get("grafico_ebitda", ""),
        grafico_cashflow=dati.get("grafico_cashflow", ""),
        semaforo_bancabilita=dati.get("semaforo_bancabilita", "giallo"),
        semaforo_sostenibilita=dati.get("semaforo_sostenibilita", "giallo"),
        semaforo_economica=dati.get("semaforo_economica", "giallo"),
        semaforo_successo=dati.get("semaforo_successo", "giallo"),
        commento_gpt=dati.get("commento_gpt", ""),
        strategia_bandi="",
        lista_bandi="",
        filtro_priorita="",
        esg="",
        consigli=""
    )

    return html
