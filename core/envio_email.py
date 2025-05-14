# core/envio_email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_a_lead(destinatario, asunto, cuerpo, remitente, clave):
    try:
        # Configurar el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto

        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Conectar al servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, clave)
        servidor.send_message(mensaje)
        servidor.quit()

        return True

    except Exception as e:
        print("Error al enviar el correo:", e)
        return False