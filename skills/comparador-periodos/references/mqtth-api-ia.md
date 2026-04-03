# API de IA — MQTTH Platform

Base URL: `http://31.97.147.124:3000`
Versión observada en pruebas: 1.1 (revalidada el 2026-04-03 UTC)

## Autenticación

Todos los endpoints bajo `/api/ia/*` requieren header:

```http
X-API-Key: <token>
```

La API key está ligada a una sola empresa. Los datos quedan filtrados automáticamente a esa empresa.

### Health

```http
GET /api/ia/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "message": "API key válida. Acceso a endpoints de IA concedido.",
  "key_name": "agente",
  "company_id": "master_company_id",
  "company_name": "MQTTH System"
}
```

## Principio de interpretación para esta skill

### Lo observado en pruebas reales

La documentación 1.1 dice que los KPIs individuales vienen en escala `0–1`, pero las respuestas reales observadas el `2026-04-03` devolvieron KPIs en escala **0–100**.

Ejemplos reales:
- `series[].oee = 21.2505`
- `series[].disponibilidad = 86.0335`
- `entidad_a.oee = 20.9241`
- `entidad_b.rendimiento = 32.2557`

Por tanto, **hasta nuevo aviso esta skill debe tratar los KPIs individuales como porcentajes ya normalizados en escala `0–100`, no como decimales `0–1`**.

### Reglas activas de interpretación

1. `oee`, `disponibilidad`, `rendimiento`, `calidad` → interpretar como `%` en escala `0–100`.
2. `deltas.*_pp` → interpretar como **puntos porcentuales (pp)**.
3. `losses.l1..l4` → minutos.
4. `losses.l5..l6` → unidades rechazadas.
5. `costo_perdida` → moneda local.
6. Si en una futura versión los KPIs vuelven a `0–1`, actualizar esta referencia y la skill.

## Catálogo

### Jerarquía completa

```http
GET /api/ia/catalog/hierarchy
```

Usar al inicio para construir mapas nombre/código → id y también para capturar `timezone` por planta cuando exista.

Respuesta incluye:
- `company`
- `plants[]`
- `areas[]`
- `lines[]`
- `machines[]`
- `references[]`
- `shifts[]`
- `_meta`
- `warnings[]` opcional

Ejemplo real observado:

```json
{
  "company": { "id": "master_company_id", "name": "MQTTH System" },
  "plants": [],
  "areas": [],
  "lines": [],
  "machines": [],
  "references": ["REF-A100", "REF-D400", "REF-B200", "REF-C300"],
  "shifts": [1, 3, 2],
  "_meta": { "total_entities": 0, "has_hierarchy": false },
  "warnings": ["no_hierarchy_configured_for_company"]
}
```

Interpretación:
- Si `warnings` incluye `no_hierarchy_configured_for_company`, no intentar resolver plantas/líneas/máquinas por nombre.
- En ese caso, limitarse a consultas `company` o avisar que no hay jerarquía configurada.

### Referencias por máquina

```http
GET /api/ia/catalog/references?machine_id=<uuid>
```

Usar solo si el catálogo realmente devolvió máquinas.

## OEE histórico

```http
GET /api/ia/oee/historia
```

Parámetros principales:
- `nivel={company|planta|area|linea|maquina}`
- `id=<uuid|all>`
- `desde=YYYY-MM-DD`
- `hasta=YYYY-MM-DD`
- `agrupar_por={hora|dia|semana|mes|turno|referencia}`

Notas observadas:
- los KPIs ya vienen en `%` (`0–100`)
- `hasta` es inclusivo
- pueden existir `warnings`
- `total_registros` puede venir `null` en algunas respuestas
- `losses` puede venir parcial según nivel de agregación

Ejemplo real observado:

```json
{
  "periodo": "2026-03-25",
  "oee": 21.2505,
  "disponibilidad": 86.0335,
  "rendimiento": 32.738,
  "calidad": 75.4024,
  "total_unidades": 420991,
  "losses": {
    "l1_averia_min": 0,
    "l5_rechazo_arranque_und": 0,
    "l6_rechazo_prod_und": 0
  },
  "costo_perdida": 0
}
```

## OEE comparador

```http
GET /api/ia/oee/compare
```

### Comparación de periodos

```http
GET /api/ia/oee/compare?tipo=periodo&nivel=company&id_a=all&desde_a=2026-03-01&hasta_a=2026-03-31&desde_b=2026-04-01&hasta_b=2026-04-30
```

### Comparación de entidades

```http
GET /api/ia/oee/compare?tipo=entidad&nivel=linea&id_a=uuid-l1&id_b=uuid-l2&desde_a=2026-03-01&hasta_a=2026-03-31&desde_b=2026-03-01&hasta_b=2026-03-31
```

