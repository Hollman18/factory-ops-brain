#!/usr/bin/env python3
import argparse
import time
import numpy as np

from analytics.common import emit, safe_float, get_conn, fetch_all, fetch_one

MAX_SECONDS = 10.0
START_TS = time.time()


def elapsed():
    return time.time() - START_TS


def actor_sugerido(metrica):
    return {
        'oee': 'supervisor',
        'disponibilidad': 'mantenimiento',
        'rendimiento': 'jefe_produccion',
        'calidad': 'calidad',
        'energia': 'energia',
        'mantenimiento': 'mantenimiento',
        'spc': 'calidad',
        'materia_prima': 'produccion',
    }.get(metrica, 'supervisor')


def causa_probable(metrica, valor_actual, valor_esperado):
    return {
        'oee': 'deterioro_integral_operativo',
        'disponibilidad': 'paradas_no_planificadas_o_averias',
        'rendimiento': 'microparadas_o_velocidad_reducida',
        'calidad': 'rechazo_retrabajo_o_desviacion_de_proceso',
        'energia': 'sobreconsumo_o_baja_eficiencia_energetica',
        'mantenimiento': 'baja_confiabilidad_o_backlog_elevado',
        'spc': 'variable_fuera_de_control',
        'materia_prima': 'sobreconsumo_o_merma_de_mp',
    }.get(metrica, 'desviacion_operativa')


def recomendacion(metrica, entidad):
    return {
        'oee': f'Priorizar revisión integral de {entidad}: disponibilidad, rendimiento y calidad.',
        'disponibilidad': f'Revisar paradas no planificadas, averías y setups en {entidad}.',
        'rendimiento': f'Revisar velocidad efectiva, microparadas y restricciones operativas en {entidad}.',
        'calidad': f'Revisar rechazo, retrabajo y condiciones de proceso en {entidad}.',
        'energia': f'Validar consumo específico, baseline y desvíos energéticos en {entidad}.',
        'mantenimiento': f'Revisar confiabilidad, backlog y tiempos de reparación en {entidad}.',
        'spc': f'Revisar variables fuera de especificación y estabilidad del proceso en {entidad}.',
        'materia_prima': f'Revisar consumo real vs estándar y trazabilidad en {entidad}.',
    }.get(metrica, f'Revisar la desviación detectada en {entidad}.')


def active_machines(conn, planta_id):
    return fetch_all(conn, """
    SELECT m.id AS maquina_id, m.nombre AS maquina_nombre, p.id AS planta_id
    FROM maquinas m
    JOIN areas a ON a.id = m.area_id
    JOIN plantas p ON p.id = a.planta_id
    WHERE COALESCE(m.activo, TRUE) = TRUE AND p.id = %(planta_id)s
    """, {"planta_id": planta_id})


def last_two_turns(conn, maquina_id):
    return fetch_all(conn, """
    SELECT pt.turno_id, pt.fecha,
           SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS oee,
           SUM(pt.disponibilidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS disponibilidad,
           SUM(pt.rendimiento * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS rendimiento,
           SUM(pt.calidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS calidad
    FROM produccion_turno pt
    WHERE pt.maquina_id = %(maquina_id)s
    GROUP BY pt.turno_id, pt.fecha
    ORDER BY pt.fecha DESC, pt.turno_id DESC
    LIMIT 2
    """, {"maquina_id": maquina_id})


def last_three_turns(conn, maquina_id):
    return fetch_all(conn, """
    SELECT * FROM (
      SELECT pt.turno_id, pt.fecha,
             SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS oee,
             SUM(pt.disponibilidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS disponibilidad,
             SUM(pt.rendimiento * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS rendimiento,
             SUM(pt.calidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS calidad
      FROM produccion_turno pt
      WHERE pt.maquina_id = %(maquina_id)s
      GROUP BY pt.turno_id, pt.fecha
      ORDER BY pt.fecha DESC, pt.turno_id DESC
      LIMIT 3
    ) x ORDER BY fecha ASC, turno_id ASC
    """, {"maquina_id": maquina_id})


def baseline_7d(conn, maquina_id):
    return fetch_all(conn, """
    SELECT pt.fecha,
           SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS oee,
           SUM(pt.disponibilidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS disponibilidad,
           SUM(pt.rendimiento * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS rendimiento,
           SUM(pt.calidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades),0) AS calidad
    FROM produccion_turno pt
    WHERE pt.maquina_id = %(maquina_id)s AND pt.fecha >= CURRENT_DATE - INTERVAL '7 day'
    GROUP BY pt.fecha
    ORDER BY pt.fecha ASC
    """, {"maquina_id": maquina_id})


