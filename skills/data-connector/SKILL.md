---
name: data-connector
description: Conecta al agente a la base de datos PostgreSQL del cliente usando DATABASE_URL, ejecuta queries SQL vía exec con psql o mediante analytics/db_query.py, parsea resultados y responde con datos operativos para producción, OEE, mantenimiento, energía, trazabilidad, materia prima y SPC.
---

# Skill: data-connector

## Propósito
Esta skill conecta el agente a PostgreSQL del cliente y reutiliza `DATA_MODEL.md`, `QUERIES.md` y `analytics/db_query.py`.

## Fuente oficial de configuración del cliente
Ruta operativa preferida:
- `CLIENT_CONFIG.json` en la raíz del workspace

Ruta template / fallback:
- `workspace-template/CLIENT_CONFIG.json`

El agente debe buscar primero en raíz y luego en `workspace-template/`.

## Seguridad
- Solo `SELECT` o `WITH ... SELECT`
- Nunca exponer `DATABASE_URL`
- No interpolar texto libre del usuario directamente en SQL

## Cómo leer DATABASE_URL
```bash
bash -lc 'test -n "$DATABASE_URL" && echo OK || echo MISSING_DATABASE_URL'
```

## Cómo obtener `planta_id`
```bash
python3 - <<'PY'
import json, os
paths=['CLIENT_CONFIG.json','workspace-template/CLIENT_CONFIG.json']
for p in paths:
    if os.path.exists(p):
        d=json.load(open(p))
        print(d.get('planta_id') or d.get('default_planta_id') or d.get('context',{}).get('planta_id') or d.get('client',{}).get('planta_id') or '')
        break
PY
```

## Cuándo usar `exec + psql`
- consultas simples
- validación rápida
- depuración

## Cuándo usar `analytics/db_query.py`
- tendencia
- anomalías
- Pareto
- análisis más complejos

## Comando exacto con psql
```bash
psql "$DATABASE_URL" -c "SELECT ..." --csv -t
```

## Regla de respuesta
Responder con:
1. qué está pasando
2. qué tan grave es
3. qué lo impulsa
4. qué hacer después
