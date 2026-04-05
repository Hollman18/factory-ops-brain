# SPC module

## Purpose
Analyze process stability, control behavior, and deviation patterns.

## Example KPIs/signals
- Cp / Cpk
- out-of-control signals
- process variability
- trend instability
- critical process points

## Operational meaning
The SPC module should help identify whether the process is under control, drifting, or behaving in a way that threatens quality consistency.

## Expected analytical behavior
- detect instability and process deviations
- identify variables or points with worst behavior
- compare process stability across periods or entities
- explain process risk in clear operational terms
- distinguish isolated points from sustained out-of-control behavior

## Role-aware interpretation
- Manager/director: summarize process stability risk, deviations, and impact
- Supervisor: identify which process point needs immediate attention
- Operator: explain what variable or control point to verify first
- Quality: emphasize deviation, control status, and containment relevance

## Alerting expectations
SPC should contribute to heartbeat alerting when there is:
- repeated out-of-control behavior
- sharp process drift
- sustained instability in a critical variable
- process deviation with material risk

## Missing-data rule
If SPC data is not connected or not reliable, state that clearly and recommend contacting the data administrator.
