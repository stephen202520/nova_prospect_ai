# ui/dashboard.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
import csv
from fpdf import FPDF
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
            messagebox.showerror("Error", "No se pudo generar el mensaje.")
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
        super().__init__()
        self.title("NovaProspectAI")
        self.geometry("1000x650")
        self.configure(bg="#121212")

        self.modo = tk.StringVar(value="para_mi")  # "cliente"
        self.contador = tk.IntVar(value=0)

        self.crear_ui()

    def crear_ui(self):
        titulo = tk.Label(self, text="NovaProspectAI", font=("Segoe UI", 24, "bold"), bg="#121212", fg="#f6c90e")
        titulo.pack(pady=20)

        selector_frame = tk.Frame(self, bg="#121212")
        selector_frame.pack()

        btn_mi = tk.Button(selector_frame, text="Buscar clientes para mí\n(MODO ACTUAL)", command=lambda: self.cambiar_modo("para_mi"), bg="#007bff", fg="white", width=25)
        btn_mi.grid(row=0, column=0, padx=10)

        btn_cliente = tk.Button(selector_frame, text="Buscar clientes para mis clientes", command=lambda: self.cambiar_modo("cliente"), bg="#6c757d", fg="white", width=25)
        btn_cliente.grid(row=0, column=1, padx=10)

        modo_label = tk.Label(self, textvariable=self.modo, font=("Segoe UI", 16), bg="#121212", fg="white")
        modo_label.pack(pady=5)

        contador_label = tk.Label(self, textvariable=self.contador, font=("Segoe UI", 16), bg="#121212", fg="white")
        contador_label.pack()

        botones_ia = ButtonsSection(self, leads_manager=None, contador_var=self.contador)

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

        btn_historial = tk.Button(
            self,
            text="View Sent History\nVer historial de envíos",
            font=("Segoe UI", 10, "bold"),
            bg="#cccccc",
            fg="#121212",
            command=abrir_historial_envios
        )
        btn_historial.pack(pady=10)

        btn_pdf = tk.Button(
            self,
            text="Export Campaign as PDF\nExportar campaña en PDF",
            font=("Segoe UI", 10, "bold"),
            bg="#ffffff",
            fg="#121212",
            command=generar_pdf
        )
        btn_pdf.pack(pady=10)

        btn_gestion_leads = tk.Button(
            self,
            text="Manage Lead Status\nActivar o Pausar Lead",
            font=("Segoe UI", 10, "bold"),
            bg="#ffcc00",
            fg="#121212",
            command=abrir_gestor_leads
        )
        btn_gestion_leads.pack(pady=10)

    def cambiar_modo(self, nuevo_modo):
        self.modo.set(nuevo_modo)

    def obtener_modo(self):
        return self.modo.get()

    def ejecutar_campaña_automatica(self):
        modo = self.obtener_modo()
        enviados = enviar_mensajes_de_campaña("Campaña_VentasAI", modo)
        messagebox.showinfo("Campaña ejecutada", f"Se enviaron {enviados} mensajes.")
        self.contador.set(self.contador.get() + enviados)


def abrir_historial_envios():
    ventana = tk.Toplevel()
    ventana.title("Historial de Envíos")
    ventana.geometry("800x400")
    ventana.configure(bg="#1a1a1a")

    tabla = tk.Frame(ventana)
    tabla.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(tabla, bg="#1a1a1a")
    scrollbar = tk.Scrollbar(tabla, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#1a1a1a")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    headers = ["Nombre", "Correo", "Fecha", "Tipo de Mensaje", "Día de Campaña"]
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, email, fecha_envio, tipo_mensaje, dia_campania FROM envios ORDER BY fecha_envio DESC")
    registros = cursor.fetchall()
    conn.close()

    for i, h in enumerate(headers):
        tk.Label(scroll_frame, text=h, font=("Segoe UI", 10, "bold"), bg="#1a1a1a", fg="#f6c90e", padx=10).grid(row=0, column=i, sticky="w")

    for r, fila in enumerate(registros, start=1):
        for c, val in enumerate(fila):
            tk.Label(scroll_frame, text=val, bg="#1a1a1a", fg="white", padx=10).grid(row=r, column=c, sticky="w")

    def exportar_csv():
        with open("historial_envios.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(registros)
        messagebox.showinfo("Exportado", "Historial exportado como 'historial_envios.csv'.")

    export_btn = tk.Button(ventana, text="Export as CSV", command=exportar_csv, bg="#f6c90e", fg="#121212", font=("Segoe UI", 10, "bold"))
    export_btn.pack(pady=10)


def generar_pdf():
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, email, fecha_envio, tipo_mensaje, dia_campania FROM envios ORDER BY fecha_envio DESC")
    registros = cursor.fetchall()
    conn.close()

    if not registros:
        messagebox.showwarning("Vacío", "No hay registros para exportar.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(200, 10, "Campaign Report - NovaProspectAI", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    for row in registros:
        nombre, email, fecha, tipo, dia = row
        pdf.cell(0, 10, f"Name: {nombre}", ln=True)
        pdf.cell(0, 10, f"Email: {email}", ln=True)
        pdf.cell(0, 10, f"Date: {fecha}", ln=True)
        pdf.cell(0, 10, f"Type: {tipo} | Day: {dia}", ln=True)
        pdf.ln(5)

    pdf.output("campaña_exportada.pdf")
    messagebox.showinfo("PDF generado", "El reporte fue guardado como 'campaña_exportada.pdf'")


def abrir_gestor_leads():
    ventana = tk.Toplevel()
    ventana.title("Activar o Pausar Lead")
    ventana.geometry("400x250")
    ventana.configure(bg="#1a1a1a")

    label = tk.Label(ventana, text="Email del lead:", bg="#1a1a1a", fg="white", font=("Segoe UI", 10))
    label.pack(pady=10)

    entrada_email = tk.Entry(ventana, width=40)
    entrada_email.pack(pady=5)

    def actualizar_estado(estado):
        email = entrada_email.get().strip()
        if not email:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un correo.")
            return

        conn = sqlite3.connect("leads.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE leads SET activo = ? WHERE email = ?", (estado, email))
        conn.commit()
        conn.close()

        estado_txt = "activado" if estado == 1 else "pausado"
        messagebox.showinfo("Listo", f"El lead fue {estado_txt} correctamente.")

    btn_activar = tk.Button(ventana, text="Activar Lead", command=lambda: actualizar_estado(1), bg="#28a745", fg="white")
    btn_activar.pack(pady=10)

    btn_pausar = tk.Button(ventana, text="Pausar Lead", command=lambda: actualizar_estado(0), bg="#dc3545", fg="white")
    btn_pausar.pack(pady=5)


if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()