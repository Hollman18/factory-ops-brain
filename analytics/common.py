#!/usr/bin/env python3
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def emit(payload, code=0):
    print(json.dumps(payload, ensure_ascii=False, default=str))
    raise SystemExit(code)


def safe_float(v, default=0.0):
    try:
        if v is None:
            return default
        return float(v)
    except Exception:
        return default


def get_conn():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        emit({'status': 'error', 'detail': 'DATABASE_URL no configurada'}, 1)
    try:
        return psycopg2.connect(db_url, connect_timeout=3)
    except Exception as e:
        emit({'status': 'error', 'detail': f'No fue posible conectar a PostgreSQL: {e}'}, 1)


def fetch_all(conn, sql, params=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params or {})
        return [dict(r) for r in cur.fetchall()]


def fetch_one(conn, sql, params=None):
    rows = fetch_all(conn, sql, params)
    return rows[0] if rows else None
