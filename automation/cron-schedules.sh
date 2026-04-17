#!/usr/bin/env bash
set -Eeuo pipefail

CLIENT_PLANTA_ID="${CLIENT_PLANTA_ID:-}"
CLIENT_TELEGRAM_GERENTE="${CLIENT_TELEGRAM_GERENTE:-}"
CLIENT_TELEGRAM_SUPERVISOR="${CLIENT_TELEGRAM_SUPERVISOR:-}"
CLIENT_TELEGRAM_MANTENIMIENTO="${CLIENT_TELEGRAM_MANTENIMIENTO:-}"
CLIENT_TELEGRAM_CALIDAD="${CLIENT_TELEGRAM_CALIDAD:-}"
CLIENT_TZ="${CLIENT_TZ:-}"

require() {
  local name="$1"
  [[ -n "${!name:-}" ]] || { echo "Falta variable requerida: $name" >&2; exit 1; }
}

require CLIENT_PLANTA_ID
require CLIENT_TELEGRAM_GERENTE
require CLIENT_TELEGRAM_SUPERVISOR
require CLIENT_TELEGRAM_MANTENIMIENTO
require CLIENT_TELEGRAM_CALIDAD

TZ_FLAG=()
if [[ -n "$CLIENT_TZ" ]]; then
  TZ_FLAG=(--tz "$CLIENT_TZ")
fi

run_cron() {
  openclaw cron add "$@"
}

# 1. Gerente — alerta crítica inmediata
run_cron \
  --name "Alerta critica gerente" \
  --cron "*/30 * * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id ${CLIENT_PLANTA_ID}. Si no hay anomalías, responde HEARTBEAT_OK. Si hay anomalías críticas, construye alerta ejecutiva: qué cambió, severidad, causa probable, impacto de negocio, quién debe actuar y acción inmediata. No enviar alertas medias al gerente salvo persistencia material." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_GERENTE}"

# 2. Gerente — reporte semanal
run_cron \
  --name "Reporte semanal gerente" \
  --cron "0 7 * * 1" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type trend --planta-id ${CLIENT_PLANTA_ID} --fecha-inicio \$(date -d '7 day ago' +%F) --fecha-fin \$(date +%F). Complementa con QUERIES.md para comparación de producción semanal, OEE agregado, líneas críticas, top pérdidas y riesgo de incumplimiento del mes. Entrega reporte ejecutivo semanal para gerente/directivo, breve y de alto valor." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_GERENTE}"

# 3. Gerente — reporte mensual
run_cron \
  --name "Reporte mensual gerente" \
  --cron "0 7 1 * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type trend --planta-id ${CLIENT_PLANTA_ID} --fecha-inicio \$(date -d '30 day ago' +%F) --fecha-fin \$(date +%F). Complementa con QUERIES.md para producción mensual, OEE mensual, cumplimiento vs meta, pérdidas dominantes, costo estimado y prioridad del siguiente mes. Entrega formato ejecutivo para gerente/directivo." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_GERENTE}"

# 4. Supervisor — cierre por turno
run_cron \
  --name "Cierre de turno supervisor" \
  --cron "5 6,14,22 * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type capacity --planta-id ${CLIENT_PLANTA_ID} --fecha-inicio \$(date +%F) --fecha-fin \$(date +%F). Complementa con QUERIES.md para identificar producción del turno, OEE del turno, línea/máquina que arrastró, principal pérdida, causa probable y acción inmediata. Entrega cierre táctico para supervisor o jefe de producción." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_SUPERVISOR}"

# 5. Supervisor — resumen diario
run_cron \
  --name "Resumen diario supervisor" \
  --cron "10 6 * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta analytics/db_query.py --query-type capacity --planta-id ${CLIENT_PLANTA_ID} --fecha-inicio \$(date -d '1 day ago' +%F) --fecha-fin \$(date -d '1 day ago' +%F). Complementa con QUERIES.md para producción diaria, OEE, comparación vs ayer, peor línea, peor máquina y acción recomendada. Entrega resumen diario para supervisor/jefe de producción." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_SUPERVISOR}"

# 6. Supervisor — heartbeat operativo
run_cron \
  --name "Heartbeat operativo supervisor" \
  --cron "*/30 * * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id ${CLIENT_PLANTA_ID}. Si no hay anomalías, responde HEARTBEAT_OK. Si hay críticas, alerta inmediato. Si hay medias, aplicar lógica de persistencia de 2 ciclos definida en HEARTBEAT.md. Responder en formato táctico para supervisor." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_SUPERVISOR}"

# 7. Mantenimiento — alerta operativa
run_cron \
  --name "Alerta mantenimiento operativa" \
  --cron "0 6-22 * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta queries de QUERIES.md y analytics/anomaly_detector.py para identificar backlog crítico, MTBF/MTTR deteriorado, OTs vencidas si el modelo las soporta y fallas recurrentes. Si no hay hallazgos relevantes, responde HEARTBEAT_OK. Si sí los hay, genera alerta corta para mantenimiento con equipo afectado, severidad, causa probable y acción inmediata." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_MANTENIMIENTO}"

# 8. Mantenimiento — resumen diario técnico
run_cron \
  --name "Resumen diario mantenimiento" \
  --cron "15 6 * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Usa QUERIES.md para resumir equipos críticos, backlog, MTBF, MTTR, fallas recurrentes y prioridad de intervención del día para mantenimiento. Mantén el mensaje corto, técnico y accionable." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_MANTENIMIENTO}"

# 9. Calidad — resumen diario
run_cron \
  --name "Resumen calidad diario" \
  --cron "55 5 * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta queries de QUERIES.md relacionadas con calidad y SPC para la planta ${CLIENT_PLANTA_ID}: calidad del día anterior, first pass yield, referencias con peor desempeño, rechazo, retrabajo y variables fuera de especificación. Genera resumen diario para calidad, concreto y accionable." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_CALIDAD}"

# 10. Calidad — alerta SPC
run_cron \
  --name "Alerta SPC calidad" \
  --cron "*/30 * * * *" \
  "${TZ_FLAG[@]}" \
  --session isolated \
  --message "Ejecuta python3 analytics/anomaly_detector.py --planta-id ${CLIENT_PLANTA_ID}. Si detecta anomalías relacionadas con spc o calidad, generar alerta para calidad con causa probable, severidad y acción inmediata. Si no hay, responder HEARTBEAT_OK." \
  --announce --channel telegram --to "${CLIENT_TELEGRAM_CALIDAD}"

echo "Cron jobs instalados correctamente."
