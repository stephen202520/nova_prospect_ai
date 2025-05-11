import time
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from core.messagegen_ai_v2 import MessageGeneratorAI
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD

class EmailSequenceManager:
    def __init__(self, db=None):
        self.db = db  # se puede conectar con base real más adelante
        self.generator = MessageGeneratorAI()

        # Lead simulado con timestamp falso
        self.leads = [{
            "id": 1,
            "nombre": "Sarah",
            "empresa": "Bluewave Marketing",
            "industria": "Digital Advertising",
            "cargo": "Marketing Director",
            "sitio_web": "https://bluewavemarketing.com",
            "email": "estivenrodriguez2019@gmail.com",
            "ultimo_contacto": datetime.utcnow() - timedelta(hours=30),
            "respondio": False,
            "seguimiento_enviado": False
        }]

    def verificar_seguimiento(self):
        print("[*] Checking leads for follow-up...")

        for lead in self.leads:
            if lead["respondio"] or lead["seguimiento_enviado"]:
                continue

            tiempo_pasado = datetime.utcnow() - lead["ultimo_contacto"]
            if tiempo_pasado > timedelta(hours=24):
                self.enviar_seguimiento(lead)

    def enviar_seguimiento(self, lead):
        print(f"[+] Sending follow-up to {lead['nombre']}")
        mensaje = self.generator.generar_mensaje(lead, modo="cliente", paso="seguimiento")

        if mensaje == "ERROR":
            print(f"[!] Error generating follow-up for {lead['email']}")
            return

        try:
            msg = MIMEText(mensaje)
            msg["Subject"] = "Just following up on my last email"
            msg["From"] = EMAIL_USERNAME
            msg["To"] = lead["email"]

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            lead["seguimiento_enviado"] = True
            print(f"[✔] Follow-up sent to {lead['email']}")

        except Exception as e:
            print(f"[!] Error sending follow-up: {e}")

# Ejecutar en modo prueba
if __name__ == "__main__":
    manager = EmailSequenceManager()
    manager.verificar_seguimiento()