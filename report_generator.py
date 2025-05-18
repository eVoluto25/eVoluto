
def costruisci_payload(caratteristiche, url_gpt, url_claude, altri_dati):
    return {
        "azienda": caratteristiche.get("denominazione"),
        "cf": caratteristiche.get("codice_fiscale", "ND"),
        "ateco": caratteristiche.get("codice_ateco", "ND"),
        "email": altri_dati.get("email"),
        "telefono": altri_dati.get("telefono"),
        "output_gpt": url_gpt,
        "output_claude": url_claude,
        "inviato": False
    }
