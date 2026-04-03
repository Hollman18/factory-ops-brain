# API de IA — MQTTH Platform

Base URL: `http://31.97.147.124:3000`

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
  "key_name": "Agente Comparador Períodos",
  "company_id": "uuid-empresa",
  "company_name": "Empresa Demo S.A."
}
```

## Catálogo

### Jerarquía completa

```http
GET /api/ia/catalog/hierarchy
```

Usar al inicio para construir mapas nombre/código → id y también para capturar `timezone` por planta.

Respuesta incluye:
- `company`
- `plants[]` con `id`, `name`, `code`, `timezone`
- `areas[]`
- `lines[]`
- `machines[]`
- `references[]`
- `shifts[]`

### Referencias por máquina

```http
GET /api/ia/catalog/references?machine_id=<uuid>
```

## OEE histórico

```http
GET /api/ia/oee/historia
```

Parámetros principales:
- `nivel={company|planta|area|linea|maquina}`
- `id=<uuid|any>`
- `desde=YYYY-MM-DD`
- `hasta=YYYY-MM-DD`
- `agrupar_por={hora|dia|semana|mes|turno|referencia|maquina|linea|planta}`
- `limit`, `offset`

Notas:
- KPIs (`oee`, `disponibilidad`, `rendimiento`, `calidad`) vienen en escala `0–1`.
- Mostrar al usuario en porcentaje multiplicando x100.
- `losses.l1..l4` están en minutos.
- `losses.l5..l6` están en unidades rechazadas.
- `hasta` es inclusivo.

## OEE comparador

```http
GET /api/ia/oee/compare
```

### Comparación de periodos

```http
GET /api/ia/oee/compare?tipo=periodo&nivel=company&id_a=any&desde_a=2026-03-01&hasta_a=2026-03-31&desde_b=2026-04-01&hasta_b=2026-04-30
```

### Comparación de entidades

```http
GET /api/ia/oee/compare?tipo=entidad&nivel=linea&id_a=uuid-l1&id_b=uuid-l2&desde_a=2026-03-01&hasta_a=2026-03-31&desde_b=2026-03-01&hasta_b=2026-03-31
```

Respuesta:
- `entidad_a`, `entidad_b` con KPIs en escala `0–1`
- `deltas` en **puntos porcentuales (pp)** para KPIs y absolutos para unidades/costo
- `analysis.driver_kpi`
- `analysis.causa_probable`
- `analysis.ganador`

Interpretación:
- `deltas.oee`, `deltas.disponibilidad`, `deltas.rendimiento`, `deltas.calidad` ya vienen en pp. No volver a multiplicar.
- `deltas.costo_perdida` negativo es bueno: B perdió menos dinero.
- Si `entidad_a` o `entidad_b` es `null`, no hay datos en ese rango y la skill debe decirlo explícitamente.

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

Jerarquía:
- `company` → plantas
- `planta` → áreas
- `area` → líneas
- `linea` → máquinas

Notas:
- `orden=asc` devuelve peores primero.
- `orden=desc` devuelve mejores primero.

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

## Reglas de interpretación para la skill

1. Resolver primero nombres humanos a IDs usando `/api/ia/catalog/hierarchy`.
2. Cachear el catálogo durante la sesión si ya fue consultado.
3. Usar `/api/ia/oee/compare` cuando el usuario compare dos periodos o dos entidades.
4. Usar `/api/ia/oee/historia` para tendencias, turnos, referencias y series temporales.
5. Usar `/api/ia/oee/ranking` para mejores/peores, top/bottom y rankings jerárquicos.
6. Mostrar KPIs individuales como `%` a partir de valores `0–1`.
7. Mostrar deltas como `pp` sin reconvertir.
8. Advertir posible desfase por UTC si el usuario espera corte local por planta/turno.
9. No consultar PostgreSQL directamente.
10. No incluir tokens en respuestas, logs o la propia skill.
