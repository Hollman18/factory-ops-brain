---
name: comparador-periodos
description: Compare production KPIs across historical periods, shifts, lines, machines, plants, or references for OEE, Maintenance, Energy, Raw Materials, and SPC. Use when the user asks things like "compara", "vs", "contra", "diferencia entre", "mejor turno", "peor línea", "cuál máquina produce más", "tendencia de", "histórico de", "cómo ha cambiado", "semana pasada vs esta", "febrero vs marzo", "ranking de plantas", or broad historical performance comparisons. Use for historical comparison and ranking questions, not real-time status queries.
---

# Comparador de periodos multi-planta

## Propósito

Responder preguntas de comparación histórica sobre KPIs de producción en cualquier dimensión de la jerarquía productiva. Traducir lenguaje natural a la llamada correcta de API, interpretar el delta y explicar qué cambió y por qué importa.

## Alcance

Usar esta skill para comparaciones históricas entre:
- periodos del tiempo
- entidades del proceso (planta, área, línea, máquina)
- turnos
- referencias o SKU
- rankings multi-planta

No usar para consultas en tiempo real como “cómo va la línea 2 ahora”.

## Asignación de agente

- **Primary**: Agente Director para comparaciones cross-plant
- **Secondary**: Agente Planta-cloud para comparaciones dentro de una planta

## Variables de entorno

- `API_BASE_URL` — Base URL del backend FastAPI o de la API de IA
- `API_TOKEN` — Bearer token para autenticación de endpoints legacy
- `DEFAULT_TIMEZONE` — Timezone IANA por defecto

## Referencias

- Si la consulta usa la API de IA de MQTTH, leer `references/mqtth-api-ia.md`.
- Mantener secretos fuera del `SKILL.md`. Guardar tokens y claves solo en notas locales del workspace o variables de entorno.

## Fuentes de datos

Nunca consultar PostgreSQL directamente. Llamar siempre la API REST. Confiar en la API para agregaciones ponderadas, recalculaciones y semántica de negocio.

Para integraciones MQTTH con endpoints `/api/ia/*`:
- Autenticarse con header `X-API-Key`.
- Considerar que la API key ya filtra por empresa.
- Preferir el catálogo jerárquico al inicio de la sesión para resolver nombres a IDs.

## Endpoints principales

```text
GET /api/metrics/oee
 ?nivel={corporacion|sede|planta|area|linea|maquina}
 &id={uuid}
 &desde={ISO_DATE}
 &hasta={ISO_DATE}
 &agrupar_por={turno|dia|semana|mes}
 &turno_id={uuid}
 &referencia_id={uuid}

GET /api/metrics/mtto
 ?nivel={planta|area|linea|maquina}
 &id={uuid}
 &desde={ISO_DATE}
 &hasta={ISO_DATE}

GET /api/metrics/energia
 ?nivel={planta|area|linea|maquina}
 &id={uuid}
 &tipo_recurso={KWH|AGUA|GAS|VAPOR|AIRE}
 &desde={ISO_DATE}
 &hasta={ISO_DATE}

GET /api/metrics/mp
 ?nivel={planta|area|contenedor}
 &id={uuid}
 &desde={ISO_DATE}
 &hasta={ISO_DATE}

GET /api/metrics/spc
 ?punto_id={uuid}
 &desde={ISO_DATE}
 &hasta={ISO_DATE}
```

## Endpoint preferido para comparación

### MQTTH API IA

Si la consulta está soportada por la API de IA de MQTTH, preferir:

```text
GET /api/ia/oee/compare
 ?tipo={periodo|entidad}
 &nivel={company|planta|area|linea|maquina}
 &id_a={uuid|all}
 &id_b={uuid}
 &desde_a={date}&hasta_a={date}
 &desde_b={date}&hasta_b={date}
```

Notas críticas observadas en pruebas reales:
- `entidad_a.*` y `entidad_b.*` vienen con KPIs en escala **0–100**.
- `deltas.oee_pp`, `deltas.disponibilidad_pp`, `deltas.rendimiento_pp`, `deltas.calidad_pp` ya vienen en **puntos porcentuales (pp)**.
- `analysis` trae `driver_kpi`, `causa_probable`, `ganador`, `delta_pp` y `brecha_oee_pp`.
- Si una entidad viene `null`, reportar que no hay datos en ese rango.
- Si el endpoint devuelve `warnings`, traducirlos a lenguaje humano.

### Endpoint legacy genérico

Si el backend expone el comparador legacy, también se puede usar:

```text
GET /api/metrics/compare
 ?modulo={oee|mtto|energia|mp|spc}
 &nivel={planta|area|linea|maquina}
 &tipo_comparacion={periodo|entidad|turno|referencia}
 &id_a={uuid}&desde_a={date}&hasta_a={date}
 &id_b={uuid}&desde_b={date}&hasta_b={date}
```

## Tipos de comparación

### 1. Misma entidad, distinto periodo

