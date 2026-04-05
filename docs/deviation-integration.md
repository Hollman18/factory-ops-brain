# Deviation integration across the system

## Purpose
Explain how deviation analysis should appear consistently in modules, heartbeat, cron, and role-based responses.

## Module integration rule
Every analytical module should support deviation thinking where relevant:
- detect deviation
- explain against what baseline/target/expectation
- estimate severity
- suggest likely driver

## Heartbeat integration rule
Heartbeat should monitor for:
- strong deviations
- sustained deviations
- cross-entity deviations
- deviations likely to create target, quality, or technical risk

## Cron integration rule
Periodic reports should include the most relevant deviations for the reporting period, framed according to role.

## Role integration rule
- Directivo/Gerente: deviation impact, target/business risk, recommendation
- Supervisor: operational deviation, driver, corrective action
- Operador: immediate deviation and first check
- Mantenimiento: technical deviation, deterioration, intervention priority
- Calidad: process/product deviation, containment, likely cause

## Personalization rule
User preferences may change which deviations are most visible, but critical deviations should not disappear.
