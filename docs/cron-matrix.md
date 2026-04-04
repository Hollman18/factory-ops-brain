# Cron matrix

## Purpose
Formalize standard reporting cadence and content by role.

## Role defaults

### Gerente / Directivo
- Frequency: weekly, monthly
- Typical scope: cross-plant, plant, area, global trend
- Modules: OEE, target risk, production, major alerts, comparative analysis
- Detail: executive

### Supervisor / Jefe de planta / Líder de turno
- Frequency: shift-close, daily
- Typical scope: line, area, shift, machine
- Modules: OEE, production, anomalies, relevant maintenance/quality drivers
- Detail: tactical and actionable

### Operador
- Frequency: on-demand by default
- Typical scope: machine, line, current process
- Modules: immediate operational state
- Detail: short and direct

### Mantenimiento / Confiabilidad
- Frequency: daily technical, optional weekly
- Typical scope: machine, line, area, critical assets
- Modules: maintenance, downtime, failure risk, recurrence
- Detail: technical

### Calidad
- Frequency: daily, optional weekly
- Typical scope: process, reference, line, plant
- Modules: quality, rejection, SPC, process deviation
- Detail: analytical and containment-oriented

## Customization rule
All cron defaults may be customized by user preference and deployment needs.
