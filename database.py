import sqlite3

def inicializar_db():
    conn = sqlite3.connect("output/historial.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS precios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio REAL,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_precios(reporte):
    conn = sqlite3.connect("output/historial.db")
    cursor = conn.cursor()
    for item in reporte:
        cursor.execute("""
            INSERT INTO precios (nombre, precio, fecha)
            VALUES (?, ?, ?)
        """, (item["nombre"], item["precio"], item["fecha"]))
    conn.commit()
    conn.close()

def obtener_historial():
    conn = sqlite3.connect("output/historial.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, precio, fecha
        FROM precios
        ORDER BY fecha DESC
    """)
    filas = cursor.fetchall()
    conn.close()
    return filas