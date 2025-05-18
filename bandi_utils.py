
import pandas as pd

TIPOLOGIA_PRIORITA = ["fondo perduto", "tasso agevolato", "credito d'imposta"]

def filtra_bandi(ateco, provincia, regione, max_bandi=10, dataset_path="dataset_bandi.csv"):
    df = pd.read_csv(dataset_path)
    df = df[df["ateco"].astype(str).str.startswith(str(ateco)[:2])]  # filtro per settore ATECO

    bandi_finali = []

    # Provincia
    provincia_match = df[df["provincia"].str.lower() == provincia.lower()]
    bandi_finali.extend(ordina_per_tipologia(provincia_match, max_bandi - len(bandi_finali)))

    # Regione
    if len(bandi_finali) < max_bandi:
        regione_match = df[
            (df["regione"].str.lower() == regione.lower()) &
            (~df.index.isin(provincia_match.index))
        ]
        bandi_finali.extend(ordina_per_tipologia(regione_match, max_bandi - len(bandi_finali)))

    # Nazionale
    if len(bandi_finali) < max_bandi:
        nazionale_match = df[
            (df["livello"].str.lower() == "nazionale") &
            (~df.index.isin(provincia_match.index)) &
            (~df.index.isin(regione_match.index))
        ]
        bandi_finali.extend(ordina_per_tipologia(nazionale_match, max_bandi - len(bandi_finali)))

    return [b["titolo"] for b in bandi_finali[:max_bandi]]

def ordina_per_tipologia(df, limite):
    risultati = []
    for tipo in TIPOLOGIA_PRIORITA:
        subset = df[df["tipologia"].str.lower() == tipo]
        risultati.extend(subset.to_dict(orient="records"))
        if len(risultati) >= limite:
            break
    return risultati[:limite]
