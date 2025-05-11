import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import sys
import os

# Ajuste de ruta para encontrar el archivo configpi.py en ../config/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(_file_)), "../")))

from config.configpi import EMAIL_REMITENTE, EMAIL_PASSWORD

def enviar_email_real(destinatario, asunto, cuerpo):
    try:
        # Crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = EMAIL_REMITENTE
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        mensaje.attach(MIMEText(cuerpo, "plain"))

        # Configurar conexión segura con servidor SMTP
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
            servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_REMITENTE, destinatario, mensaje.as_string())

        return True

    except Exception as e:
        print(f"[ERROR] Falló el envío de email: {str(e)}")
        return False