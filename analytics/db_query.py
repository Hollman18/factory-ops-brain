#!/usr/bin/env python3
import argparse
from datetime import datetime, timedelta, date

import numpy as np
from scipy.stats import linregress, zscore

from analytics.common import emit, safe_float, get_conn, fetch_all, fetch_one


def month_days(d: date):
    next_month = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
    return (next_month - timedelta(days=1)).day


def capacity_mode(conn, args):
    sql = """
    SELECT pt.planta_id,
           SUM(pt.total_unidades) AS produccion_real,
           SUM(COALESCE(cmr.capacidad_turno_teorica, 0)) AS capacidad_nominal,
           SUM(pt.total_unidades) / NULLIF(SUM(COALESCE(cmr.capacidad_turno_teorica, 0)), 0) AS pct_operativo_actual,
           1.0 AS pct_nominal,
           (SUM(COALESCE(cmr.capacidad_turno_teorica, 0)) - SUM(pt.total_unidades)) AS gap_unidades,
           (1.0 - (SUM(pt.total_unidades) / NULLIF(SUM(COALESCE(cmr.capacidad_turno_teorica, 0)), 0))) AS gap_pct,
           SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_agregado,
           SUM(pt.disponibilidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS disponibilidad_agregada,
           SUM(pt.rendimiento * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS rendimiento_agregado,
           SUM(pt.calidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS calidad_agregada
    FROM produccion_turno pt
    LEFT JOIN capacidad_maquina_referencia cmr
      ON cmr.maquina_id = pt.maquina_id AND cmr.referencia_id = pt.referencia_id
    WHERE pt.planta_id = %(planta_id)s
      AND pt.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
      AND (%(maquina_id)s IS NULL OR pt.maquina_id = %(maquina_id)s)
    GROUP BY pt.planta_id
    """
    row = fetch_one(conn, sql, vars(args))
    if not row:
        emit({"status": "ok", "data": {}, "insight": "No hay datos para calcular capacidad en el rango consultado.", "recomendacion": "Validar capacidad nominal por referencia y carga de producción del periodo."})
    pct_operativo = safe_float(row.get("pct_operativo_actual"))
    disp = safe_float(row.get("disponibilidad_agregada"))
    rend = safe_float(row.get("rendimiento_agregado"))
    cal = safe_float(row.get("calidad_agregada"))
    if rend <= disp and rend <= cal:
        prioridad = "rendimiento"
        recomendacion_prioridad = "Subir velocidad efectiva, atacar microparadas y revisar capacidad por SKU."
    elif disp <= rend and disp <= cal:
        prioridad = "disponibilidad"
        recomendacion_prioridad = "Reducir averías y tiempos de setup con foco en equipos críticos."
    else:
        prioridad = "calidad"
        recomendacion_prioridad = "Reducir rechazo y retrabajo en referencias con peor first pass yield."
    emit({"status": "ok", "data": {"dominio": "produccion_capacidad", "planta_id": row.get("planta_id"), "%_operativo_actual": pct_operativo, "%_nominal": safe_float(row.get("pct_nominal")), "gap": safe_float(row.get("gap_pct")), "gap_unidades": safe_float(row.get("gap_unidades")), "produccion_real": safe_float(row.get("produccion_real")), "capacidad_nominal": safe_float(row.get("capacidad_nominal")), "oee_agregado": safe_float(row.get("oee_agregado")), "disponibilidad_agregada": disp, "rendimiento_agregado": rend, "calidad_agregada": cal, "recomendacion_prioridad": recomendacion_prioridad}, "insight": f"La planta está operando al {pct_operativo*100:.1f}% de su capacidad nominal y la principal brecha está en {prioridad}.", "recomendacion": recomendacion_prioridad})


