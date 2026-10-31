import json
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone

from config import OUTPUT_DIR, ARCHIVO_BASE_DATOS

OWNER_TOKEN_HOURS = 24
DOWNLOAD_TOKEN_MINUTES = 15


def _utcnow():
    return datetime.now(timezone.utc)


def _iso(value):
    return value.isoformat()


def _migrar_columnas(db, tabla, columnas):
    existentes = {row[1] for row in db.execute(f"PRAGMA table_info({tabla})")}
    for nombre, definicion in columnas.items():
        if nombre not in existentes:
            db.execute(f"ALTER TABLE {tabla} ADD COLUMN {nombre} {definicion}")


def inicializar_db():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS reportes (
            id TEXT PRIMARY KEY, created_at TEXT NOT NULL, timezone TEXT NOT NULL,
            language TEXT NOT NULL, currency TEXT NOT NULL, crypto_ids TEXT NOT NULL,
            status TEXT NOT NULL, owner_token_hash TEXT NOT NULL,
            expires_at TEXT, revoked_at TEXT, ranking_source TEXT NOT NULL DEFAULT 'unknown'
        );
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cripto TEXT NOT NULL,
            precio REAL NOT NULL, fecha TEXT NOT NULL, report_id TEXT
        );
        CREATE TABLE IF NOT EXISTS archivos (
            report_id TEXT NOT NULL, formato TEXT NOT NULL, ruta TEXT NOT NULL,
            download_token_hash TEXT NOT NULL, paid INTEGER NOT NULL DEFAULT 0,
            created_at TEXT, expires_at TEXT, revoked_at TEXT, used_at TEXT,
            PRIMARY KEY (report_id, formato)
        );
        """)
        _migrar_columnas(db, "reportes", {
            "expires_at": "TEXT", "revoked_at": "TEXT",
            "ranking_source": "TEXT NOT NULL DEFAULT 'unknown'",
        })
        _migrar_columnas(db, "historial", {"report_id": "TEXT"})
        _migrar_columnas(db, "archivos", {
            "created_at": "TEXT", "expires_at": "TEXT", "revoked_at": "TEXT", "used_at": "TEXT",
        })


def _hash(token):
    import hashlib
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def crear_reporte(report_id, crypto_ids, timezone_name, language, currency, ranking_source="unknown"):
    inicializar_db()
    owner_token = secrets.token_urlsafe(32)
    now = _utcnow()
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.execute("""INSERT INTO reportes
            (id, created_at, timezone, language, currency, crypto_ids, status,
             owner_token_hash, expires_at, revoked_at, ranking_source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?)""", (
            report_id, _iso(now), timezone_name, language, currency,
            json.dumps(crypto_ids), "generated", _hash(owner_token),
            _iso(now + timedelta(hours=OWNER_TOKEN_HOURS)), ranking_source,
        ))
    return owner_token


def validar_propietario(report_id, token):
    if not token:
        return False
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT owner_token_hash, expires_at, revoked_at FROM reportes WHERE id=?", (report_id,)).fetchone()
    if not row or not secrets.compare_digest(row[0], _hash(token)) or row[2]:
        return False
    return not row[1] or datetime.fromisoformat(row[1]) > _utcnow()


def revocar_propietario(report_id):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        return db.execute("UPDATE reportes SET revoked_at=? WHERE id=?", (_iso(_utcnow()), report_id)).rowcount == 1


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
    now = _utcnow()
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        db.execute("""INSERT OR REPLACE INTO archivos
            (report_id, formato, ruta, download_token_hash, paid, created_at, expires_at, revoked_at, used_at)
            VALUES (?, ?, ?, ?, 0, ?, ?, NULL, NULL)""", (
            report_id, formato, str(ruta), _hash(token), _iso(now),
            _iso(now + timedelta(minutes=DOWNLOAD_TOKEN_MINUTES)),
        ))
    return token


def autorizar_descarga(report_id, formato, token):
    if not token:
        return False
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT paid, download_token_hash, expires_at, revoked_at FROM archivos WHERE report_id=? AND formato=?", (report_id, formato)).fetchone()
        if not row or row[0] != 1 or row[3]:
            return False
        if not secrets.compare_digest(row[1], _hash(token)):
            return False
        if row[2] and datetime.fromisoformat(row[2]) <= _utcnow():
            return False
        db.execute("UPDATE archivos SET used_at=? WHERE report_id=? AND formato=?", (_iso(_utcnow()), report_id, formato))
        return True


def marcar_pagado(report_id, formato):
    """Simula el pago y emite un token de descarga válido durante 15 minutos."""
    token = secrets.token_urlsafe(32)
    now = _utcnow()
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        updated = db.execute("""UPDATE archivos
            SET paid=1, download_token_hash=?, created_at=?, expires_at=?, revoked_at=NULL, used_at=NULL
            WHERE report_id=? AND formato=?""", (
            _hash(token), _iso(now), _iso(now + timedelta(minutes=DOWNLOAD_TOKEN_MINUTES)),
            report_id, formato,
        )).rowcount
    return token if updated == 1 else None


def revocar_descarga(report_id, formato):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        return db.execute("UPDATE archivos SET revoked_at=? WHERE report_id=? AND formato=?", (_iso(_utcnow()), report_id, formato)).rowcount == 1


def obtener_archivos(report_id):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        return db.execute("SELECT formato, ruta, paid, expires_at, revoked_at, used_at FROM archivos WHERE report_id=? ORDER BY formato", (report_id,)).fetchall()


def obtener_estado_archivos(report_id):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        rows = db.execute("SELECT formato, paid, expires_at, revoked_at FROM archivos WHERE report_id=? ORDER BY formato", (report_id,)).fetchall()
    return [{"formato": r[0], "pagado": bool(r[1]), "disponible": not bool(r[3]) and (not r[2] or datetime.fromisoformat(r[2]) > _utcnow())} for r in rows]


def obtener_fuente_ranking(report_id):
    with sqlite3.connect(ARCHIVO_BASE_DATOS) as db:
        row = db.execute("SELECT ranking_source FROM reportes WHERE id=?", (report_id,)).fetchone()
    return row[0] if row else None
