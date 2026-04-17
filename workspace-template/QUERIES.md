# QUERIES.md

Archivo de consultas SQL listas para usar por el agente. La intención es que el agente copie y parametrice estas queries en lugar de generarlas desde cero.

Reglas globales:
- usar `NULLIF` en toda división
- nunca usar promedio simple para OEE ni sus pilares en niveles agregados
- para OEE agregado usar siempre: `SUM(oee * total_unidades) / SUM(total_unidades)`
- para energía, materia prima y trazabilidad preferir sumas, razones específicas y comparaciones contra línea base / estándar
- para SPC preferir consultas por ventana, límites y tendencia antes que promedios simples

---

# Grupo 1 — Producción, OEE y capacidad

## Q1. OEE actual del día por planta
**Parámetros:** `:planta_id`, `:fecha`
```sql
SELECT pt.planta_id,
       SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_actual_dia,
       SUM(pt.disponibilidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS disponibilidad_actual_dia,
       SUM(pt.rendimiento * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS rendimiento_actual_dia,
       SUM(pt.calidad * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS calidad_actual_dia,
       SUM(pt.total_unidades) AS total_unidades
FROM produccion_turno pt
WHERE pt.planta_id = :planta_id AND pt.fecha = :fecha
GROUP BY pt.planta_id;
```
**Responde:** OEE y pilares del día con ponderación correcta.

## Q2. % capacidad operativa vs nominal
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT pt.planta_id,
       SUM(pt.total_unidades) AS produccion_real,
       SUM(cmr.capacidad_turno_teorica) AS capacidad_nominal_total,
       SUM(pt.total_unidades) / NULLIF(SUM(cmr.capacidad_turno_teorica), 0) AS pct_capacidad_operativa
FROM produccion_turno pt
LEFT JOIN capacidad_maquina_referencia cmr
  ON cmr.maquina_id = pt.maquina_id AND cmr.referencia_id = pt.referencia_id
WHERE pt.planta_id = :planta_id
  AND pt.fecha BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY pt.planta_id;
```
**Responde:** Uso de capacidad operativa vs nominal.

## Q3. Producción real vs meta del turno
**Parámetros:** `:planta_id`, `:turno_id`, `:fecha`
```sql
SELECT pt.turno_id,
       SUM(pt.total_unidades) AS produccion_real,
       mi.meta_valor AS meta_turno,
       SUM(pt.total_unidades) / NULLIF(mi.meta_valor, 0) AS pct_cumplimiento_meta
FROM produccion_turno pt
JOIN metas_indicadores mi
  ON mi.nivel = 'planta'
 AND mi.entidad_id = pt.planta_id
 AND mi.tipo_indicador = 'produccion_turno'
 AND (mi.turno_id = pt.turno_id OR mi.turno_id IS NULL)
WHERE pt.planta_id = :planta_id
  AND pt.turno_id = :turno_id
  AND pt.fecha = :fecha
GROUP BY pt.turno_id, mi.meta_valor;
```
**Responde:** Producción real del turno frente a meta.

## Q4. Top 5 máquinas con menor OEE últimos 7 días
**Parámetros:** `:planta_id`, `:fecha_fin`
```sql
SELECT pt.maquina_id,
       m.nombre AS maquina_nombre,
       SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_7d,
       SUM(pt.total_unidades) AS total_unidades
FROM produccion_turno pt
JOIN maquinas m ON m.id = pt.maquina_id
WHERE pt.planta_id = :planta_id
  AND pt.fecha BETWEEN (:fecha_fin::date - INTERVAL '6 day') AND :fecha_fin
GROUP BY pt.maquina_id, m.nombre
ORDER BY oee_7d ASC
LIMIT 5;
```
**Responde:** Máquinas con peor OEE reciente.

## Q5. Producción esta semana vs semana anterior
**Parámetros:** `:planta_id`, `:inicio_semana_actual`, `:fin_semana_actual`, `:inicio_semana_anterior`, `:fin_semana_anterior`
```sql
SELECT actual.produccion_semana_actual,
       anterior.produccion_semana_anterior,
       actual.produccion_semana_actual - anterior.produccion_semana_anterior AS delta_unidades,
       (actual.produccion_semana_actual - anterior.produccion_semana_anterior)
         / NULLIF(anterior.produccion_semana_anterior, 0) AS delta_pct
