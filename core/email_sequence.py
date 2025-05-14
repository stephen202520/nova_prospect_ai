# core/email_sequence.py

from datetime import datetime, timedelta
from core.messagegen_ai_v2 import generar_mensaje_ia
from core.envio_email import enviar_email_a_lead
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD
from db.manejador_db import obtener_leads, registrar_envio, obtener_envios_por_email

def enviar_mensajes_de_campaña(nombre_campaña="Campaña_VentasAI", modo="para_mi"):
    leads = obtener_leads()
    enviados = 0
    hoy = datetime.now()

    for lead in leads:
        email = lead.get("email")
        if not email:
            continue

        historial = obtener_envios_por_email(email)
        etapas_enviadas = [h['etapa'] for h in historial]

        # ENVIAR DÍA 0 (inicio)
        if 0 not in etapas_enviadas:
            mensaje = generar_mensaje_ia(lead, tipo="inicio", modo=modo)
            if mensaje != "ERROR":
                if enviar_email_a_lead(email, "Let me help your business grow with AI", mensaje, EMAIL_USERNAME, EMAIL_PASSWORD):
                    registrar_envio(email, nombre_campaña, 0)
                    enviados += 1
            continue

        for registro in historial:
            fecha_envio = datetime.strptime(registro["fecha_envio"], "%Y-%m-%d %H:%M:%S")
            dias_pasados = (hoy - fecha_envio).days

            # ENVIAR DÍA 3 (seguimiento)
            if registro["etapa"] == 0 and 3 <= dias_pasados < 7 and 1 not in etapas_enviadas:
                mensaje = generar_mensaje_ia(lead, tipo="seguimiento", modo=modo)
                if mensaje != "ERROR":
                    if enviar_email_a_lead(email, "Following up on our AI proposal", mensaje, EMAIL_USERNAME, EMAIL_PASSWORD):
                        registrar_envio(email, nombre_campaña, 1)
                        enviados += 1

            # ENVIAR DÍA 7 (cierre)
            elif registro["etapa"] == 1 and dias_pasados >= 4 and 2 not in etapas_enviadas:
                mensaje = generar_mensaje_ia(lead, tipo="cierre", modo=modo)
                if mensaje != "ERROR":
                    if enviar_email_a_lead(email, "Final note about growing with AI", mensaje, EMAIL_USERNAME, EMAIL_PASSWORD):
                        registrar_envio(email, nombre_campaña, 2)
                        enviados += 1

    return enviados