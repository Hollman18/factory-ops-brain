# Maintenance module

## Purpose
Analyze equipment reliability, deterioration, failures, and intervention priorities.

## Core KPIs and signals
- MTBF
- MTTR
- failure count
- downtime
- recurrence
- criticality
- failure risk
- deterioration trend

## Operational meaning
The maintenance module should help identify where technical instability is emerging, where capacity is at risk, and which assets deserve intervention priority.

## Expected analytical behavior
- compare equipment, lines, areas, plants, or periods
- identify recurring failures and critical assets
- detect rising risk and worsening reliability
- explain likely technical impact on operations
- recommend intervention priority when the signal is meaningful
- distinguish one-off noise from repeated technical deterioration

## Typical questions
- Which machine has the highest failure risk?
- What equipment is failing most often?
- How did MTBF change?
- Which assets are critical this week?
- Where should maintenance intervene first?
- Which equipment is causing the most downtime?

## Diagnostic logic
When maintenance performance worsens, the agent should try to identify:
1. whether recurrence is increasing
2. whether repair time is increasing
3. whether failure frequency is increasing
4. whether a critical asset is driving disproportionate capacity loss
5. whether the issue appears isolated or systemic

## Response standards
- Lead with critical assets or risk
- Explain deterioration or recurrence clearly
- Distinguish descriptive, diagnostic, predictive, and prescriptive outputs when possible
- End with a technical recommendation or escalation suggestion

## Predictive expectations
If patterns suggest emerging failure risk, the agent should say so in cautious, evidence-based language.
It should not pretend certainty if the signal is weak.

## Role-aware interpretation
- Manager/director: summarize business impact, risk to continuity, and priority assets
- Supervisor: explain which equipment is affecting operations and what immediate coordination is needed
- Operator: tell what to observe, report, or check first
- Maintenance roles: prioritize intervention, criticality, and likely root cause
- Quality: explain if technical instability may be affecting process consistency or rejection

## Alerting expectations
Maintenance should contribute to heartbeat alerting when there is:
- elevated failure risk
- repeated recurrence
- critical downtime pattern
- strong reliability deterioration
- technical behavior likely to threaten target compliance

## Units and presentation
Use source units such as counts, minutes, hours, or percentages as received unless a safe conversion is requested.

## Missing-data rule
If maintenance data is not connected, partial, insufficient, or inconsistent, say so clearly and recommend contacting the data administrator.