FROM (
  SELECT SUM(total_unidades) AS produccion_semana_actual
  FROM produccion_turno
  WHERE planta_id = :planta_id
    AND fecha BETWEEN :inicio_semana_actual AND :fin_semana_actual
) actual,
(
  SELECT SUM(total_unidades) AS produccion_semana_anterior
  FROM produccion_turno
  WHERE planta_id = :planta_id
    AND fecha BETWEEN :inicio_semana_anterior AND :fin_semana_anterior
) anterior;
```
**Responde:** Cambio semanal de producción.

---

# Grupo 2 — Anomalías y alertas

## Q6. Máquinas bajo meta crítica hoy
**Parámetros:** `:planta_id`, `:fecha`
```sql
SELECT pt.maquina_id,
       m.nombre AS maquina_nombre,
       SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_hoy,
       mi.meta_critica
FROM produccion_turno pt
JOIN maquinas m ON m.id = pt.maquina_id
JOIN metas_indicadores mi
  ON mi.nivel = 'maquina'
 AND mi.entidad_id = pt.maquina_id
 AND mi.tipo_indicador = 'oee'
WHERE pt.planta_id = :planta_id
  AND pt.fecha = :fecha
GROUP BY pt.maquina_id, m.nombre, mi.meta_critica
HAVING SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) < mi.meta_critica
ORDER BY oee_hoy ASC;
```
**Responde:** Máquinas bajo umbral crítico.

## Q7. Líneas con tendencia negativa >10% vs 7 días
**Parámetros:** `:planta_id`, `:fecha`
```sql
WITH hoy AS (
  SELECT pt.linea_id,
         SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_hoy
  FROM produccion_turno pt
  WHERE pt.planta_id = :planta_id AND pt.fecha = :fecha
  GROUP BY pt.linea_id
), hist AS (
  SELECT pt.linea_id,
         SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_7d
  FROM produccion_turno pt
  WHERE pt.planta_id = :planta_id
    AND pt.fecha BETWEEN (:fecha::date - INTERVAL '7 day') AND (:fecha::date - INTERVAL '1 day')
  GROUP BY pt.linea_id
)
SELECT h.linea_id,
       lp.nombre AS linea_nombre,
       h.oee_hoy,
       hist.oee_7d,
       (h.oee_hoy - hist.oee_7d) / NULLIF(hist.oee_7d, 0) AS delta_pct
FROM hoy h
JOIN hist ON hist.linea_id = h.linea_id
JOIN lineas_produccion lp ON lp.id = h.linea_id
WHERE (h.oee_hoy - hist.oee_7d) / NULLIF(hist.oee_7d, 0) <= -0.10
ORDER BY delta_pct ASC;
```
**Responde:** Líneas deteriorándose rápidamente.

## Q8. Equipos con más de X paradas no planificadas 24h
**Parámetros:** `:planta_id`, `:fecha_corte`, `:min_eventos`
```sql
SELECT ep.maquina_id,
       m.nombre AS maquina_nombre,
       COUNT(*) AS total_paradas_noplan,
       SUM(ep.duracion_min) AS total_minutos
FROM eventos_parada ep
JOIN maquinas m ON m.id = ep.maquina_id
JOIN areas a ON a.id = m.area_id
WHERE a.planta_id = :planta_id
  AND ep.tipo_parada = 'no_planificada'
  AND ep.inicio BETWEEN (:fecha_corte::timestamp - INTERVAL '24 hour') AND :fecha_corte
GROUP BY ep.maquina_id, m.nombre
HAVING COUNT(*) > :min_eventos
ORDER BY total_paradas_noplan DESC, total_minutos DESC;
```
**Responde:** Equipos con alta recurrencia de paradas.

## Q9. Variables de proceso fuera de límites en turno
**Parámetros:** `:turno_id`, `:fecha`
```sql
SELECT lv.punto_id,
       pm.nombre AS punto_nombre,
       tvp.nombre AS variable_nombre,
       lv.valor,
       lv.timestamp,
       lv.tipo_alarma
FROM lecturas_variable lv
JOIN puntos_medicion pm ON pm.id = lv.punto_id
JOIN tipos_variable_proceso tvp ON tvp.id = pm.tipo_variable_id
WHERE lv.turno_id = :turno_id
  AND DATE(lv.timestamp) = :fecha
  AND lv.en_alarma = TRUE
ORDER BY lv.timestamp DESC;
```
**Responde:** Variables fuera de límites en el turno actual.

---

# Grupo 3 — Mantenimiento

## Q10. MTBF y MTTR por máquina últimos 30 días
**Parámetros:** `:planta_id`, `:fecha_corte`
```sql
SELECT ml.maquina_id,
       m.nombre AS maquina_nombre,
       AVG(ml.mtbf) AS mtbf_promedio,
       AVG(ml.mttr) AS mttr_promedio,
       COUNT(*) AS total_eventos
