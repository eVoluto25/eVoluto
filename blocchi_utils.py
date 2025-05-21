
import re

def suddividi_blocchi_coerenti(testo: str, max_lunghezza: int = 4500) -> list[str]:
    '''
    Divide il testo in blocchi coerenti (per paragrafi), senza tagli casuali,
    rispettando i limiti di token (approssimati in caratteri).
    '''
    paragrafi = re.split(r'\n{2,}', '\n'.join(testo))
    blocchi = []
    blocco_corrente = ""

    for paragrafo in paragrafi:
        if len(blocco_corrente) + len(paragrafo) + 2 < max_lunghezza:
            blocco_corrente += paragrafo.strip() + "\n\n"
        else:
            blocchi.append(blocco_corrente.strip())
            blocco_corrente = paragrafo.strip() + "\n\n"

    if blocco_corrente.strip():
        blocchi.append(blocco_corrente.strip())

    return blocchi
