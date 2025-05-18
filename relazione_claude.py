
from datetime import datetime

def genera_relazione_claude(azienda, lista_bandi, valutazioni):
    oggi = datetime.now().strftime('%d/%m/%Y')
    azienda_nome = azienda.get("denominazione", "Azienda Sconosciuta")
    partita_iva = azienda.get("partita_iva", "ND")

    semafori = {
        "Probabilità Accesso": "🟢" if valutazioni.get("successo") else "🔴",
        "Adattabilità Settore": "🟢" if valutazioni.get("settore") else "🟡",
        "Tempistiche Ammissibili": "🟡",
        "Copertura Coerente": "🟢"
    }

    bandi_html = "".join([f"<li><b>{b['titolo']}</b> - {b['tipologia'].capitalize()}, {b['livello'].capitalize()}</li>" for b in lista_bandi])

    html = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2cm; }}
        h1, h2 {{ color: #003366; }}
        .page-break {{ page-break-after: always; }}
        ul {{ margin-top: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    </style>
</head>
<body>

<!-- Pagina 1 -->
<h1>Matching Opportunità Finanziarie</h1>
<p><b>Ragione Sociale:</b> {azienda_nome}<br>
<b>Partita IVA:</b> {partita_iva}<br>
<b>Data Analisi:</b> {oggi}</p>

<h2>Bandi selezionati</h2>
<ul>
{bandi_html or "<li>Nessun bando coerente al momento</li>"}
</ul>
<div class="page-break"></div>

<!-- Pagina 2 -->
<h2>Valutazioni Claude</h2>
<table>
{''.join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in semafori.items()])}
</table>
<p><b>Legenda:</b> 🟢 Elevata Coerenza, 🟡 Parziale, 🔴 Non consigliato</p>
<div class="page-break"></div>

<!-- Pagina 3 -->
<h2>Analisi e Suggerimenti</h2>
<p>Claude segnala una buona compatibilità tra il profilo aziendale e i bandi regionali e nazionali. Si consiglia di considerare in priorità quelli a fondo perduto con tempi di apertura ravvicinati. La probabilità di accesso è alta, a patto di presentare progetti ben documentati e coerenti con le linee guida degli enti eroganti.</p>
<div class="page-break"></div>

<!-- Pagina 4 -->
<h2>Azioni Consigliate</h2>
<ol>
    <li>Contattare la Camera di Commercio locale per i bandi territoriali</li>
    <li>Preparare documentazione per almeno 2 bandi regionali</li>
    <li>Iniziare studio tecnico per i progetti ammissibili</li>
</ol>
<div class="page-break"></div>

<!-- Pagina 5 -->
<h2>Conclusione</h2>
<p>In base al matching svolto, l'azienda ha accesso a numerose opportunità di finanziamento. Un corretto piano di presentazione e una consulenza strategica possono massimizzare il punteggio ottenuto nei bandi. Consigliamo una presentazione entro i prossimi 45 giorni per almeno un bando regionale e uno nazionale.</p>

</body>
</html>
"""
    return html