FROM mantenimiento_log ml
JOIN maquinas m ON m.id = ml.maquina_id
JOIN areas a ON a.id = m.area_id
WHERE a.planta_id = :planta_id
  AND ml.timestamp BETWEEN (:fecha_corte::date - INTERVAL '30 day') AND :fecha_corte
GROUP BY ml.maquina_id, m.nombre
ORDER BY mtbf_promedio ASC, mttr_promedio DESC;
```
**Responde:** Estado de confiabilidad y mantenibilidad.

## Q11. Pareto de fallas por categoría
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT cfcat.id AS categoria_id,
       cfcat.nombre AS categoria_nombre,
       SUM(ep.duracion_min) AS minutos_perdidos,
       COUNT(*) AS total_eventos
FROM eventos_parada ep
JOIN codigos_falla cf ON cf.id = ep.codigo_falla_id
JOIN categorias_falla cfcat ON cfcat.id = cf.categoria_id
JOIN maquinas m ON m.id = ep.maquina_id
JOIN areas a ON a.id = m.area_id
WHERE a.planta_id = :planta_id
  AND ep.inicio BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY cfcat.id, cfcat.nombre
ORDER BY minutos_perdidos DESC
LIMIT 10;
```
**Responde:** Categorías de falla más costosas en tiempo.

## Q12. Equipos con backlog alto o confiabilidad baja
**Parámetros:** `:planta_id`, `:fecha_corte`
```sql
SELECT ml.maquina_id,
       m.nombre AS maquina_nombre,
       AVG(ml.mtbf) AS mtbf_promedio,
       AVG(ml.mttr) AS mttr_promedio,
       AVG(ml.backlog) AS backlog_promedio
FROM mantenimiento_log ml
JOIN maquinas m ON m.id = ml.maquina_id
JOIN areas a ON a.id = m.area_id
WHERE a.planta_id = :planta_id
  AND ml.timestamp BETWEEN (:fecha_corte::date - INTERVAL '30 day') AND :fecha_corte
GROUP BY ml.maquina_id, m.nombre
ORDER BY backlog_promedio DESC, mtbf_promedio ASC;
```
**Responde:** Activos con mayor riesgo de mantenimiento.

---

# Grupo 4 — Energía, materia prima y trazabilidad

## Q13. Consumo kWh del día vs línea base
**Parámetros:** `:planta_id`, `:fecha`, `:fecha_inicio_base`, `:fecha_fin_base`
```sql
WITH hoy AS (
  SELECT SUM(ee.kwh) AS kwh_hoy
  FROM energia_eventos ee
  JOIN maquinas m ON m.id = ee.maquina_id
  JOIN areas a ON a.id = m.area_id
  WHERE a.planta_id = :planta_id
    AND DATE(ee.timestamp) = :fecha
), base AS (
  SELECT AVG(d.kwh_dia) AS kwh_linea_base
  FROM (
    SELECT DATE(ee.timestamp) AS fecha_base, SUM(ee.kwh) AS kwh_dia
    FROM energia_eventos ee
    JOIN maquinas m ON m.id = ee.maquina_id
    JOIN areas a ON a.id = m.area_id
    WHERE a.planta_id = :planta_id
      AND DATE(ee.timestamp) BETWEEN :fecha_inicio_base AND :fecha_fin_base
    GROUP BY DATE(ee.timestamp)
  ) d
)
SELECT hoy.kwh_hoy,
       base.kwh_linea_base,
       hoy.kwh_hoy - base.kwh_linea_base AS delta_kwh,
       (hoy.kwh_hoy - base.kwh_linea_base) / NULLIF(base.kwh_linea_base, 0) AS delta_pct
FROM hoy, base;
```
**Responde:** Desviación de consumo energético vs baseline.

## Q14. Consumo por unidad producida vs estándar
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`, `:estandar_kwh_por_unidad`
```sql
SELECT SUM(ee.kwh) AS kwh_total,
       SUM(pt.total_unidades) AS total_unidades,
       SUM(ee.kwh) / NULLIF(SUM(pt.total_unidades), 0) AS kwh_por_unidad_real,
       :estandar_kwh_por_unidad AS kwh_por_unidad_estandar,
       (SUM(ee.kwh) / NULLIF(SUM(pt.total_unidades), 0)) / NULLIF(:estandar_kwh_por_unidad, 0) AS ratio_vs_estandar
FROM energia_eventos ee
JOIN produccion_turno pt ON pt.maquina_id = ee.maquina_id AND pt.fecha = DATE(ee.timestamp)
WHERE pt.planta_id = :planta_id
  AND pt.fecha BETWEEN :fecha_inicio AND :fecha_fin;
