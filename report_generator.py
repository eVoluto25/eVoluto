
def costruisci_payload(caratteristiche, url_gpt, url_claude, altri_dati):
    return {
        "azienda": caratteristiche.get("denominazione"),
        "partita_iva": caratteristiche.get("partita_iva", "ND"),
        "ateco": caratteristiche.get("codice_ateco", "ND"),
        "email": altri_dati.get("email"),
        "telefono": altri_dati.get("telefono"),
        "output_gpt": url_gpt,
        "output_claude": url_claude,
        "inviato": False
    }
