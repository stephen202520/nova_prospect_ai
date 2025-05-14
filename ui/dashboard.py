# ui/dashboard.py

import tkinter as tk
from tkinter import messagebox
from config.config import EMAIL_USERNAME, EMAIL_PASSWORD
from core.envio_email import enviar_email_a_lead
from core.messagegen_ai_v2 import generar_mensaje_ia
from core.email_sequence import enviar_mensajes_de_campaña
from ui.components.buttons import ButtonsSection

class BotonEnviar(tk.Frame):
    def __init__(self, parent, modo_callback, contador_callback):
        super()._init_(parent, bg="#1e1e1e")
        self.parent = parent
        self.modo_callback = modo_callback
        self.contador_callback = contador_callback
        self.pack(pady=10)
        self.build_ui()

    def build_ui(self):
        self.button = tk.Button(
            self,
            text="Send Email to Lead\nEnviar correo al lead",
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=10,
            pady=8,
            command=self.enviar_email
        )
        self.button.pack()

    def enviar_email(self):
        modo = self.modo_callback()

        lead = {
            "nombre": "Sarah",
            "empresa": "Bluewave Marketing",
            "sector": "Digital Advertising",
            "cargo": "Marketing Director",
            "sitio_web": "https://bluewavemarketing.com",
            "email": "estivenrodriguez2019@gmail.com"
        }

        paso = "inicio" if modo == "cliente" else "mi_inicio"
        mensaje = generar_mensaje_ia(lead, tipo=paso, modo=modo)

        if mensaje == "ERROR":
            messagebox.showerror("Error", "No se pudo generar el mensaje con IA.")
            return

        success = enviar_email_a_lead(
            destinatario=lead["email"],
            asunto="Let me help your business grow with AI",
            cuerpo=mensaje,
            remitente=EMAIL_USERNAME,
            clave=EMAIL_PASSWORD
        )

        if success:
            self.contador_callback()
            messagebox.showinfo("Éxito", "Correo enviado correctamente.")
        else:
            messagebox.showerror("Error", "Falló al enviar el correo.")

class Dashboard(tk.Tk):
    def __init__(self):
        super()._init_()
        self.title("NovaProspectAI")
        self.geometry("1000x600")
        self.configure(bg="#121212")

        self.modo = tk.StringVar(value="para_mi")  # o "cliente"
        self.contador = tk.IntVar(value=0)

        self.crear_ui()

    def crear_ui(self):
        titulo = tk.Label(self, text="NovaProspectAI", font=("Segoe UI", 24, "bold"),
                          bg="#121212", fg="#f6c90e")
        titulo.pack(pady=20)

        selector_frame = tk.Frame(self, bg="#121212")
        selector_frame.pack()

        btn_mi = tk.Button(selector_frame, text="Buscar clientes para mí",
                           command=lambda: self.cambiar_modo("para_mi"),
                           bg="#007bff", fg="white", width=25)
        btn_mi.grid(row=0, column=0, padx=10)

        btn_cliente = tk.Button(selector_frame, text="Buscar clientes para mis clientes",
                                command=lambda: self.cambiar_modo("cliente"),
                                bg="#6c757d", fg="white", width=25)
        btn_cliente.grid(row=0, column=1, padx=10)

        modo_label = tk.Label(self, textvariable=self.modo, bg="#121212", fg="white")
        modo_label.pack(pady=5)

        contador_label = tk.Label(self, textvariable=self.contador,
                                  font=("Segoe UI", 16), bg="#121212", fg="white")
        contador_label.pack()

        # Sección de botones IA
        botones_ia = ButtonsSection(self, leads_manager=None, contador_var=self.contador)

        # Botón para ejecutar campaña automática (día 0, 3, 7)
        boton_campaña = tk.Button(
            self,
            text="Launch Automated Campaign\nLanzar campaña automática",
            font=("Segoe UI", 12, "bold"),
            bg="#f6c90e",
            fg="#1a1a1a",
            width=30,
            height=2,
            command=self.ejecutar_campaña_automatica
        )
        boton_campaña.pack(pady=15)

    def cambiar_modo(self, nuevo_modo):
        self.modo.set(nuevo_modo)

    def obtener_modo(self):
        return self.modo.get()

    def ejecutar_campaña_automatica(self):
        modo = self.obtener_modo()
        enviados = enviar_mensajes_de_campaña("Campaña_VentasAI", modo)
        messagebox.showinfo("Campaña ejecutada", f"Se enviaron {enviados} mensajes.")
        self.contador.set(self.contador.get() + enviados)

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()