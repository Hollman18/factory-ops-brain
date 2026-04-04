# Energy module

## Purpose
Analyze energy consumption, efficiency, and deviation versus expected behavior.

## Example KPIs/signals
- total consumption
- consumption per unit
- energy cost
- deviation versus standard
- cross-line or cross-plant efficiency

## Operational meaning
The energy module should help identify whether a process is consuming more energy than expected and whether the issue appears structural, operational, or localized.

## Expected analytical behavior
- compare consumption across periods and entities
- detect unusually high use or poor efficiency
- relate energy behavior to operational performance when possible
- distinguish high absolute consumption from poor specific efficiency

## Role-aware interpretation
- Manager/director: summarize efficiency trend and business/cost impact
- Supervisor: highlight where abnormal use is occurring operationally
- Operator: point to obvious process checks when meaningful
- Maintenance: note if abnormal consumption may reflect technical deterioration

## Alerting expectations
Energy should contribute to heartbeat alerting when there is:
- abnormal deviation vs standard or baseline
- sustained efficiency deterioration
- major cross-entity anomaly

## Missing-data rule
If energy data is not connected or not reliable, state that clearly and recommend contacting the data administrator.