def meta(conn, maquina_id, metrica):
    return fetch_one(conn, """
    SELECT meta_valor, meta_minima, meta_critica, meta_excelencia
    FROM metas_indicadores
    WHERE nivel='maquina' AND entidad_id=%(maquina_id)s AND tipo_indicador=%(metrica)s
    ORDER BY vigente_desde DESC NULLS LAST LIMIT 1
    """, {"maquina_id": maquina_id, "metrica": metrica})


def detect_metric(entidad, latest, base, mt, metrica):
    out = []
    actual = safe_float(latest.get(metrica))
    esperado = safe_float(mt.get('meta_valor')) if mt else None
    critica = safe_float(mt.get('meta_critica')) if mt and mt.get('meta_critica') is not None else None
    minima = safe_float(mt.get('meta_minima')) if mt and mt.get('meta_minima') is not None else None
    if mt and actual < safe_float(mt.get('meta_valor')):
        sev = 'critica' if (critica is not None and actual < critica) else ('media' if (minima is not None and actual < minima) else 'baja')
        out.append({"severidad": sev, "entidad": entidad, "metrica": metrica, "valor_actual": actual, "valor_esperado": esperado, "causa_probable": causa_probable(metrica, actual, esperado), "quien_debe_actuar": actor_sugerido(metrica), "recomendacion": recomendacion(metrica, entidad)})
    vals = np.array([safe_float(x.get(metrica)) for x in base], dtype=float)
    if len(vals) >= 3 and np.nanstd(vals) > 0:
        z = float((actual - np.nanmean(vals)) / np.nanstd(vals))
        if abs(z) > 2.5:
            out.append({"severidad": 'critica' if abs(z) > 3.5 else 'media', "entidad": entidad, "metrica": metrica, "valor_actual": actual, "valor_esperado": float(np.nanmean(vals)), "causa_probable": causa_probable(metrica, actual, float(np.nanmean(vals))), "quien_debe_actuar": actor_sugerido(metrica), "recomendacion": recomendacion(metrica, entidad)})
    return out


def detect_trend(entidad, rows):
    if len(rows) < 3:
        return []
    out = []
    for metrica in ['oee', 'disponibilidad', 'rendimiento', 'calidad']:
        vals = [safe_float(x.get(metrica)) for x in rows]
        if vals[0] > vals[1] > vals[2]:
            out.append({"severidad": 'media', "entidad": entidad, "metrica": metrica, "valor_actual": vals[-1], "valor_esperado": vals[0], "causa_probable": 'tendencia_negativa_sostenida', "quien_debe_actuar": actor_sugerido(metrica), "recomendacion": f'Tendencia negativa sostenida en {metrica} durante 3 turnos consecutivos en {entidad}.'})
    return out


def energy_check(conn, planta_id):
    row = fetch_one(conn, """
    SELECT a.planta_id, SUM(ee.kwh) AS kwh_24h, AVG(d.kwh_dia) AS baseline_kwh_dia
    FROM energia_eventos ee
    JOIN maquinas m ON m.id = ee.maquina_id
    JOIN areas a ON a.id = m.area_id
    LEFT JOIN (
      SELECT a2.planta_id, DATE(ee2.timestamp) AS fecha, SUM(ee2.kwh) AS kwh_dia
      FROM energia_eventos ee2
      JOIN maquinas m2 ON m2.id = ee2.maquina_id
      JOIN areas a2 ON a2.id = m2.area_id
      WHERE DATE(ee2.timestamp) >= CURRENT_DATE - INTERVAL '7 day'
      GROUP BY a2.planta_id, DATE(ee2.timestamp)
    ) d ON d.planta_id = a.planta_id
    WHERE a.planta_id = %(planta_id)s AND ee.timestamp >= NOW() - INTERVAL '24 hour'
    GROUP BY a.planta_id
    """, {"planta_id": planta_id})
    if not row: return []
    actual = safe_float(row.get('kwh_24h')); esperado = safe_float(row.get('baseline_kwh_dia'))
    if esperado > 0 and actual > esperado * 1.20:
        return [{"severidad": 'media', "entidad": f'planta:{planta_id}', "metrica": 'energia', "valor_actual": actual, "valor_esperado": esperado, "causa_probable": causa_probable('energia', actual, esperado), "quien_debe_actuar": actor_sugerido('energia'), "recomendacion": recomendacion('energia', f'planta {planta_id}') }]
    return []


