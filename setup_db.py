import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("leads.db")
cursor = conn.cursor()

# Crear la tabla de historial de envíos si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_email TEXT NOT NULL,
    campaña TEXT NOT NULL,
    etapa INTEGER NOT NULL,
    fecha_envio TEXT NOT NULL
);
""")

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()

print("Tabla 'envios' creada exitosamente.")