Ejemplos:
- “OEE de planta BAQ febrero vs marzo”
- “Cómo cambió el MTBF de envasadora L3 este mes vs el anterior”

Acción:
1. Identificar entidad y ambos periodos.
2. Llamar `/api/metrics/compare?tipo_comparacion=periodo`.
3. Reportar deltas con contexto.

### 2. Distintas entidades, mismo periodo

Ejemplos:
- “Compara línea 1 vs línea 2 esta semana”
- “Cuál máquina tiene mejor calidad en planta BAQ”

Acción:
1. Identificar entidades y periodo compartido.
2. Llamar `/api/metrics/compare?tipo_comparacion=entidad`.
3. Reportar ranking y mayor brecha.

### 3. Comparación por turno

Ejemplos:
- “Mejor turno de esta semana en envasadora 3”
- “Turno A vs Turno B en línea 2”

Acción:
1. Consultar OEE con `agrupar_por=turno`.
2. Comparar `turno_id`.
3. Identificar mejor/peor turno y el KPI con mayor diferencia.

### 4. Comparación por referencia o SKU

Ejemplos:
- “Cuál referencia da mejor rendimiento en la empacadora”
- “OEE por producto este mes”

Acción:
1. Consultar OEE agrupado por referencia.
2. Ordenar por OEE o KPI pedido.
3. Si aplica, explicar con `velocidad_ideal` o configuración de referencia.

### 5. Ranking multi-planta

Ejemplos:
- “Ranking de plantas por OEE este mes”
- “Cuál planta tiene peor disponibilidad”

Acción:
1. Si existe MQTTH API IA, usar `/api/ia/oee/ranking?nivel=company&id=any&...`.
2. Si no, consultar OEE a nivel corporación agrupado por planta.
3. Ordenar por KPI solicitado.
4. Identificar la pérdida dominante del peor desempeño.

## Flujo de trabajo

### Paso 1: Parsear la solicitud

Extraer:
- **Módulo**: OEE, Mantenimiento, Energía, Materia Prima o SPC. Si no es explícito, asumir OEE.
- **Tipo de comparación**: periodo, entidad, turno, referencia o ranking.
- **Entidades**: planta, línea, máquina, SKU o punto SPC.
- **Periodos**: interpretar expresiones relativas usando la zona horaria correcta.
- **KPI específico**: disponibilidad, MTBF, consumo kWh, Cpk, etc. Si no se especifica, devolver el dashboard del módulo.

Interpretación estándar de fechas:
- “esta semana” = lunes 00:00 a ahora
- “semana pasada” = lunes anterior a domingo anterior
- “este mes” = día 1 a ahora
- “mes pasado” = primer a último día del mes anterior
- “hoy vs ayer” = fecha actual contra fecha previa
- “Q1 vs Q2” = ene-mar vs abr-jun

### Paso 2: Validar y completar vacíos

- Si la entidad es ambigua, desambiguar por planta o preguntar.
- Si falta el periodo, usar por defecto “este mes vs mes anterior” para comparaciones por periodo o “esta semana” para rankings.
- Si el módulo es realmente ambiguo, preguntar cuál quiere comparar. Si el contexto sugiere OEE, no preguntar.

### Paso 3: Llamar la API

Si se usa MQTTH API IA:
1. Llamar primero `/api/ia/catalog/hierarchy` para resolver nombres a IDs cuando haga falta.
2. Cachear durante la sesión el mapa nombre → id para plantas, áreas, líneas y máquinas.
3. Usar `/api/ia/oee/compare` para comparar dos periodos o dos entidades.
4. Usar `/api/ia/oee/historia` para tendencias, turnos, referencias y series.
5. Usar `/api/ia/oee/ranking` para mejores/peores o rankings jerárquicos.
6. Si `warnings` indica falta de jerarquía o falta de hijos, explicarlo claramente y no inventar comparaciones.
7. Para uso en Telegram, responder en texto natural breve; no devolver JSON crudo salvo que el usuario lo pida.

Ejemplo MQTTH:

```bash
curl -s -H "X-API-Key: ${MQTTH_IA_API_KEY}" \
  "${MQTTH_API_BASE_URL}/api/ia/oee/compare?tipo=periodo&nivel=planta&id_a=${PLANTA_ID}&desde_a=2026-02-01&hasta_a=2026-02-28&desde_b=2026-03-01&hasta_b=2026-03-31"
```

Si se usa backend legacy, preferir `/api/metrics/compare` cuando se comparen dos cosas. Para rankings, usar el endpoint del módulo con `agrupar_por`.

Ejemplo legacy:

```bash
curl -s -H "Authorization: Bearer ${API_TOKEN}" \
  "${API_BASE_URL}/api/metrics/compare?modulo=oee&tipo_comparacion=periodo&nivel=planta&id_a=${PLANTA_ID}&desde_a=2026-02-01&hasta_a=2026-02-28&id_b=${PLANTA_ID}&desde_b=2026-03-01&hasta_b=2026-03-31"
```

Si no existe un endpoint comparador, hacer dos llamadas separadas y calcular los deltas manualmente.

