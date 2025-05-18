
import smtplib
from email.mime.text import MIMEText
import os

def invia_email_interna(azienda, url_gpt, url_claude, destinatario="verifica.evoluto@gmail.com"):
    corpo = f"""
    ✅ Analisi generata per: {azienda}

    📎 GPT:
    {url_gpt}

    📎 Claude:
    {url_claude}
    """

    msg = MIMEText(corpo)
    msg["Subject"] = f"📩 Report completato - {azienda}"
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = destinatario

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
