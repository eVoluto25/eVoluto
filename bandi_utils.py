from datetime import datetime

def seleziona_bandi_priori(bandi):
    oggi = datetime.today().date()

    # Filtro bandi aperti (non scaduti)
    bandi_validi = [
        b for b in bandi
        if b.get("Data_chiusura") and datetime.strptime(b["Data_chiusura"], "%Y-%m-%d").date() >= oggi
    ]

    # Ordina bandi per priorità agevolazione e scadenza
    def priorita_agevolazione(b):
        forma = (b.get("Forma_agevolazione") or "").lower()
        if "fondo perduto" in forma:
            return 0
        elif "tasso zero" in forma:
            return 1
        elif "credito" in forma:
            return 2
        return 3

    bandi_validi.sort(key=lambda b: (priorita_agevolazione(b), b.get("Data_chiusura", "9999-12-31")))

    # Filtri per categoria
    def is_camera(b): return "camera di commercio" in (b.get("Ente", "")).lower()
    def is_regionale(b): return "regionale" in (b.get("Categoria", "")).lower()
    def is_nazionale(b): return "nazionale" in (b.get("Categoria", "")).lower()

    camcom = list(filter(is_camera, bandi_validi))
    regionali = list(filter(is_regionale, bandi_validi))
    nazionali = list(filter(is_nazionale, bandi_validi))

    selezionati = []

    # Cascata con target massimo: 1 Camera, 3 Regionali, 16 Nazionali
    selezionati += camcom[:1]
    selezionati += regionali[:3]
    selezionati += nazionali[:16]

    # Se meno di 20, aggiungi altri rimanenti unici
    gia_scelti = set(b["id"] for b in selezionati)
    rimanenti = [b for b in bandi_validi if b["id"] not in gia_scelti]

    while len(selezionati) < 20 and rimanenti:
        selezionati.append(rimanenti.pop(0))

    return selezionati