def trend_mode(conn, args):
    sql = """
    SELECT pt.fecha::date AS fecha,
           SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee
    FROM produccion_turno pt
    WHERE pt.planta_id = %(planta_id)s
      AND pt.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
      AND (%(maquina_id)s IS NULL OR pt.maquina_id = %(maquina_id)s)
    GROUP BY pt.fecha::date
    ORDER BY pt.fecha::date ASC
    """
    rows = fetch_all(conn, sql, vars(args))
    if len(rows) < 2:
        emit({"status": "ok", "data": {"dominio": "tendencia_oee", "series": rows}, "insight": "No hay suficientes puntos para calcular tendencia lineal de OEE.", "recomendacion": "Ampliar el rango temporal o validar carga diaria."})
    xs = np.arange(1, len(rows) + 1, dtype=float)
    ys = np.array([safe_float(r['oee']) for r in rows], dtype=float)
    reg = linregress(xs, ys)
    fecha_fin_dt = datetime.strptime(args.fecha_fin, "%Y-%m-%d").date()
    projected = float(reg.slope * month_days(fecha_fin_dt) + reg.intercept)
    meta = safe_float(args.meta_mensual_oee, 0.85)
    riesgo = projected < meta
    emit({"status": "ok", "data": {"dominio": "tendencia_oee", "series": rows, "pendiente": reg.slope, "intercepto": reg.intercept, "proyeccion_fin_mes": projected, "meta_mensual_oee": meta, "riesgo_incumplir_meta": riesgo}, "insight": f"La pendiente del OEE proyecta un cierre de {projected*100:.1f}% frente a una meta de {meta*100:.1f}%.", "recomendacion": "Priorizar la línea con mayor deterioro si hay riesgo; sostener control diario si la tendencia es favorable."})


def anomaly_mode(conn, args):
    sql = """
    SELECT pt.maquina_id,
           m.nombre AS maquina_nombre,
           SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee,
           SUM(COALESCE(pt.l1_averia,0) + COALESCE(pt.l2_setup,0) + COALESCE(pt.l3_microparada,0)) AS tiempo_parada,
           AVG(COALESCE(pt.vel_real,0)) AS velocidad_real
    FROM produccion_turno pt
    JOIN maquinas m ON m.id = pt.maquina_id
    WHERE pt.planta_id = %(planta_id)s
      AND pt.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
      AND (%(maquina_id)s IS NULL OR pt.maquina_id = %(maquina_id)s)
    GROUP BY pt.maquina_id, m.nombre
    """
    rows = fetch_all(conn, sql, vars(args))
    if len(rows) < 3:
        emit({"status": "ok", "data": {"dominio": "anomalias_operativas", "series": rows, "anomalias": []}, "insight": "No hay suficientes entidades para Z-score robusto.", "recomendacion": "Ampliar el universo de comparación."})
    oee_vals = np.array([safe_float(r['oee']) for r in rows], dtype=float)
    stop_vals = np.array([safe_float(r['tiempo_parada']) for r in rows], dtype=float)
    speed_vals = np.array([safe_float(r['velocidad_real']) for r in rows], dtype=float)
    z_oee = zscore(oee_vals, nan_policy='omit')
    z_stop = zscore(stop_vals, nan_policy='omit')
    z_speed = zscore(speed_vals, nan_policy='omit')
    anomalies = []
    for i, r in enumerate(rows):
        if abs(z_oee[i]) > 2.5 or abs(z_stop[i]) > 2.5 or abs(z_speed[i]) > 2.5:
            anomalies.append({"entidad": r['maquina_nombre'], "oee": safe_float(r['oee']), "tiempo_parada": safe_float(r['tiempo_parada']), "velocidad_real": safe_float(r['velocidad_real']), "z_oee": float(abs(z_oee[i])) if not np.isnan(z_oee[i]) else 0.0, "z_tiempo_parada": float(abs(z_stop[i])) if not np.isnan(z_stop[i]) else 0.0, "z_velocidad_real": float(abs(z_speed[i])) if not np.isnan(z_speed[i]) else 0.0})
    emit({"status": "ok", "data": {"dominio": "anomalias_operativas", "series": rows, "anomalias": anomalies}, "insight": f"Se detectaron {len(anomalies)} entidades anómalas por OEE, paradas o velocidad.", "recomendacion": "Priorizar primero las anomalías simultáneas en OEE bajo y paradas altas."})


