# DATA_MODEL.md

Mapa operativo del modelo de datos industrial para que un agente de IA entienda cómo está estructurada la base de datos del cliente sin verla directamente ni inventarla.

---

## 1. Propósito

Este archivo define la estructura mínima que el agente necesita para:
- entender la jerarquía industrial
- consultar producción, OEE y capacidad correctamente
- distinguir dato IoT vs manual vs calculado
- agregar métricas sin errores
- interpretar metas y severidad
- analizar mantenimiento, energía, trazabilidad, materia prima y SPC

Regla general: este archivo manda sobre cualquier inferencia. Si algo no está aquí, el agente no debe asumirlo sin validación adicional.

---

## 2. Jerarquía organizacional y FKs

La jerarquía base es:

**Corporación → Sede → Planta → Área → Línea → Máquina**

### Tablas jerárquicas
- `corporaciones`
  - PK: `id`
- `sedes`
  - PK: `id`
  - FK: `corporacion_id -> corporaciones.id`
- `plantas`
  - PK: `id`
  - FK: `sede_id -> sedes.id`
- `areas`
  - PK: `id`
  - FK: `planta_id -> plantas.id`
- `lineas_produccion`
  - PK: `id`
  - FK: `area_id -> areas.id`
- `maquinas`
  - PK: `id`
  - FK: `linea_id -> lineas_produccion.id`
  - FK de contexto adicional disponible: `area_id -> areas.id`

### Regla de navegación para el agente
Cuando una consulta diga “planta”, “área”, “línea” o “máquina”, el agente debe asumir esta jerarquía y respetar esos FK.

---

## 3. Tablas principales que el agente debe conocer

### 3.1 `produccion_turno`
Tabla fact principal para producción, OEE y capacidad operativa.

#### Claves y contexto
- `id`
- `maquina_id`
- `turno_id`
- `referencia_id`
- `fecha`
- `proceso_id` (si aplica)

#### Campos operativos clave
- `und_buenas`
- `und_nc`
- `desperdicio`
- `retrabajo`
- `total_unidades`
- `vel_real`
- `vel_ideal`
- `t_calendario`
- `t_programado`
- `t_operativo`
- `t_productivo`
- `t_parada`
- `t_micro`

#### KPIs calculados almacenados o derivados
- `disponibilidad`
- `rendimiento`
- `calidad`
- `oee`
- `teep`
- `first_pass_yield`
- `desperdicio_pct`
- `retrabajo_pct`
- `costo_perdida`
- `und_no_producidas`
- `utilizacion`

#### Pérdidas principales
- `l1_averia`
- `l2_setup`
- `l3_microparada`
- `l4_velocidad`
- `l5_rechazo_arranque`
- `l6_rechazo_prod`

---

### 3.2 `metas_indicadores`
Tabla de metas y umbrales para cualquier KPI industrial.

#### Campos clave que el agente debe leer
- `id`
- `nivel` — corporacion / sede / planta / area / linea / maquina
- `entidad_id`
- `tipo_indicador` — oee / disponibilidad / rendimiento / calidad / teep / fpy / energia / mtbf / mttr / consumo_mp / spc / etc.
- `meta_valor`
- `meta_minima`
- `meta_critica`
- `meta_excelencia`
- `vigente_desde`
- `vigente_hasta`
- `turno_id` (opcional)
- `referencia_id` (opcional)

#### Regla de interpretación
- `meta_critica`: por debajo de aquí, el indicador está en estado crítico
- `meta_minima`: mínimo aceptable operativo
- `meta_valor`: objetivo esperado normal
- `meta_excelencia`: benchmark superior / world-class

---

### 3.3 `eventos_parada`
Tabla de detalle de paradas por máquina / turno.

#### Campos clave esperados
- `id`
- `produccion_turno_id`
- `maquina_id`
- `codigo_falla_id`
- `inicio`
- `fin`
- `duracion_min`
- `tipo_parada`
- `clasificacion`
- `comentario_operador`

#### Uso por el agente
- explicar caídas de disponibilidad
- detectar averías repetitivas
- identificar causas raíz por turno
- construir Pareto de paradas

---

