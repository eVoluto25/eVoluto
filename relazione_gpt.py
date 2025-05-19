from jinja2 import Template
from pathlib import Path
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime

def genera_grafico(valori, titolo):
    fig, ax = plt.subplots()
    ax.plot(valori, marker='o')
    ax.set_title(titolo)
    ax.grid(True)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{img_base64}" style="width:100%; max-width:600px;">'

def genera_relazione_gpt(dati):
    oggi = datetime.now().strftime('%d/%m/%Y')
    azienda = dati.get("denominazione", "Azienda Sconosciuta")
    partita_iva = dati.get("partita_iva", "ND")
    provincia = dati.get("provincia", "ND")
    email = dati.get("email", "ND")
    telefono = dati.get("telefono", "ND")

    semafori = {
        "Bancabilità": "🟢",
        "Probabilità di Successo": "🟡",
        "Sostenibilità Aziendale": "🔴",
        "Solidità Economico-Finanziaria": "🟢"
    }

    grafico_ebitda = genera_grafico([50, 75, 80, 95], "Andamento EBITDA")
    grafico_cashflow = genera_grafico([20, 40, 35, 55], "Cash Flow Annuale")

    html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2cm; }}
        h1 {{ text-align: center; color: #003366; }}
        .page-break {{ page-break-after: always; }}
        .center {{ text-align: center; }}
        .semafori td {{ padding: 10px; font-size: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    </style>
</head>
<body>

<!-- Pagina 1 - Copertina -->
<div class="page">
    <div class="center">
        <img src="https://i.imgur.com/3XjTQWJ.png" width="150"><br>
        <h1>Analisi Finanziaria Aziendale</h1>
        <h3>Elaborata da eVoluto AI</h3>
        <p><b>Ragione Sociale:</b> {azienda}<br>
        <b>Partita IVA:</b> {partita_iva}<br>
        <b>Provincia:</b> {provincia}<br>
        <b>Email:</b> {email}<br>
        <b>Telefono:</b> {telefono}<br>
        <b>Data Analisi:</b> {oggi}</p>
    </div>
</div>
<div class="page-break"></div>

<!-- Pagina 2 - Semafori -->
<div class="page">
    <h2>Indici Principali e Valutazioni AI</h2>
    <table class="semafori">
        {''.join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in semafori.items()])}
    </table>
    <p><b>Legenda:</b> 🟢 Ottimo, 🟡 Medio, 🔴 Critico</p>
    <p>Secondo l’analisi, l’azienda presenta un buon equilibrio patrimoniale, ma necessita di attenzione su alcuni fronti legati alla sostenibilità operativa. Di seguito un dettaglio tecnico completo.</p>
</div>
<div class="page-break"></div>

<!-- Pagina 3 - Grafici -->
<div class="page">
    <h2>Andamento Finanziario</h2>
    <h3>EBITDA</h3>
    {grafico_ebitda}
    <p>L’EBITDA mostra un trend positivo, segno di redditività operativa crescente.</p>
    <h3>Cash Flow</h3>
    {grafico_cashflow}
    <p>Il Cash Flow evidenzia capacità di autofinanziamento buona e regolare.</p>
</div>
<div class="page-break"></div>

<!-- Pagina 4 - Indici -->
<div class="page">
    <h2>Dettaglio Indici Finanziari</h2>
    <table>
        <tr><th>Indice</th><th>Valore</th></tr>
        <tr><td>ROE</td><td>12%</td></tr>
        <tr><td>ROS</td><td>8%</td></tr>
        <tr><td>EBITDA Margin</td><td>18%</td></tr>
        <tr><td>Totale Attivo</td><td>€ 2.000.000</td></tr>
        <tr><td>Patrimonio Netto</td><td>€ 1.200.000</td></tr>
        <tr><td>PFN</td><td>€ 250.000</td></tr>
        <tr><td>DSCR (media)</td><td>1.8</td></tr>
    </table>
</div>
<div class="page-break"></div>

<!-- Pagina 5 - Considerazioni Finali -->
<div class="page">
    <h2>Analisi e Considerazioni Finali</h2>
    <p>L’analisi svolta evidenzia una situazione finanziaria complessivamente solida. I principali indicatori confermano la bancabilità dell’azienda, con margini operativi e di liquidità adeguati. Tuttavia, il sistema segnala una possibile criticità nella sostenibilità aziendale generale, legata all’equilibrio tra investimenti e capacità di autofinanziamento. Si consiglia una valutazione più approfondita in ottica strategica per rafforzare la resilienza economico-finanziaria di medio-lungo termine.</p>
</div>

</body>
</html>
"""
    return html
