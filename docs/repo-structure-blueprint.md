# Final repository structure blueprint

## Root
- `README.md`
- `.gitignore`
- `FACTORY_AGENT_BASE_CONFIG.txt`
- `docs/`
- `templates/`
- `workspace-template/`

## docs/
- `overview.md` — what the agent is, who it serves, and how it scales from small business to multinational organizations
- `principles.md` — core operating principles
- `roles.md` — role catalog, role classes, adaptation logic, and profile expectations
- `onboarding.md` — mandatory onboarding flow and profile creation rules
- `security.md` — sensitive-data boundaries, primary-user exception, domain restriction, and authorization model
- `heartbeat-routing.md` — heartbeat purpose, severity logic, routing, escalation, and token discipline
- `cron-by-role.md` — report standards, role defaults, customization rules, and examples
- `data-availability.md` — behavior for missing, partial, insufficient, inconsistent, or not-connected data
- `hierarchy-and-drilldown.md` — organization hierarchy, roll-up/drill-down rules, and cross-level comparisons
- `personalization.md` — learning preferences, profile enrichment, and adaptive behavior
- `severity-and-escalation.md` — severity model and escalation policy
- `recommendations-implemented.md` — implemented design recommendations

## docs/modules/
- `oee.md`
- `maintenance.md`
- `quality.md`
- `spc.md`
- `energy.md`
- `raw-materials.md`
- `production.md`
- `target-risk.md`
- `comparative-analysis.md`
- `alerts-and-anomalies.md`

## templates/
- `gerente-semanal.md`
- `gerente-mensual.md`
- `supervisor-turno.md`
- `supervisor-diario.md`
- `mantenimiento-diario.md`
- `calidad-diario.md`
- `alerta-critica.md`

## workspace-template/
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `HEARTBEAT.md`
- `MEMORY.md`
- `profiles/README.md`
- `profiles/users/.gitkeep`
- `automation/role-rules.md`
- `automation/report-schedules.md`
- `automation/heartbeat-rules.md`
- `automation/templates/`

## Design logic
- `docs/` explains the system
- `templates/` standardizes output
- `workspace-template/` makes it immediately deployable in new agents
