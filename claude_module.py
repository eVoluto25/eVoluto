
from anthropic import Anthropic
from relazione_claude import genera_relazione_claude

def carica_prompt_claude():
    with open("prompts/prompt_claude.txt", encoding="utf-8") as f:
        return f.read()

def genera_output_claude(dati_input):
    prompt = carica_prompt_claude()
    client = Anthropic(api_key=dati_input["claude_api_key"])

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        temperature=0.6,
        system=prompt,
        messages=[
            {"role": "user", "content": dati_input["contenuto"]}
        ]
    )

    testo = message.content[0].text if hasattr(message.content[0], "text") else ""
    return genera_relazione_claude(testo, dati_input)
