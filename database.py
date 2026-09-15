import sqlite3

from config import ARCHIVO_BASE_DATOS, OUTPUT_DIR


def inicializar_db():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conexion = sqlite3.connect(ARCHIVO_BASE_DATOS)

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cripto TEXT NOT NULL,
                precio REAL NOT NULL,
                fecha TEXT NOT NULL
            )
        """)

        conexion.commit()
    finally:
        conexion.close()


def inicializar_base_datos():
    inicializar_db()


def obtener_precio_anterior(cripto):
    conexion = sqlite3.connect(ARCHIVO_BASE_DATOS)

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT precio
            FROM historial
            WHERE LOWER(cripto) = LOWER(?)
            ORDER BY id DESC
            LIMIT 1
            """,
            (cripto,),
        )

        resultado = cursor.fetchone()

        if resultado is None:
            return None

        return resultado[0]
    finally:
        conexion.close()


def guardar_precios(reporte):
    conexion = sqlite3.connect(ARCHIVO_BASE_DATOS)

    try:
        cursor = conexion.cursor()

        for item in reporte:
            precio = item.get("precio")

            if isinstance(precio, (int, float)):
                cursor.execute(
                    """
                    INSERT INTO historial (cripto, precio, fecha)
                    VALUES (?, ?, ?)
                    """,
                    (
                        item["nombre"],
                        precio,
                        item["fecha"],
                    ),
                )

        conexion.commit()
    finally:
        conexion.close()


def obtener_historial():
    conexion = sqlite3.connect(ARCHIVO_BASE_DATOS)

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT cripto, precio, fecha
            FROM historial
            ORDER BY id ASC
            """
        )

        return cursor.fetchall()
    finally:
        conexion.close()
