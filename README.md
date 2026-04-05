# Factory Intelligence Agent Template

A reusable OpenClaw template for building factory intelligence agents that can operate across small plants, multi-site operations, and multinational manufacturing organizations.

This template is designed to support industrial analytics, operational reporting, anomaly detection, role-based decision support, hierarchy drill-down, secure onboarding, and adaptive user personalization.

---

## What this repository is

This repository provides a structured foundation for creating OpenClaw agents specialized in factory operations.

It is built to support:
- factory KPI analysis
- OEE interpretation
- maintenance intelligence
- operational anomaly detection
- role-based cron reporting
- lightweight heartbeat escalation
- secure multi-user onboarding
- hierarchy-aware drill-down
- gradual personalization over time

The goal is not just to answer KPI questions, but to help factory users understand:
1. what is happening
2. how serious it is
3. what is driving it
4. what should happen next

---

## Design philosophy

This template follows a few core principles:

- **Interpret, don’t just display** — the agent should explain operational meaning, not only show metrics.
- **Adapt by role** — managers, supervisors, operators, maintenance, and quality users need different framing.
- **Use real hierarchy** — the agent should work across corporation, region, plant, area, line, machine, shift, and reference when the data source provides that hierarchy.
- **Stay honest about data** — if a required source is missing, partial, insufficient, or inconsistent, the agent must say so clearly and recommend contacting the data administrator.
- **Protect sensitive information** — factory users should not receive secrets, credentials, or security-sensitive configuration.
- **Learn and personalize** — the agent should improve over time based on role, preferences, common questions, report style, and alert tolerance.

---

## Intended use cases

This template is suitable for scenarios such as:

- OEE monitoring and interpretation
- maintenance and reliability analysis
- operational reporting by role
- target-risk monitoring
- anomaly and alert routing
- cross-line / cross-plant comparisons
- industrial assistant deployments on Telegram or other OpenClaw-supported channels

It is designed to scale from:
- a single local plant
- a multi-line facility
- a multi-plant company
- a multinational industrial organization

---

## Core capabilities

### Industrial analytics
- OEE
- maintenance
- quality
- SPC
- energy
- raw materials
- production
- target risk
- comparative analysis
- alerts and anomalies

### Role-aware behavior
- Gerente / Directivo
- Supervisor / Jefe de planta / Líder de turno
- Operador
- Mantenimiento / Confiabilidad / Técnico
- Calidad
- Additional industrial roles via role mapping and preferences

### Operational automation
- cron reports by role
- heartbeat-based critical alerting
- escalation by severity and function
- user profile onboarding and adaptation

### Trust and safety
- no fabricated analysis when data is missing
- no exposure of secrets or sensitive security information
- separation between role framing and individual preferences

---

## Repository structure

```text
.
├── README.md
├── FACTORY_AGENT_BASE_CONFIG.txt
├── docs/
├── templates/
└── workspace-template/
```

### `docs/`
System design, principles, role behavior, security, drill-down logic, heartbeat routing, cron standards, personalization rules, and module definitions.

### `docs/modules/`
Detailed behavior for each analytical module:
- OEE
- maintenance
- quality
- SPC
- energy
- raw materials
- production
- target risk
- comparative analysis
- alerts and anomalies

### `templates/`
Reusable report and alert templates for different roles and automation flows.

### `workspace-template/`
A copy-ready workspace skeleton for new OpenClaw agents, including:
- AGENTS
- SOUL
- HEARTBEAT
- MEMORY
- profile structure
- automation scaffolding

---

## How data availability is handled

This template assumes the agent may support many analytical modules, but actual responses depend on the data sources connected in a given deployment.

If a source is not available, the agent should respond clearly, for example:

> I do not have that data connected right now. Please contact the data administrator so that source can be enabled or connected.

This means the architecture is broad, while the runtime behavior remains honest and safe.

---

## How role-based behavior works

Role defines the default response frame.
Preferences define personalization.

That means two users with the same role may still receive different:
- report cadence
- detail level
- comparison style
- preferred units
- alert sensitivity
- reporting format

The template is designed to support both standardized deployment and progressive personalization.

---

## Current implementation emphasis

This template is especially strong in:
- OEE
- maintenance
- reporting logic
- heartbeat/cron structure
- secure onboarding
- hierarchy-aware industrial behavior

The broader module architecture is already documented so the same template can grow with additional connected data sources over time.

---

## Recommended usage

### Option 1 — Use as a reusable OpenClaw workspace template
Copy the contents of `workspace-template/` into a new agent workspace, then adapt:
- channels
- authentication
- cron schedules
- user allowlists
- data integrations
- organization-specific preferences

### Option 2 — Use as a design reference
Use the docs and templates as a blueprint for building a custom industrial OpenClaw agent from scratch.

### Option 3 — Use as a Git-tracked base for multiple deployments
Maintain this repo as the source of truth, then clone and customize per customer, plant, or organization.

---

## What this template does not do

This template does **not** assume:
- every metric is already connected
- every module has live data on day one
- every user has the same reporting needs
- factory users are allowed to access secrets or privileged configuration

It is intentionally designed to be:
- modular
- honest about data availability
- secure by default
- adaptable across industrial contexts

---

## Recommended next steps after cloning

1. Review `docs/principles.md`
2. Review `docs/roles.md`
3. Review `docs/data-availability.md`
4. Review `docs/security.md`
5. Copy `workspace-template/` into the target OpenClaw workspace
6. Connect your plant/company data sources
7. Configure role-based cron schedules
8. Validate alert routing and onboarding behavior

---

## Status

This repository is intended to serve as a serious, reusable foundation for factory intelligence agents in OpenClaw and is structured for ongoing growth and refinement.
