# ui/components/buttons.py

import tkinter as tk
from tkinter import messagebox
from core.messagegen_ai_v2 import generar_mensaje_ia
from core.email_sequence import enviar_mensajes_de_campaña
from core.envio_email import enviar_email_a_lead
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD

class ButtonsSection:
    def __init__(self, parent, leads_manager, contador_var):
        self.parent = parent
        self.leads_manager = leads_manager
        self.contador_var = contador_var

        self.frame = tk.Frame(parent, bg="#1a1a1a")
        self.frame.pack(pady=10)

        self.create_button("Send Email to Lead", "Enviar correo inicial al lead", self.send_email_to_lead)
        self.create_button("Send Follow-Up", "Enviar correo de seguimiento (día 3)", self.send_follow_up)
        self.create_button("Launch Campaign", "Lanzar campaña completa (día 0, 3 y 7)", self.launch_campaign)

    def create_button(self, text, subtext, command):
        frame = tk.Frame(self.frame, bg="#1a1a1a")
        frame.pack(pady=7)

        btn = tk.Button(frame, text=text, command=command, font=("Segoe UI", 12, "bold"),
                        bg="#f6c90e", fg="#1a1a1a", width=30, height=2, relief="raised", bd=3)
        btn.pack()

        label = tk.Label(frame, text=subtext, font=("Segoe UI", 9), bg="#1a1a1a", fg="white")
        label.pack()

    def send_email_to_lead(self):
        modo = self.obtener_modo_actual()
        lead = self.leads_manager.obtener_siguiente_lead()

        if not lead:
            messagebox.showinfo("Info", "No hay más leads disponibles.")
            return

        tipo_mensaje = "inicio"
        mensaje = generar_mensaje_ia(lead, tipo=tipo_mensaje, modo=modo)

        if mensaje:
            exito = enviar_email_a_lead(
                destinatario=lead['email'],
                asunto="Let me help your business grow with AI",
                cuerpo=mensaje,
                remitente=EMAIL_USERNAME,
                clave=EMAIL_PASSWORD
            )
            if exito:
                self.incrementar_contador()
                messagebox.showinfo("Enviado", f"Mensaje enviado a {lead['email']}")
            else:
                messagebox.showerror("Error", "No se pudo enviar el correo.")
        else:
            messagebox.showerror("Error", "No se generó el mensaje.")

    def send_follow_up(self):
        modo = self.obtener_modo_actual()
        lead = self.leads_manager.obtener_siguiente_lead()

        if not lead:
            messagebox.showinfo("Info", "No hay más leads disponibles.")
            return

        tipo_mensaje = "seguimiento"
        mensaje = generar_mensaje_ia(lead, tipo=tipo_mensaje, modo=modo)

        if mensaje:
            exito = enviar_email_a_lead(
                destinatario=lead['email'],
                asunto="Just following up – quick reminder",
                cuerpo=mensaje,
                remitente=EMAIL_USERNAME,
                clave=EMAIL_PASSWORD
            )
            if exito:
                self.incrementar_contador()
                messagebox.showinfo("Enviado", f"Seguimiento enviado a {lead['email']}")
            else:
                messagebox.showerror("Error", "No se pudo enviar el correo.")
        else:
            messagebox.showerror("Error", "No se generó el mensaje.")

    def launch_campaign(self):
        modo = self.obtener_modo_actual()
        try:
            enviados = enviar_mensajes_de_campaña("Campaña_VentasAI", modo)
            self.contador_var.set(self.contador_var.get() + enviados)
            messagebox.showinfo("Campaña lanzada", f"Se enviaron {enviados} mensajes en total.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo lanzar la campaña:\n{e}")

    def incrementar_contador(self):
        self.contador_var.set(self.contador_var.get() + 1)

    def obtener_modo_actual(self):
        return self.parent.modo.get()