### 3.4 `plantas`
- `id`
- `sede_id`
- `nombre`
- `codigo`
- `zona_horaria`

### 3.5 `lineas_produccion`
- `id`
- `area_id`
- `nombre`
- `codigo`
- `velocidad_nominal`

### 3.6 `maquinas`
- `id`
- `linea_id`
- `area_id`
- `nombre`
- `codigo`
- `velocidad_nominal`
- `costo_hora_parada`
- `activo`

### 3.7 `referencias_producto`
- `id`
- `corporacion_id`
- `nombre`
- `sku`
- `familia_producto`

### 3.8 `capacidad_maquina_referencia`
Relación máquina × referencia para capacidad ideal por SKU.

#### Campos clave
- `id`
- `maquina_id`
- `referencia_id`
- `velocidad_ideal`
- `capacidad_turno_teorica`
- `unidad_capacidad`

#### Uso por el agente
- interpretar rendimiento por SKU
- evitar comparar rendimiento sin contexto de referencia
- comparar capacidad nominal vs operativa

### 3.9 `mantenimiento_log`
Tabla operativa de mantenimiento.

#### Campos clave
- `id`
- `maquina_id`
- `timestamp`
- `mtbf`
- `mttr`
- `backlog`
- `cumplimiento_plan`
- `criticidad`

### 3.10 `energia_eventos`
Tabla/evento de consumo energético o vista equivalente.

#### Campos clave
- `id`
- `maquina_id`
- `timestamp`
- `kwh`
- `kvar`
- `agua`
- `gas`
- `vapor`
- `aire_comprimido`

### 3.11 `materia_prima_consumo`
Consumo y trazabilidad de materia prima.

#### Campos clave
- `id`
- `planta_id`
- `linea_id`
- `maquina_id`
- `referencia_id`
- `materia_prima_id`
- `fecha`
- `consumo_real`
- `consumo_estandar`
- `lote_mp`
- `lote_pt`

### 3.12 `lecturas_variable`
Lecturas de variables de proceso para SPC y alarmas.

#### Campos clave
- `id`
- `punto_id`
- `turno_id`
- `timestamp`
- `valor`
- `en_alarma`
- `tipo_alarma`
- `lsl`
- `usl`
- `ll`
- `l`
- `h`
- `hh`

### 3.13 `puntos_medicion`
Catálogo de sensores / tags.

#### Campos clave
- `id`
- `tipo_variable_id`
- `nivel`
- `entidad_id`
- `maquina_id`
- `proceso_id`
- `nombre`
- `tag_scada`

---

## 4. Columnas calculadas clave y fórmulas

### Disponibilidad
`disponibilidad = t_productivo / t_operativo`

### Rendimiento
`rendimiento = total_unidades / (t_productivo * vel_ideal)`

### Calidad
`calidad = und_buenas / total_unidades`

### OEE
`oee = disponibilidad * rendimiento * calidad`

### TEEP
`teep = oee * (t_programado / t_calendario)`

### First Pass Yield
`first_pass_yield = und_buenas / (und_buenas + und_nc + desperdicio)`

### Indicadores derivados útiles
- `desperdicio_pct = desperdicio / total_unidades`
- `retrabajo_pct = retrabajo / total_unidades`
- `und_no_producidas = (t_parada + t_micro) * vel_ideal`
- `costo_perdida = und_no_producidas * valor_unitario`
- `consumo_especifico_energia = kwh / total_unidades`
- `consumo_mp_vs_estandar = consumo_real / consumo_estandar`

---

## 5. Regla obligatoria de agregación ponderada

### Regla crítica
**Nunca usar `AVG(oee)` ni promedio simple para OEE o sus pilares.**

### Regla correcta
Siempre agregar ponderando por `total_unidades`.

### Fórmulas obligatorias
- `oee_agregado = SUM(oee * total_unidades) / SUM(total_unidades)`
- `disponibilidad_agregada = SUM(disponibilidad * total_unidades) / SUM(total_unidades)`
- `rendimiento_agregado = SUM(rendimiento * total_unidades) / SUM(total_unidades)`
- `calidad_agregada = SUM(calidad * total_unidades) / SUM(total_unidades)`

