# cron-schedules.md

Definiciones recomendadas de cron jobs por rol para Factory Ops Brain usando `openclaw cron add`.

## Principio de diseño
No todos los roles deben recibir la misma frecuencia ni el mismo nivel de detalle.

### Regla general
- **Gerente / directivo:** pocas notificaciones, solo valor ejecutivo
- **Supervisor / jefe de producción:** seguimiento frecuente y táctico
- **Mantenimiento:** alertas por condición + resumen técnico
- **Calidad:** resumen diario + alertas por desviación / SPC

## Regla clave
**Gerencia no debe recibir ruido operativo.**
Por defecto, no se recomienda enviar un reporte diario largo al gerente. La configuración recomendada es:
- alertas críticas inmediatas
- reporte semanal
- reporte mensual
- daily solo si el cliente lo pide explícitamente y en formato ultra corto

## Nota sobre zona horaria
OpenClaw puede detectar la zona horaria por defecto del sistema o del usuario/canal (por ejemplo Telegram).  
Por eso el instalador puede:
- usar `--tz "CLIENT_TZ"`
- o eliminar `--tz` y dejar que OpenClaw use la zona horaria detectada

---

# 1. Matriz recomendada por rol

## Gerente / Directivo
### Sí enviar
- alerta crítica inmediata
- reporte semanal ejecutivo
- reporte mensual ejecutivo

### No enviar por defecto
- cierre por turno
- detalle técnico diario
- múltiples alertas medias

### Opcional
- daily ultra corto de 3-4 líneas si el cliente lo pide explícitamente

---

## Supervisor / Jefe de producción
### Sí enviar
- cierre por turno
- resumen diario
- heartbeat crítico

### Objetivo
Ayudar a actuar sobre pérdidas, líneas críticas, turnos y máquinas.

---

## Mantenimiento
### Sí enviar
- alertas por backlog / OTs vencidas / confiabilidad baja
- resumen diario técnico
- semanal técnico opcional

---

## Calidad
### Sí enviar
- resumen diario de calidad
- alertas SPC / fuera de especificación
- semanal por referencias críticas (opcional)

---

# 2. Cron jobs recomendados

## 2.1 Gerente — alerta crítica inmediata (recomendado)

```bash
# Alertas críticas al gerente/directivo solo cuando el heartbeat detecta anomalías severas.
openclaw cron add \
  --name "Alerta critica gerente" \
  --cron "*/30 * * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id CLIENT_PLANTA_ID. Si no hay anomalías, responde HEARTBEAT_OK. Si hay anomalías críticas, construye alerta ejecutiva: qué cambió, severidad, causa probable, impacto de negocio, quién debe actuar y acción inmediata. No enviar alertas medias al gerente salvo persistencia material." \
  --announce --channel telegram --to CLIENT_TELEGRAM_GERENTE
```

---

## 2.2 Gerente — reporte semanal ejecutivo (recomendado)

```bash
# Resumen semanal para gerencia con foco en tendencia, cumplimiento, riesgo y prioridad.
openclaw cron add \
  --name "Reporte semanal gerente" \
  --cron "0 7 * * 1" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type trend --planta-id CLIENT_PLANTA_ID --fecha-inicio $(date -d '7 day ago' +%F) --fecha-fin $(date +%F). Complementa con QUERIES.md para comparación de producción semanal, OEE agregado, líneas críticas, top pérdidas y riesgo de incumplimiento del mes. Entrega reporte ejecutivo semanal para gerente/directivo, breve y de alto valor." \
  --announce --channel telegram --to CLIENT_TELEGRAM_GERENTE
```

---

## 2.3 Gerente — reporte mensual ejecutivo (recomendado)

```bash
# Cierre mensual ejecutivo. Útil para cumplimiento y decisiones de dirección.
openclaw cron add \
  --name "Reporte mensual gerente" \
  --cron "0 7 1 * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type trend --planta-id CLIENT_PLANTA_ID --fecha-inicio $(date -d '30 day ago' +%F) --fecha-fin $(date +%F). Complementa con QUERIES.md para producción mensual, OEE mensual, cumplimiento vs meta, pérdidas dominantes, costo estimado y prioridad del siguiente mes. Entrega formato ejecutivo para gerente/directivo." \
  --announce --channel telegram --to CLIENT_TELEGRAM_GERENTE
```

---

## 2.4 Gerente — reporte diario ejecutivo ultra corto (opcional, no default)

```bash
# Solo activar si el cliente lo pide explícitamente. No debe ser largo ni operativo.
openclaw cron add \
  --name "Reporte diario gerente" \
  --cron "0 6 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type capacity --planta-id CLIENT_PLANTA_ID --fecha-inicio $(date +%F) --fecha-fin $(date +%F). Con ese resultado genera un daily ejecutivo de máximo 4 líneas para gerente: producción vs meta, OEE vs objetivo, principal desviación y recomendación priorizada. Sin detalle operativo excesivo." \
  --announce --channel telegram --to CLIENT_TELEGRAM_GERENTE
```

---

## 2.5 Supervisor / jefe de producción — cierre por turno (recomendado)

