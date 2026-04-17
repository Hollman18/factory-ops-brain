#!/usr/bin/env python3
import json
from analytics.common import get_conn, fetch_all, emit

REQUIRED = {
    'produccion_turno': ['planta_id','linea_id','area_id','maquina_id','turno_id','referencia_id','fecha','total_unidades','und_buenas','desperdicio','retrabajo','oee','disponibilidad','rendimiento','calidad','vel_real','vel_ideal','t_operativo','t_productivo','t_parada','t_micro'],
    'metas_indicadores': ['nivel','entidad_id','tipo_indicador','meta_valor','meta_minima','meta_critica','meta_excelencia'],
    'maquinas': ['id','nombre','linea_id','area_id'],
    'lineas_produccion': ['id','nombre','area_id'],
    'areas': ['id','nombre','planta_id'],
    'plantas': ['id','nombre'],
    'referencias_producto': ['id','nombre'],
    'capacidad_maquina_referencia': ['maquina_id','referencia_id','capacidad_turno_teorica','velocidad_ideal'],
}

conn = get_conn()
rows = fetch_all(conn, """
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, column_name
""")
existing = {}
for r in rows:
    existing.setdefault(r['table_name'], set()).add(r['column_name'])

missing_tables = []
missing_columns = {}
for table, cols in REQUIRED.items():
    if table not in existing:
        missing_tables.append(table)
        continue
    missing = [c for c in cols if c not in existing[table]]
    if missing:
        missing_columns[table] = missing

status = 'ok' if not missing_tables and not missing_columns else 'error'
emit({
    'status': status,
    'data': {
        'missing_tables': missing_tables,
        'missing_columns': missing_columns,
    },
    'insight': 'Schema validado' if status == 'ok' else 'Schema incompatible con el contrato mínimo',
    'recomendacion': 'Ajustar mapping o esquema antes de desplegar' if status != 'ok' else 'Esquema compatible'
}, 0 if status == 'ok' else 1)
