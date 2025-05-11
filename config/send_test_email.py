import smtplib
from email.mime.text import MIMEText
from  config.config import SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD

def enviar_correo_prueba():
    destinatario = EMAIL_USERNAME  # te lo envías a ti mismo
    asunto = "Correo de prueba desde NovaProspectAI"
    cuerpo = "¡Hola! Este es un correo de prueba enviado desde tu aplicación."

    msg = MIMEText(cuerpo)
    msg["Subject"] = asunto
    msg["From"] = EMAIL_USERNAME
    msg["To"] = destinatario

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, destinatario, msg.as_string())
        print("✔ Correo de prueba enviado con éxito.")
    except Exception as e:
        print(f"[!] Error al enviar el correo: {e}")

if __name__ == "__main__":
    enviar_correo_prueba()