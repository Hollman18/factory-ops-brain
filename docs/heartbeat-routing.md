# Heartbeat routing

## Purpose
Heartbeat exists for high-signal monitoring and escalation, not for routine summaries.

## Core rules
- Keep token use low.
- Prefer compact checks.
- Alert only when the issue matters operationally.
- Route to the role that can best act.
- Escalate upward when business impact is material.

## Detection rules
Heartbeat should detect:
- abnormal behavior vs recent baseline
- KPI deviation outside expected range
- deterioration across comparable periods
- quality instability
- elevated failure-risk pattern
- target-miss risk
- major cross-entity anomaly
- critical deviations in any supported module

## Severity-aware routing

### Informational
Use sparingly. Usually no alert unless there is specific user preference.

### Warning
Alert the role that can act directly.
Examples:
- supervisor for operational deviation
- maintenance for emerging technical deterioration or technical deviation
- quality for quality drift or process deviation

### Critical
Escalate quickly and explicitly.
Examples:
- severe target risk -> gerente/directivo
- critical technical instability -> maintenance + supervisor, and management if impact is material
- major quality event -> quality + supervisor, and management if impact is material
- major cross-entity or sustained deviation -> role responsible for action, plus management when impact is material

## Routing logic
- operational issue / operational deviation -> Supervisor / Jefe de planta / Líder de turno
- technical instability / failure risk / technical deviation -> Mantenimiento / Confiabilidad
- quality deviation -> Calidad
- material target risk / business impact -> Gerente or Directivo
- Super User Developer -> no operational heartbeat routing by default; only explicit administrative/testing monitoring if configured on purpose

## Personalization rule
Heartbeat routing should consider role defaults plus user preferences when they exist.

## Missing-data rule
If a heartbeat check cannot be performed because the source is not connected or the data is not reliable, the agent should not fabricate an alert. It should remain honest about the lack of monitoring input.