Respuesta observada:
- `entidad_a`, `entidad_b` con KPIs en escala `%` (`0–100`)
- `deltas` con sufijo `_pp` en **puntos porcentuales (pp)**
- `analysis.driver_kpi`
- `analysis.delta_pp`
- `analysis.causa_probable`
- `analysis.ganador`
- `analysis.brecha_oee_pp`
- `warnings` opcional

Ejemplo real observado:

```json
{
  "deltas": {
    "oee_pp": -7.84,
    "disponibilidad_pp": -1.55,
    "rendimiento_pp": -11.49,
    "calidad_pp": -1.54,
    "total_unidades": -279725947,
    "costo_perdida": 0
  },
  "analysis": {
    "driver_kpi": "rendimiento",
    "delta_pp": -11.49,
    "causa_probable": "variacion_rendimiento",
    "ganador": "entidad_a",
    "brecha_oee_pp": 7.84,
    "reduccion_costo": 0
  },
  "entidad_a": {
    "nombre": "2026-03-01 → 2026-03-31",
    "oee": 20.9241,
    "disponibilidad": 86.0942,
    "rendimiento": 32.3706,
    "calidad": 75.0064
  },
  "entidad_b": {
    "nombre": "2026-04-01 → 2026-04-30",
    "oee": 20.8457,
    "disponibilidad": 86.0787,
    "rendimiento": 32.2557,
    "calidad": 74.991
  }
}
```

Interpretación para la skill:
- Mostrar `entidad_a.*` y `entidad_b.*` como `%` directos.
- Mostrar `deltas.oee_pp`, `deltas.disponibilidad_pp`, `deltas.rendimiento_pp`, `deltas.calidad_pp` como `pp`.
- No dividir ni multiplicar esos KPIs salvo que el backend cambie otra vez.
- Si `entidad_a` o `entidad_b` es `null`, reportar que no hay datos en ese rango.

### Causas probables posibles

- `variacion_averias`
- `variacion_setup`
- `variacion_microparadas`
- `variacion_velocidad`
- `variacion_rendimiento`
- `variacion_rechazos`
- `variacion_general`

## OEE ranking

```http
GET /api/ia/oee/ranking
```

Parámetros:
- `nivel` = nivel del padre
- `id` = id del padre
- `desde`, `hasta`
- `orden={asc|desc}`

Jerarquía esperada:
- `company` → plantas
- `planta` → áreas
- `area` → líneas
- `linea` → máquinas

Notas:
- `orden=asc` devuelve peores primero.
- `orden=desc` devuelve mejores primero.
- Si no hay hijos configurados, puede venir `warnings: ["no_children_configured_at_this_level"]`.

Ejemplo real observado:

```json
{
  "meta": {
    "nivel": "company",
    "id": "master_company_id",
    "desde": "2026-03-01",
    "hasta": "2026-03-31",
    "child_type": "planta"
  },
  "ranking": [],
  "warnings": ["no_children_configured_at_this_level"]
}
```

## Warnings relevantes

- `no_hierarchy_configured_for_company`
- `no_children_configured_at_this_level`
- `no_historical_data_for_period`

La skill debe mostrarlos en lenguaje humano cuando bloqueen una comparación.

## Errores

Formato:

```json
{ "error": "<codigo>", "message": "<descripcion>" }
```

Códigos relevantes:
- `missing_api_key`
- `invalid_api_key`
- `missing_params`
- `invalid_nivel`
- `invalid_agrupar_por`
- `invalid_date`
- `invalid_date_range`
- `invalid_tipo`
- `server_error`

## Reglas operativas para la skill

1. Resolver nombres humanos a IDs usando `/api/ia/catalog/hierarchy` solo si realmente hay jerarquía disponible.
2. Cachear el catálogo durante la sesión si ya fue consultado.
3. Usar `/api/ia/oee/compare` cuando el usuario compare dos periodos o dos entidades.
4. Usar `/api/ia/oee/historia` para tendencias, turnos, referencias y series temporales.
5. Usar `/api/ia/oee/ranking` para mejores/peores, top/bottom y rankings jerárquicos.
6. Mostrar KPIs individuales como `%` directos, porque en pruebas reales ya vienen en `0–100`.
7. Mostrar deltas con sufijo `_pp` como `pp`.
8. Advertir posible desfase por UTC si el usuario espera corte local por planta/turno.
9. Si no hay jerarquía configurada, limitar consultas a `company` y explicarlo.
10. No consultar PostgreSQL directamente.
11. No incluir tokens en respuestas, logs o la propia skill.