def pareto_mode(conn, args):
    sql = """
    SELECT cfcat.id AS categoria_id,
           cfcat.nombre AS categoria_nombre,
           SUM(ep.duracion_min) AS minutos_perdidos,
           COUNT(*) AS total_eventos,
           SUM(ep.duracion_min * COALESCE(m.costo_hora_parada, 0) / 60.0) AS costo_estimado
    FROM eventos_parada ep
    JOIN codigos_falla cf ON cf.id = ep.codigo_falla_id
    JOIN categorias_falla cfcat ON cfcat.id = cf.categoria_id
    JOIN maquinas m ON m.id = ep.maquina_id
    JOIN areas a ON a.id = m.area_id
    WHERE a.planta_id = %(planta_id)s
      AND ep.inicio BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
      AND (%(maquina_id)s IS NULL OR ep.maquina_id = %(maquina_id)s)
    GROUP BY cfcat.id, cfcat.nombre
    ORDER BY minutos_perdidos DESC, costo_estimado DESC
    LIMIT 10
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "pareto_perdidas", "top_causas": rows}, "insight": f"Se identificaron {len(rows)} causas principales de pérdida.", "recomendacion": "Atacar primero la categoría líder en minutos perdidos y costo estimado."})


def maintenance_mode(conn, args):
    sql = """
    SELECT ml.maquina_id, m.nombre AS maquina_nombre,
           AVG(ml.mtbf) AS mtbf_promedio,
           AVG(ml.mttr) AS mttr_promedio,
           AVG(ml.backlog) AS backlog_promedio,
           AVG(ml.cumplimiento_plan) AS cumplimiento_plan
    FROM mantenimiento_log ml
    JOIN maquinas m ON m.id = ml.maquina_id
    JOIN areas a ON a.id = m.area_id
    WHERE a.planta_id = %(planta_id)s
      AND ml.timestamp BETWEEN %(fecha_inicio)s::timestamp AND (%(fecha_fin)s::timestamp + INTERVAL '1 day')
      AND (%(maquina_id)s IS NULL OR ml.maquina_id = %(maquina_id)s)
    GROUP BY ml.maquina_id, m.nombre
    ORDER BY backlog_promedio DESC, mtbf_promedio ASC
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "maintenance", "rows": rows}, "insight": f"Se analizaron {len(rows)} equipos para mantenimiento.", "recomendacion": "Priorizar backlog alto, bajo MTBF y alto MTTR."})


def energy_mode(conn, args):
    sql = """
    SELECT DATE(ee.timestamp) AS fecha,
           SUM(ee.kwh) AS kwh_total,
           SUM(pt.total_unidades) AS total_unidades,
           SUM(ee.kwh) / NULLIF(SUM(pt.total_unidades), 0) AS kwh_por_unidad
    FROM energia_eventos ee
    JOIN maquinas m ON m.id = ee.maquina_id
    JOIN areas a ON a.id = m.area_id
    LEFT JOIN produccion_turno pt ON pt.maquina_id = ee.maquina_id AND pt.fecha = DATE(ee.timestamp)
    WHERE a.planta_id = %(planta_id)s
      AND DATE(ee.timestamp) BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
      AND (%(maquina_id)s IS NULL OR ee.maquina_id = %(maquina_id)s)
    GROUP BY DATE(ee.timestamp)
    ORDER BY fecha ASC
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "energy", "rows": rows}, "insight": f"Se calculó consumo energético para {len(rows)} días.", "recomendacion": "Comparar kWh por unidad contra baseline y estándar."})


def material_mode(conn, args):
    sql = """
    SELECT mpc.referencia_id,
           SUM(mpc.consumo_real) AS consumo_real,
           SUM(mpc.consumo_estandar) AS consumo_estandar,
           SUM(mpc.consumo_real) / NULLIF(SUM(mpc.consumo_estandar), 0) AS ratio_consumo_vs_estandar
    FROM materia_prima_consumo mpc
    WHERE mpc.planta_id = %(planta_id)s
      AND mpc.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
    GROUP BY mpc.referencia_id
    ORDER BY ratio_consumo_vs_estandar DESC
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "material", "rows": rows}, "insight": f"Se analizaron {len(rows)} referencias con consumo de materia prima.", "recomendacion": "Priorizar referencias con sobreconsumo frente al estándar."})


