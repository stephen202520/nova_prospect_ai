import sqlite3

conn = sqlite3.connect("leads.db")
cursor = conn.cursor()

# Verifica si la columna ya existe antes de agregarla
try:
    cursor.execute("ALTER TABLE leads ADD COLUMN activo INTEGER DEFAULT 1")
    print("Columna 'activo' agregada.")
except:
    print("La columna ya existe o hubo un error.")

conn.commit()
conn.close()