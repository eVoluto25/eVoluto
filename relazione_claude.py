
from jinja2 import Template
from pathlib import Path

def genera_relazione_claude(dati):
    # Carica il template HTML
    template_path = Path("template_relazione.html")
    with open(template_path, encoding="utf-8") as f:
        template = Template(f.read())

    # Prepara i dati per il rendering
    html = template.render(
        titolo="Analisi Strategica Claude",
        azienda=dati["azienda"],
        data=dati["data"],
        logo=dati["logo"],
        paragrafo_1="",
        paragrafo_2="",
        grafico_ebitda="",
        grafico_cashflow="",
        semaforo_bancabilita="",
        semaforo_sostenibilita="",
        semaforo_economica="",
        semaforo_successo=dati["semaforo_successo"],
        commento_gpt="",
        strategia_bandi=dati["strategia_bandi"],
        lista_bandi=dati["lista_bandi"],
        filtro_priorita=dati["filtro_priorita"],
        esg=dati["esg"],
        consigli=dati["consigli"]
    )

    return html
