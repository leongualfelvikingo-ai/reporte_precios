import json
import secrets
import sqlite3
from datetime import datetime, timezone

from config import OUTPUT_DIR, ARCHIVO_BASE_DATOS


def inicializar_db():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS reportes (
            id TEXT PRIMARY KEY, created_at TEXT NOT NULL, timezone TEXT NOT NULL,
            language TEXT NOT NULL, currency TEXT NOT NULL, crypto_ids TEXT NOT NULL,
            status TEXT NOT NULL, owner_token_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cripto TEXT NOT NULL,
            precio REAL NOT NULL, fecha TEXT NOT NULL, report_id TEXT
        );
        CREATE TABLE IF NOT EXISTS archivos (
            report_id TEXT NOT NULL, formato TEXT NOT NULL, ruta TEXT NOT NULL,
            download_token_hash TEXT NOT NULL, paid INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (report_id, formato)
        );
        """)
        columns = {row[1] for row in db.execute("PRAGMA table_info(historial)")}
        if "report_id" not in columns:
            db.execute("ALTER TABLE historial ADD COLUMN report_id TEXT")


def _hash(token):
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()


def crear_reporte(report_id, crypto_ids, timezone_name, language, currency):
    inicializar_db()
    owner_token = secrets.token_urlsafe(32)
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.execute("INSERT INTO reportes VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
            report_id, datetime.now(timezone.utc).isoformat(), timezone_name, language,
            currency, json.dumps(crypto_ids), "generated", _hash(owner_token),
        ))
    return owner_token


def guardar_precios(reporte, report_id=None):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        for item in reporte:
            if isinstance(item.get("precio"), (int, float)):
                db.execute("INSERT INTO historial (cripto, precio, fecha, report_id) VALUES (?, ?, ?, ?)", (item["id"], item["precio"], item["fecha"], report_id))


def obtener_precio_anterior(cripto):
    inicializar_db()
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT precio FROM historial WHERE LOWER(cripto)=LOWER(?) ORDER BY id DESC LIMIT 1", (cripto,)).fetchone()
    return row[0] if row else None


def obtener_historial(report_id=None):
    inicializar_db()
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        if report_id:
            return db.execute("SELECT cripto, precio, fecha FROM historial WHERE report_id=? ORDER BY id ASC", (report_id,)).fetchall()
        return db.execute("SELECT cripto, precio, fecha FROM historial ORDER BY id ASC").fetchall()


def registrar_archivo(report_id, formato, ruta):
    token = secrets.token_urlsafe(32)
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.execute("INSERT OR REPLACE INTO archivos VALUES (?, ?, ?, ?, 0)", (report_id, formato, str(ruta), _hash(token)))
    return token


def autorizar_descarga(report_id, formato, token):
    if not token:
        return False
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT paid, download_token_hash FROM archivos WHERE report_id=? AND formato=?", (report_id, formato)).fetchone()
    return bool(row and row[0] == 1 and secrets.compare_digest(row[1], _hash(token)))


def marcar_pagado(report_id, formato):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        updated = db.execute("UPDATE archivos SET paid=1 WHERE report_id=? AND formato=?", (report_id, formato)).rowcount
    return updated == 1


def obtener_archivos(report_id):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        return db.execute("SELECT formato, ruta, paid FROM archivos WHERE report_id=? ORDER BY formato", (report_id,)).fetchall()