```bash
# Cierre táctico por turno para supervisión / jefatura de producción.
openclaw cron add \
  --name "Cierre de turno supervisor" \
  --cron "5 6,14,22 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type capacity --planta-id CLIENT_PLANTA_ID --fecha-inicio $(date +%F) --fecha-fin $(date +%F). Complementa con QUERIES.md para identificar producción del turno, OEE del turno, línea/máquina que arrastró, principal pérdida, causa probable y acción inmediata. Entrega cierre táctico para supervisor o jefe de producción." \
  --announce --channel telegram --to CLIENT_TELEGRAM_SUPERVISOR
```

---

## 2.6 Supervisor / jefe de producción — resumen diario (recomendado)

```bash
# Consolidado del día para supervisión.
openclaw cron add \
  --name "Resumen diario supervisor" \
  --cron "10 6 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type capacity --planta-id CLIENT_PLANTA_ID --fecha-inicio $(date -d '1 day ago' +%F) --fecha-fin $(date -d '1 day ago' +%F). Complementa con QUERIES.md para producción diaria, OEE, comparación vs ayer, peor línea, peor máquina y acción recomendada. Entrega resumen diario para supervisor/jefe de producción." \
  --announce --channel telegram --to CLIENT_TELEGRAM_SUPERVISOR
```

---

## 2.7 Supervisor / jefe de producción — heartbeat crítico (recomendado)

```bash
# Heartbeat operativo para supervisión. Solo si hay anomalías críticas o medias persistentes.
openclaw cron add \
  --name "Heartbeat operativo supervisor" \
  --cron "*/30 * * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id CLIENT_PLANTA_ID. Si no hay anomalías, responde HEARTBEAT_OK. Si hay críticas, alerta inmediato. Si hay medias, aplicar lógica de persistencia de 2 ciclos definida en HEARTBEAT.md. Responder en formato táctico para supervisor." \
  --announce --channel telegram --to CLIENT_TELEGRAM_SUPERVISOR
```

---

## 2.8 Mantenimiento — alerta por OTs vencidas / backlog / deterioro (recomendado)

```bash
# Seguimiento operativo de mantenimiento. No enviar ruido si no hay condición relevante.
openclaw cron add \
  --name "Alerta mantenimiento operativa" \
  --cron "0 6-22 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta queries de QUERIES.md y analytics/anomaly_detector.py para identificar backlog crítico, MTBF/MTTR deteriorado, OTs vencidas si el modelo las soporta y fallas recurrentes. Si no hay hallazgos relevantes, responde HEARTBEAT_OK. Si sí los hay, genera alerta corta para mantenimiento con equipo afectado, severidad, causa probable y acción inmediata." \
  --announce --channel telegram --to CLIENT_TELEGRAM_MANTENIMIENTO
```

---

## 2.9 Mantenimiento — resumen diario técnico (recomendado)

```bash
# Resumen técnico diario de mantenimiento.
openclaw cron add \
  --name "Resumen diario mantenimiento" \
  --cron "15 6 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Usa QUERIES.md para resumir equipos críticos, backlog, MTBF, MTTR, fallas recurrentes y prioridad de intervención del día para mantenimiento. Mantén el mensaje corto, técnico y accionable." \
  --announce --channel telegram --to CLIENT_TELEGRAM_MANTENIMIENTO
```

---

## 2.10 Calidad — resumen diario (recomendado)

```bash
# Resumen de calidad antes del arranque del turno.
openclaw cron add \
  --name "Resumen calidad diario" \
  --cron "55 5 * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta queries de QUERIES.md relacionadas con calidad y SPC para CLIENT_PLANTA_ID: calidad del día anterior, first pass yield, referencias con peor desempeño, rechazo, retrabajo y variables fuera de especificación. Genera resumen diario para calidad, concreto y accionable." \
  --announce --channel telegram --to CLIENT_TELEGRAM_CALIDAD
```

---

## 2.11 Calidad — alerta SPC / fuera de especificación (opcional recomendado)

```bash
# Alerta de calidad por desvío de proceso o SPC. Activar si el cliente usa variables de proceso / SPC.
openclaw cron add \
  --name "Alerta SPC calidad" \
  --cron "*/30 * * * *" \
  --tz "CLIENT_TZ" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id CLIENT_PLANTA_ID. Si detecta anomalías relacionadas con spc o calidad, generar alerta para calidad con causa probable, severidad y acción inmediata. Si no hay, responder HEARTBEAT_OK." \
  --announce --channel telegram --to CLIENT_TELEGRAM_CALIDAD
```

---

# 3. Placeholders esperados por el instalador
- `CLIENT_PLANTA_ID`
- `CLIENT_TELEGRAM_GERENTE`
- `CLIENT_TELEGRAM_SUPERVISOR`
- `CLIENT_TELEGRAM_MANTENIMIENTO`
- `CLIENT_TELEGRAM_CALIDAD`
- `CLIENT_TZ`

---

# 4. Recomendación final de producto

## Configuración recomendada por defecto
### Gerente
- alerta crítica inmediata
- semanal ejecutivo
- mensual ejecutivo
- daily solo opcional y ultra corto

### Supervisor
- cierre por turno
- resumen diario
- heartbeat crítico

### Mantenimiento
- alerta por condición
- resumen diario técnico

### Calidad
- resumen diario
- alerta SPC si aplica

Esto reduce ruido, mejora adopción y alinea mejor el producto con la forma real en que cada rol consume información.
