def costruisci_payload(caratteristiche_azienda, url_gpt=None, url_claude=None):
    azienda = caratteristiche_azienda.get("azienda", "ND")
    partita_iva = caratteristiche_azienda.get("partita_iva", "ND")
    ateco = caratteristiche_azienda.get("ateco", "ND")
    email = caratteristiche_azienda.get("email", "ND")
    telefono = caratteristiche_azienda.get("telefono", "ND")

    html = f"""
    <html>
      <head><title>Relazione GPT</title></head>
      <body>
        <h1>🧠 Analisi GPT per {azienda}</h1>
        <ul>
          <li><strong>Partita IVA:</strong> {partita_iva}</li>
          <li><strong>Codice ATECO:</strong> {ateco}</li>
          <li><strong>Email:</strong> {email}</li>
          <li><strong>Telefono:</strong> {telefono}</li>
        </ul>
        <h2>📄 File Analisi</h2>
        <p>👉 <a href="{url_gpt}" target="_blank">Scarica analisi GPT</a></p>
        <p>👉 <a href="{url_claude}" target="_blank">Scarica analisi bandi (Claude)</a></p>
      </body>
    </html>
    """
    return html
