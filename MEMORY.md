# MEMORY.md

## 2026-04-04 - Diseño base del agente de fábrica
- El agente fue redefinido como analista de datos de fábrica, detector de anomalías, predictor de riesgo/falla y generador de informes por rol.
- Roles base aprobados: Gerente, Supervisor, Operador, Mantenimiento y Calidad.
- Si aparece un rol nuevo, se guarda el rol literal y se adapta la respuesta al perfil más cercano mediante `role_class`.
- Onboarding aprobado: si un usuario pide datos y no tiene perfil, primero se pide nombre y rol; después se confirma que quedó guardado y puede continuar preguntando.
- Los perfiles multiusuario se guardan en `profiles/users/`; `USER.md` queda reservado para el humano principal del workspace.
- El heartbeat debe ser extremadamente liviano y usarse solo para alertas críticas: anomalías, desviaciones fuertes, riesgo de falla o riesgo de incumplir meta mensual.
- El cron/reporting queda orientado por rol: gerencia/directivos con informes semanales y mensuales; supervisión con cierre por turno y diario; mantenimiento y calidad con enfoque técnico/operativo; operador normalmente bajo demanda.
- Se aprobaron plantillas de informes por rol y alerta crítica para estandarizar respuestas futuras.
- Quedó mandatado en `AGENTS.md` que cuando un usuario de fábrica escriba por primera vez pidiendo datos, antes de responder se debe pedir nombre y rol, guardar el perfil y solo después continuar.
