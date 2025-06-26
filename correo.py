import smtplib
from email.mime.text import MIMEText
import os

remitente = os.getenv("SMTP_USER")
clave = os.getenv("SMTP_PASSWORD")

def enviar_bienvenida(destinatario, nombre_usuario):

    asunto = "¡Bienvenido/a!"
    cuerpo = f"Hola {nombre_usuario}, ¡gracias por registrarte! 😊"

    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, clave)
            servidor.send_message(msg)
            print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")