def traceability_mode(conn, args):
    sql = """
    SELECT mpc.lote_pt,
           mpc.lote_mp,
           mpc.referencia_id,
           SUM(mpc.consumo_real) AS consumo_real
    FROM materia_prima_consumo mpc
    WHERE mpc.planta_id = %(planta_id)s
      AND mpc.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s
    GROUP BY mpc.lote_pt, mpc.lote_mp, mpc.referencia_id
    ORDER BY consumo_real DESC
    LIMIT 100
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "traceability", "rows": rows}, "insight": f"Se recuperaron {len(rows)} relaciones lote PT ↔ lote MP.", "recomendacion": "Usar esta salida para trazabilidad ascendente y descendente."})


def spc_mode(conn, args):
    sql = """
    SELECT pm.nombre AS punto_nombre,
           COUNT(*) AS total_fuera_especificacion,
           AVG(lv.valor) AS promedio_valor,
           MIN(lv.valor) AS minimo,
           MAX(lv.valor) AS maximo
    FROM lecturas_variable lv
    JOIN puntos_medicion pm ON pm.id = lv.punto_id
    WHERE lv.timestamp BETWEEN %(fecha_inicio)s::timestamp AND (%(fecha_fin)s::timestamp + INTERVAL '1 day')
    GROUP BY pm.nombre
    ORDER BY total_fuera_especificacion DESC, punto_nombre ASC
    """
    rows = fetch_all(conn, sql, vars(args))
    emit({"status": "ok", "data": {"dominio": "spc", "rows": rows}, "insight": f"Se analizaron {len(rows)} puntos de proceso/SPC.", "recomendacion": "Priorizar puntos con más eventos fuera de especificación o deriva de promedio."})


def build_parser():
    p = argparse.ArgumentParser(description='Factory Ops Brain analytics db_query.py')
    p.add_argument('--query-type', required=True, choices=['capacity', 'trend', 'anomaly', 'pareto', 'maintenance', 'energy', 'material', 'traceability', 'spc'])
    p.add_argument('--planta-id', required=True)
    p.add_argument('--fecha-inicio', required=True)
    p.add_argument('--fecha-fin', required=True)
    p.add_argument('--maquina-id', required=False, default=None)
    p.add_argument('--meta-mensual-oee', required=False, type=float, default=0.85)
    return p


def main():
    args = build_parser().parse_args()
    conn = get_conn()
    try:
        if args.query_type == 'capacity':
            capacity_mode(conn, args)
        elif args.query_type == 'trend':
            trend_mode(conn, args)
        elif args.query_type == 'anomaly':
            anomaly_mode(conn, args)
        elif args.query_type == 'pareto':
            pareto_mode(conn, args)
        elif args.query_type == 'maintenance':
            maintenance_mode(conn, args)
        elif args.query_type == 'energy':
            energy_mode(conn, args)
        elif args.query_type == 'material':
            material_mode(conn, args)
        elif args.query_type == 'traceability':
            traceability_mode(conn, args)
        elif args.query_type == 'spc':
            spc_mode(conn, args)
        else:
            emit({'status': 'error', 'detail': 'Tipo de query no soportado'}, 1)
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()
