# db/manejador_db.py

import sqlite3
from datetime import datetime

DB_PATH = "data/leads.db"

def obtener_leads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, empresa, sector, cargo, sitio_web, email FROM leads WHERE activo = 1")
    resultados = cursor.fetchall()
    conn.close()

    leads = []
    for row in resultados:
        leads.append({
            "nombre": row[0],
            "empresa": row[1],
            "sector": row[2],
            "cargo": row[3],
            "sitio_web": row[4],
            "email": row[5]
        })
    return leads

def registrar_envio(email, campaña, etapa):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO envios (lead_email, campaña, etapa, fecha_envio)
        VALUES (?, ?, ?, ?)
    """, (email, campaña, etapa, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def obtener_envios_por_email(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT campaña, etapa, fecha_envio FROM envios
        WHERE lead_email = ?
        ORDER BY fecha_envio ASC
    """, (email,))
    resultados = cursor.fetchall()
    conn.close()

    historial = []
    for row in resultados:
        historial.append({
            "campaña": row[0],
            "etapa": row[1],
            "fecha_envio": row[2]
        })
    return historial