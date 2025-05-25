
def costruisci_payload(caratteristiche, url_gpt, url_claude):
    return {
        "azienda": caratteristiche.get("denominazione"),
        "partita_iva": caratteristiche.get("partita_iva", "ND"),
        "ateco": caratteristiche.get("codice_ateco", "ND"),
        "email": caratteristiche.get("email"),
        "telefono": caratteristiche.get("telefono"),
        "output_gpt": url_gpt,
        "output_claude": url_claude,
        "inviato": False
    }
