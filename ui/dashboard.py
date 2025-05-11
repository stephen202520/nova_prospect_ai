import tkinter as tk
from ui.components.buttons import BotonEnviar

class Dashboard:
    def _init_(self):
        self.root = tk.Tk()
        self.root.title("NovaProspectAI - PRO")
        self.root.geometry("1000x620")
        self.root.configure(bg="#1e1e1e")

        self.modo = "cliente"  # cliente o mi
        self.contador = 0

        self.build_ui()
        self.root.mainloop()

    def build_ui(self):
        tk.Label(
            self.root,
            text="NovaProspectAI",
            font=("Segoe UI", 28, "bold"),
            bg="#1e1e1e",
            fg="#f6c90e"
        ).pack(pady=20)

        self.modo_button = tk.Button(
            self.root,
            text="Mode: For My Clients\nModo: Para mis clientes",
            command=self.toggle_modo,
            font=("Segoe UI", 14),
            bg="#444",
            fg="white",
            width=30,
            height=2
        )
        self.modo_button.pack(pady=10)

        # Botón de enviar
        self.boton_enviar = BotonEnviar(
            parent=self.root,
            modo_callback=self.get_modo,
            contador_callback=self.incrementar_contador
        )

        # Contador visual
        self.label_contador = tk.Label(
            self.root,
            text="Emails sent: 0\nCorreos enviados",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="white"
        )
        self.label_contador.pack(pady=20)

    def toggle_modo(self):
        if self.modo == "cliente":
            self.modo = "mi"
            self.root.configure(bg="#202e1e")
            self.modo_button.config(
                text="Mode: For Me\nModo: Para mí"
            )
        else:
            self.modo = "cliente"
            self.root.configure(bg="#1e1e1e")
            self.modo_button.config(
                text="Mode: For My Clients\nModo: Para mis clientes"
            )

    def get_modo(self):
        return self.modo

    def incrementar_contador(self):
        self.contador += 1
        self.label_contador.config(
            text=f"Emails sent: {self.contador}\nCorreos enviados"
        )

if __name__ == "__main__":
    Dashboard()