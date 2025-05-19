
from jinja2 import Template
from pathlib import Path

def genera_relazione_gpt(dati):
    # Carica il template HTML
    template_path = Path("template_relazione.html")
    with open(template_path, encoding="utf-8") as f:
        template = Template(f.read())

    # Prepara i dati per il rendering
    html = template.render(
        titolo="Analisi Finanziaria GPT",
        azienda=dati["azienda"],
        data=dati["data"],
        logo=dati["logo"],
        paragrafo_1=dati["paragrafo_1"],
        paragrafo_2=dati["paragrafo_2"],
        grafico_ebitda=dati["grafico_ebitda"],
        grafico_cashflow=dati["grafico_cashflow"],
        semaforo_bancabilita=dati["semaforo_bancabilita"],
        semaforo_sostenibilita=dati["semaforo_sostenibilita"],
        semaforo_economica=dati["semaforo_economica"],
        semaforo_successo=dati["semaforo_successo"],
        commento_gpt=dati["commento_gpt"],
        strategia_bandi="",
        lista_bandi="",
        filtro_priorita="",
        esg="",
        consigli=""
    )

    return html
