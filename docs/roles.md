# Roles

## Purpose
Define how the agent should adapt its behavior, reporting style, depth, priorities, and recommendations according to the user’s role in the organization.

## Base industrial roles
- Gerente
- Directivo
- Supervisor
- Operador
- Mantenimiento
- Calidad

## Extended factory roles
- Jefe de planta
- Jefe de producción
- Coordinador de producción
- Líder de turno
- Planeación
- Logística
- Supply chain
- Ingeniería de procesos
- Mejora continua
- Confiabilidad
- Técnico de mantenimiento
- Coordinador de mantenimiento
- Calidad proceso
- Calidad laboratorio
- Compras / abastecimiento
- Finanzas operativas
- Analista de datos / BI industrial

## General role rules
- Store the literal role from the user.
- Map to an internal `role_class` for adaptation when needed.
- Role-based behavior is the default, not a prison.
- Users may customize reports, questions, frequencies, and preferred detail.
- The agent should learn individual preferences over time.

## Role behavior

### Gerente / Directivo
Prioritize:
- executive summary
- trend
- impact
- target risk
- main business driver
- cross-plant / cross-area comparisons when available
- recommendation for action or escalation

Report style:
- short to medium
- comparative
- decision-oriented

Heartbeat relevance:
- only meaningful risks, severe deteriorations, and target-miss threats

Cron/report defaults:
- weekly
- monthly
- optional high-severity alerts only

### Supervisor / Jefe de planta / Líder de turno
Prioritize:
- line, area, shift, machine, or reference performance
- losses and deviations
- immediate root-cause direction
- corrective action

Report style:
- tactical
- actionable
- medium detail

Heartbeat relevance:
- operational deviations that require action

Cron/report defaults:
- shift-close
- daily
- optional focused anomaly alerts

### Operador
Prioritize:
- what is wrong
- where to look
- what to check first
- what action should happen now

Report style:
- short
- concrete
- low jargon unless asked for more detail

Heartbeat relevance:
- only if a targeted operational alert is appropriate in the deployment

Cron/report defaults:
- usually on-demand
- optional targeted alerts if enabled

### Mantenimiento / Técnico / Confiabilidad
Prioritize:
- failure risk
- recurrence
- deterioration
- critical assets
- intervention priority
- technical implication for continuity

Report style:
- technical
- concise
- severity-aware

Heartbeat relevance:
- elevated failure risk
- recurring technical instability
- critical downtime pattern

Cron/report defaults:
- daily technical
- alert-driven escalation
- optional weekly criticality summary

### Calidad / Calidad proceso / Laboratorio
Prioritize:
- deviation
- rejection
- scrap / merma
- SPC instability when available
- containment
- process/reference risk

Report style:
- analytical
- operational
- containment-oriented

Heartbeat relevance:
- strong deviation
- rejection spike
- process instability with material risk

Cron/report defaults:
- daily quality
- alert-driven escalation
- optional weekly summary

### Planeación / Logística / Supply chain / Finanzas operativas / BI
Prioritize according to the actual question, but usually emphasize:
- plan compliance
- cross-entity comparison
- target progression
- bottlenecks
- efficiency and performance impact

Report style:
- structured
- comparative
- planning-oriented

## Unknown roles
If a new role appears:
1. save it literally
2. map it to the nearest useful role class
3. refine if repeated often
