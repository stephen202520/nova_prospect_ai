import tkinter as tk
import sys
import os

# Ajuste de ruta para importar desde core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '../../')))

from core.messagegen_ai_v2 import generar_mensaje_ia
from core.envio_email import enviar_email_real

class Botonera:
    def _init_(self, parent, get_datos_lead, get_modo_activo, contador_callback, log_callback):
        self.parent = parent
        self.get_datos_lead = get_datos_lead
        self.get_modo_activo = get_modo_activo
        self.contador_callback = contador_callback
        self.log_callback = log_callback

        self.crear_boton("Send Email to Lead", "Enviar primer mensaje", self.enviar_mensaje_inicial)
        self.crear_boton("Send Follow-Up", "Enviar seguimiento", self.enviar_mensaje_followup)
        self.crear_boton("Send Closing Email", "Enviar mensaje final", self.enviar_mensaje_cierre)

    def crear_boton(self, texto, texto_es, comando):
        frame = tk.Frame(self.parent, bg="#1a1a1a")
        frame.pack(pady=6)
        boton = tk.Button(
            frame,
            text=texto,
            font=("Segoe UI", 12, "bold"),
            bg="#007acc",
            fg="white",
            padx=14,
            pady=6,
            command=comando
        )
        boton.pack()
        etiqueta = tk.Label(
            frame,
            text=texto_es,
            font=("Segoe UI", 9),
            bg="#1a1a1a",
            fg="#cccccc"
        )
        etiqueta.pack()

    def enviar_mensaje_inicial(self):
        self._procesar_envio(tipo="inicial")

    def enviar_mensaje_followup(self):
        self._procesar_envio(tipo="seguimiento")

    def enviar_mensaje_cierre(self):
        self._procesar_envio(tipo="cierre")

    def _procesar_envio(self, tipo):
        datos_lead = self.get_datos_lead()
        modo = self.get_modo_activo()

        if not datos_lead or "email" not in datos_lead:
            self.log_callback("Lead incompleto o sin email.")
            return

        self.log_callback(f"Generando mensaje IA ({tipo}) para {datos_lead['email']}...")

        try:
            asunto, cuerpo = generar_mensaje_ia(datos_lead, tipo=tipo, modo=modo)
            enviado = enviar_email_real(datos_lead['email'], asunto, cuerpo)

            if enviado:
                self.contador_callback()
                self.log_callback(f"Email enviado exitosamente a {datos_lead['email']}.")
            else:
                self.log_callback(f"No se pudo enviar el email a {datos_lead['email']}.")

        except Exception as e:
            self.log_callback(f"Error al generar/enviar mensaje: {str(e)}")