```
**Responde:** Eficiencia energética específica.

## Q15. Consumo de materia prima vs estándar
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT mpc.referencia_id,
       rp.nombre AS referencia_nombre,
       SUM(mpc.consumo_real) AS consumo_real,
       SUM(mpc.consumo_estandar) AS consumo_estandar,
       SUM(mpc.consumo_real) / NULLIF(SUM(mpc.consumo_estandar), 0) AS ratio_consumo_vs_estandar
FROM materia_prima_consumo mpc
JOIN referencias_producto rp ON rp.id = mpc.referencia_id
WHERE mpc.planta_id = :planta_id
  AND mpc.fecha BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY mpc.referencia_id, rp.nombre
ORDER BY ratio_consumo_vs_estandar DESC;
```
**Responde:** Referencias con sobreconsumo de materia prima.

## Q16. Trazabilidad de lote MP → PT
**Parámetros:** `:lote_pt`
```sql
SELECT mpc.lote_pt,
       mpc.lote_mp,
       mpc.referencia_id,
       rp.nombre AS referencia_nombre,
       SUM(mpc.consumo_real) AS consumo_real
FROM materia_prima_consumo mpc
JOIN referencias_producto rp ON rp.id = mpc.referencia_id
WHERE mpc.lote_pt = :lote_pt
GROUP BY mpc.lote_pt, mpc.lote_mp, mpc.referencia_id, rp.nombre
ORDER BY consumo_real DESC;
```
**Responde:** Lotes de materia prima consumidos para un lote de producto terminado.

---

# Grupo 5 — SPC, tendencia y predicción simple

## Q17. Tendencia lineal de OEE últimos 14 días
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT pt.fecha,
       SUM(pt.oee * pt.total_unidades) / NULLIF(SUM(pt.total_unidades), 0) AS oee_agregado,
       SUM(pt.total_unidades) AS total_unidades
FROM produccion_turno pt
WHERE pt.planta_id = :planta_id
  AND pt.fecha BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY pt.fecha
ORDER BY pt.fecha ASC;
```
**Responde:** Serie base para regresión y proyección de OEE.

## Q18. Riesgo de incumplir meta mensual
**Parámetros:** `:planta_id`, `:fecha_inicio_mes`, `:fecha_corte`, `:meta_mensual_unidades`, `:dias_mes`, `:dia_mes_actual`
```sql
SELECT SUM(pt.total_unidades) AS producido_acumulado,
       :meta_mensual_unidades AS meta_mensual_unidades,
       SUM(pt.total_unidades) / NULLIF(:meta_mensual_unidades, 0) AS pct_producido,
       :dia_mes_actual / NULLIF(:dias_mes, 0) AS pct_mes_transcurrido,
       (SUM(pt.total_unidades) / NULLIF(:meta_mensual_unidades, 0)) - (:dia_mes_actual / NULLIF(:dias_mes, 0)) AS gap_vs_ritmo
FROM produccion_turno pt
WHERE pt.planta_id = :planta_id
  AND pt.fecha BETWEEN :fecha_inicio_mes AND :fecha_corte;
```
**Responde:** Si la producción va en ritmo o en riesgo.

## Q19. Variables SPC fuera de especificación
**Parámetros:** `:planta_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT pm.id AS punto_id,
       pm.nombre AS punto_nombre,
       COUNT(*) AS total_fuera_especificacion,
       AVG(lv.valor) AS promedio_valor
FROM lecturas_variable lv
JOIN puntos_medicion pm ON pm.id = lv.punto_id
WHERE pm.nivel IN ('planta','area','linea','maquina')
  AND lv.timestamp BETWEEN :fecha_inicio AND :fecha_fin
  AND ((lv.lsl IS NOT NULL AND lv.valor < lv.lsl) OR (lv.usl IS NOT NULL AND lv.valor > lv.usl))
GROUP BY pm.id, pm.nombre
ORDER BY total_fuera_especificacion DESC;
```
**Responde:** Puntos de medición más fuera de especificación.

## Q20. Señal de deriva de proceso por variable
**Parámetros:** `:punto_id`, `:fecha_inicio`, `:fecha_fin`
```sql
SELECT DATE(lv.timestamp) AS fecha,
       AVG(lv.valor) AS promedio_dia,
       MIN(lv.valor) AS minimo_dia,
       MAX(lv.valor) AS maximo_dia
FROM lecturas_variable lv
WHERE lv.punto_id = :punto_id
  AND lv.timestamp BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY DATE(lv.timestamp)
ORDER BY fecha ASC;
```
**Responde:** Serie diaria para detectar drift de proceso.
