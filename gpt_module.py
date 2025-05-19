
from openai import OpenAI
from relazione_gpt import genera_relazione_gpt

def carica_prompt_gpt():
    with open("prompts/prompt_gpt.txt", encoding="utf-8") as f:
        return f.read()

def genera_output_gpt(dati_input):
    prompt = carica_prompt_gpt()
    client = OpenAI(api_key=dati_input["gpt_api_key"])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": dati_input["contenuto"]}
        ],
        temperature=0.7
    )

    testo = response.choices[0].message.content
    return genera_relazione_gpt(testo, dati_input)