### Aplicación
Se usa para subir de nivel:
- máquina → línea
- línea → área
- área → planta
- planta → sede
- sede → corporación

### Regla adicional
Para energía, materia prima y costos normalmente se agregan por suma o por razón específica, no con promedio simple de KPIs.

---

## 6. Campos denormalizados disponibles en `produccion_turno`

Para evitar JOINs pesados, el modelo asume que `produccion_turno` ya trae contexto jerárquico.

### Campos denormalizados disponibles
- `planta_id`
- `linea_id`
- `area_id`
- `maquina_id`
- `turno_id`
- `referencia_id`
- `proceso_id`
- opcionalmente `corporacion_id` y `sede_id`

### Regla para el agente
Si el objetivo es responder rápido analítica operativa, priorizar filtros sobre estos campos denormalizados antes de asumir joins complejos.

---

## 7. Ciclo OEE parcial vs final

### Durante el turno
El OEE es **parcial** y se calcula con **datos IoT solamente**.

### Al cierre del turno
El OEE pasa a ser **final** cuando se incorporan los **datos manuales del operador o supervisor**.

### Regla para el agente
- si la consulta es en tiempo real: tratar el dato como **parcial**
- si la consulta es sobre turno cerrado / día consolidado: tratar el dato como **final**

---

## 8. Qué viene del Edge vs manual vs qué calcula la BD

### 8.1 Lo que viene del Edge / IoT
- conteos automáticos
- estados de máquina
- velocidades reales
- tiempos acumulados
- variables de proceso
- alarmas
- consumos energéticos
- niveles de contenedores / MP

### 8.2 Lo que ingresa el operador manualmente
- turno
- referencia
- proceso
- causa de parada
- desperdicio validado
- retrabajo validado
- comentarios de operación
- lote / trazabilidad manual

### 8.3 Lo que calcula la BD / backend
- OEE agregado
- comparaciones históricas
- rankings
- costos
- tendencias
- Paretos
- análisis SPC de mayor ventana
- proyecciones simples

---

## 9. Cómo leer `metas_indicadores`

### Orden de interpretación recomendado
1. comparar valor actual contra `meta_critica`
2. luego contra `meta_minima`
3. luego contra `meta_valor`
4. luego contra `meta_excelencia`

### Resultado esperado de lectura
- por debajo de `meta_critica` → **crítico**
- entre `meta_critica` y `meta_minima` → **muy débil**
- entre `meta_minima` y `meta_valor` → **por debajo de objetivo**
- entre `meta_valor` y `meta_excelencia` → **cumple**
- por encima de `meta_excelencia` → **excelente**

---

## 10. Reglas operativas para el agente

1. No inventar estructura fuera de este archivo.
2. Usar `produccion_turno` como tabla central para producción/OEE/capacidad.
3. Usar `eventos_parada` para explicar disponibilidad y causa raíz.
4. Usar `metas_indicadores` para interpretar severidad en cualquier dominio.
5. Nunca promediar OEE simple.
6. Diferenciar dato parcial del turno vs dato final de cierre.
7. Priorizar columnas denormalizadas (`planta_id`, `linea_id`, `area_id`) para consultas rápidas.
8. Distinguir siempre entre dato IoT, manual y calculado.
9. Extender análisis a mantenimiento, energía, materia prima, trazabilidad y SPC cuando el usuario lo pida o el riesgo lo justifique.

---

## 11. Resumen mínimo para consulta rápida

### Tabla central
- `produccion_turno`

### Tablas de apoyo esenciales
- `metas_indicadores`
- `eventos_parada`
- `plantas`
- `lineas_produccion`
- `maquinas`
- `referencias_producto`
- `capacidad_maquina_referencia`
- `mantenimiento_log`
- `energia_eventos`
- `materia_prima_consumo`
- `lecturas_variable`
- `puntos_medicion`

### Fórmula crítica
- `SUM(oee * total_unidades) / SUM(total_unidades)`

### Denormalización disponible
- `planta_id`, `linea_id`, `area_id` ya están en `produccion_turno`

### Regla temporal
- durante turno = OEE parcial IoT
- al cierre = OEE final con dato manual
