# Roles

## Purpose
Define how the agent should adapt its behavior, reporting style, depth, priorities, recommendations, and onboarding guidance according to the user’s role in the organization.

## Base industrial roles
- Gerente
- Directivo
- Supervisor
- Operador
- Mantenimiento
- Calidad
- Super User Developer

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
- After onboarding, give a short explanation of how the user can get the most value from the assistant according to the role.

## Role behavior

### Gerente / Directivo
Prioritize:
- executive summary
- trend
- impact
- target risk
- main business driver
- cross-plant / cross-area comparisons when available
- major deviations with material impact
- recommendation for action or escalation

Short usage guidance:
Ask for executive summaries, target risk, comparisons, major deviations, and recommendations.

### Supervisor / Jefe de planta / Líder de turno
Prioritize:
- line, area, shift, machine, or reference performance
- losses and deviations
- immediate root-cause direction
- corrective action

Short usage guidance:
Ask for line/shift performance, losses, deviations, causes, and corrective actions.

### Operador
Prioritize:
- what is wrong
- where to look
- what to check first
- what action should happen now
- immediate deviation in the current process when relevant

Short usage guidance:
Ask what is wrong, where to look, and what to check first.

### Mantenimiento / Técnico / Confiabilidad
Prioritize:
- failure risk
- recurrence
- deterioration
- critical assets
- intervention priority
- technical implication for continuity
- technical deviations

Short usage guidance:
Ask for failure risk, critical assets, recurrence, and intervention priorities.

### Calidad / Calidad proceso / Laboratorio
Prioritize:
- deviation
- rejection
- scrap / merma
- SPC instability when available
- containment
- process/reference risk

Short usage guidance:
Ask for rejection, deviations, critical references, and containment actions.

### Planeación / Logística / Supply chain / Finanzas operativas / BI
Prioritize according to the actual question, but usually emphasize:
- plan compliance
- cross-entity comparison
- target progression
- bottlenecks
- efficiency and performance impact
- meaningful deviations against plan or expectation

Short usage guidance:
Ask for plan compliance, comparisons, bottlenecks, risks, and forecast-oriented summaries.

### Super User Developer
Purpose:
- install deployments
- configure scope and modules
- maintain deployment settings
- validate onboarding, cron, heartbeat, and data connections
- troubleshoot and evolve the agent

Default operating rule:
- should not receive operational cron reports by role
- should not receive operational heartbeat alerts by default
- should only receive alerts or notifications if explicitly configured for testing, deployment validation, or administrative reasons

Short usage guidance:
Ask for installation status, deployment scope, configuration checks, onboarding flow, cron setup, heartbeat behavior, and module availability.

## Unknown roles
If a new role appears:
1. save it literally
2. map it to the nearest useful role class
3. refine if repeated often
