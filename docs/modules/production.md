# Production module

## Purpose
Analyze output, throughput, plan compliance, and production rhythm.

## Example KPIs/signals
- produced units
- throughput
- plan compliance
- actual pace vs expected pace
- bottlenecks

## Operational meaning
The production module should help determine whether the plant is producing at the required pace, where output is being constrained, and how current performance affects target compliance.

## Expected analytical behavior
- compare production output across periods and entities
- detect capacity loss and bottlenecks
- connect production behavior to OEE, maintenance, or target risk when relevant
- explain whether shortfalls appear structural or situational

## Role-aware interpretation
- Manager/director: summarize production attainment and target risk
- Supervisor: identify where pace is being lost and what should be corrected
- Operator: explain immediate process checks
- Maintenance: connect output loss to technical instability when relevant

## Alerting expectations
Production should contribute to heartbeat alerting when there is:
- strong shortfall vs expected pace
- sustained underproduction
- bottleneck concentration with material business impact

## Missing-data rule
If production data is not connected or not reliable, state that clearly and recommend contacting the data administrator.