def spc_check(conn, planta_id):
    rows = fetch_all(conn, """
    SELECT pm.nombre AS punto_nombre, COUNT(*) AS total_fuera
    FROM lecturas_variable lv
    JOIN puntos_medicion pm ON pm.id = lv.punto_id
    WHERE lv.timestamp >= NOW() - INTERVAL '24 hour' AND lv.en_alarma = TRUE
    GROUP BY pm.nombre ORDER BY total_fuera DESC LIMIT 3
    """)
    return [{"severidad": 'media', "entidad": r['punto_nombre'], "metrica": 'spc', "valor_actual": safe_float(r['total_fuera']), "valor_esperado": 0, "causa_probable": causa_probable('spc', safe_float(r['total_fuera']), 0), "quien_debe_actuar": actor_sugerido('spc'), "recomendacion": recomendacion('spc', r['punto_nombre'])} for r in rows]


def mp_check(conn, planta_id):
    rows = fetch_all(conn, """
    SELECT referencia_id, SUM(consumo_real) AS consumo_real, SUM(consumo_estandar) AS consumo_estandar
    FROM materia_prima_consumo
    WHERE planta_id = %(planta_id)s AND fecha >= CURRENT_DATE - INTERVAL '7 day'
    GROUP BY referencia_id
    HAVING SUM(consumo_real) / NULLIF(SUM(consumo_estandar), 0) > 1.10
    ORDER BY SUM(consumo_real) / NULLIF(SUM(consumo_estandar), 0) DESC LIMIT 3
    """, {"planta_id": planta_id})
    return [{"severidad": 'baja', "entidad": f"referencia:{r['referencia_id']}", "metrica": 'materia_prima', "valor_actual": safe_float(r['consumo_real']), "valor_esperado": safe_float(r['consumo_estandar']), "causa_probable": causa_probable('materia_prima', safe_float(r['consumo_real']), safe_float(r['consumo_estandar'])), "quien_debe_actuar": actor_sugerido('materia_prima'), "recomendacion": recomendacion('materia_prima', f"referencia {r['referencia_id']}")} for r in rows]


def main():
    parser = argparse.ArgumentParser(description='Factory Ops Brain anomaly detector for heartbeat')
    parser.add_argument('--planta-id', required=True)
    args = parser.parse_args()

    conn = get_conn()
    try:
        maquinas = active_machines(conn, args.planta_id)
        anomalias = []
        for m in maquinas:
            if elapsed() > MAX_SECONDS: break
            entidad = f"maquina:{m['maquina_nombre']}"
            last2 = last_two_turns(conn, m['maquina_id'])
            if last2:
                latest = last2[0]
                base = baseline_7d(conn, m['maquina_id'])
                for metrica in ['oee', 'disponibilidad', 'rendimiento', 'calidad']:
                    anomalias.extend(detect_metric(entidad, latest, base, meta(conn, m['maquina_id'], metrica), metrica))
            anomalias.extend(detect_trend(entidad, last_three_turns(conn, m['maquina_id'])))
        anomalias.extend(energy_check(conn, args.planta_id))
        anomalias.extend(spc_check(conn, args.planta_id))
        anomalias.extend(mp_check(conn, args.planta_id))

        uniq = []
        seen = set()
        for a in anomalias:
            key = (a['entidad'], a['metrica'], a['severidad'], round(float(a['valor_actual']), 6), round(float(a['valor_esperado']), 6))
            if key not in seen:
                seen.add(key)
                uniq.append(a)
        order = {'critica': 0, 'media': 1, 'baja': 2}
        uniq.sort(key=lambda x: order.get(x['severidad'], 9))
        emit({"status": "ok", "anomalias": uniq, "elapsed_seconds": round(elapsed(), 3)})
    except Exception as e:
        emit({"status": "error", "anomalias": [], "detail": str(e), "elapsed_seconds": round(elapsed(), 3)}, 1)
    finally:
        try: conn.close()
        except Exception: pass


if __name__ == '__main__':
    main()