### Paso 4: Interpretar deltas

Si la respuesta viene de MQTTH `/api/ia/oee/compare`:
- Mostrar `entidad_a.*` y `entidad_b.*` como `%` directos, sin multiplicar por 100.
- Mostrar `deltas.oee_pp`, `deltas.disponibilidad_pp`, `deltas.rendimiento_pp`, `deltas.calidad_pp` directamente en **pp**.
- No recalcular esos deltas ni reconvertir los KPIs salvo que el backend cambie de contrato.
- Interpretar `analysis.driver_kpi` como el principal impulsor del cambio.
- Traducir `analysis.causa_probable` a lenguaje humano.
- Si `deltas` o `analysis` vienen `null`, explicar que falta uno de los periodos o que no hay datos comparables.

Si la respuesta no trae deltas listos, calcular para cada KPI:
- **Delta absoluto** = valor_b - valor_a
- **Delta porcentual** = `(valor_b - valor_a) / valor_a * 100`
- **Dirección** = mejora o deterioro

Considerar **más alto es mejor** para:
- OEE, Disponibilidad, Rendimiento, Calidad, TEEP, FPY, MTBF, Confiabilidad, Factor de Potencia, Rendimiento MP, % Renovable, Cumplimiento Plan Prev, Cp, Cpk, Nivel Sigma

Considerar **más bajo es mejor** para:
- MTTR, Desperdicio %, Retrabajo %, Tiempo Muerto, Costo Pérdida, Tasa de Falla, Backlog, Consumo/Und, Costo/Und, Emisiones CO2, Merma %, % Alarma, % Fuera de Control SPC, Desviación de Consumo

Si el delta es menor a 1% en KPIs porcentuales, describirlo como **estable**.

### Paso 5: Detectar causa raíz principal

Si OEE cambia más de 3 puntos, revisar pilares y pérdidas:
1. Si cae Disponibilidad, revisar L1 averías y L2 setup.
2. Si cae Rendimiento, revisar L3 microparadas y L4 velocidad reducida.
3. Si cae Calidad, revisar L5 arranque y L6 producción.

Sugerencias típicas:
- **L1 alto** → analizar Pareto de fallas
- **L2 alto** → revisar SMED y tiempos de setup
- **L3 alto** → inspeccionar ajustes mecánicos o sensores
- **L4 alto** → validar velocidad ideal/configuración
- **L5/L6 altos** → revisar variables de proceso y SPC

### Paso 6: Formatear respuesta

Estructura recomendada:

```text
[Resumen breve con hallazgo principal]

Periodo A: {nombre} ({desde} — {hasta})
Periodo B: {nombre} ({desde} — {hasta})

OEE: A: {valor_a}% → B: {valor_b}% ({delta_pp} pp)
Disponibilidad: A: {valor_a}% → B: {valor_b}% ({delta_pp} pp)
Rendimiento: A: {valor_a}% → B: {valor_b}% ({delta_pp} pp)
Calidad: A: {valor_a}% → B: {valor_b}% ({delta_pp} pp)

[Mayor diferencia]: {KPI} cambió {delta_pp} pp. Causa probable: {explicación}

[Acción sugerida]: {recomendación específica}
```

Para Telegram y chats rápidos:
- Priorizar respuestas de 4–8 líneas.
- No devolver JSON salvo que el usuario lo pida.
- Liderar con el hallazgo principal.
- Si no hay datos, decirlo en la primera línea.

Mantener el resumen en menos de 250 palabras y cerrar siempre con una acción sugerida o una pregunta de seguimiento.

## Comparaciones cross-module

Si el usuario pide una comparación amplia como “cómo estuvo planta BAQ en febrero vs marzo”, sintetizar todos los módulos:

1. **OEE**: OEE ponderado, 3 pilares, unidades producidas, costo pérdida
2. **Mantenimiento**: MTBF, MTTR, número de fallas, falla principal
3. **Energía**: consumo total, costo, consumo por unidad, factor de potencia
4. **Materia prima**: consumo específico, desviación vs estándar, merma
5. **SPC**: variables fuera de control, peor Cpk

Hacer llamadas paralelas a la API y liderar la respuesta con el módulo que más cambió.

## Reglas

- Nunca promediar OEEs ni porcentajes entre entidades. Usar promedio ponderado.
- Nunca promediar MTBF entre máquinas. Recalcular desde totales.
- No promediar factor de potencia; recalcular desde sumas de kW y kVAR.
- Para SPC, usar varianza agrupada, no promedio simple de desviaciones.
- Si cambió la tarifa energética entre periodos, mencionarlo explícitamente.
- Si se comparan plantas en zonas horarias distintas, convertir límites de fecha a hora local antes de consultar la API.
- Si un periodo tiene producción cero, no mostrar KPIs porcentuales; indicar “Sin producción en este periodo”.
- Incluir número de registros o turnos por periodo cuando esté disponible.
- Terminar siempre con una recomendación o follow-up útil.
