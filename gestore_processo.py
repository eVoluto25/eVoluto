import os
import json

FILE_STATO = "stato_processo.json"
DIR_BLOCCHI_GPT = "blocchi_gpt"
DIR_BLOCCHI_CLAUDE = "blocchi_claude"

# 🧠 Carica lo stato attuale
def carica_stato():
    if os.path.exists(FILE_STATO):
        with open(FILE_STATO, "r") as f:
            return json.load(f)
    return {}

# ✅ Aggiorna un singolo step
def aggiorna_stato(nome_step, valore=True):
    stato = carica_stato()
    stato[nome_step] = valore
    with open(FILE_STATO, "w") as f:
        json.dump(stato, f, indent=2)

# ❓ Verifica se uno step è stato già completato
def stato_step(nome_step):
    stato = carica_stato()
    return stato.get(nome_step, False)

# ♻️ Reset completo del processo
def reset_stato():
    if os.path.exists(FILE_STATO):
        os.remove(FILE_STATO)
    for cartella in [DIR_BLOCCHI_GPT, DIR_BLOCCHI_CLAUDE]:
        if os.path.exists(cartella):
            for file in os.listdir(cartella):
                os.remove(os.path.join(cartella, file))
            os.rmdir(cartella)

# 📊 Log visivo dello stato
def mostra_stato():
    stato = carica_stato()
    if not stato:
        print("⛔ Nessuno stato registrato.")
        return
    print("\n📋 Stato attuale del processo:")
    for step, completato in stato.items():
        icona = "✅" if completato else "❌"
        print(f"{icona} {step}")
    print()

# 💾 Salva blocchi GPT
def salva_blocchi_gpt(blocchi):
    if not os.path.exists(DIR_BLOCCHI_GPT):
        os.makedirs(DIR_BLOCCHI_GPT)
    for i, testo in enumerate(blocchi):
        with open(os.path.join(DIR_BLOCCHI_GPT, f"gpt_b_{i+1}.txt"), "w", encoding="utf-8") as f:
            f.write(testo.strip())

# 💾 Salva blocchi Claude
def salva_blocchi_claude(paragrafi):
    if not os.path.exists(DIR_BLOCCHI_CLAUDE):
        os.makedirs(DIR_BLOCCHI_CLAUDE)
    for i, testo in enumerate(paragrafi):
        with open(os.path.join(DIR_BLOCCHI_CLAUDE, f"claude_p_{i+1}.txt"), "w", encoding="utf-8") as f:
            f.write(testo.strip())
