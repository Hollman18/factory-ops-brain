# Quality module

## Purpose
Analyze product/process quality performance, deviations, rejection, scrap, merma, and quality risk.

## Example KPIs/signals
- quality percentage
- rejection
- scrap
- merma
- defects
- reference/process quality ranking
- quality trend

## Operational meaning
The quality module should help identify where the process is producing unstable output, where customer risk may exist, and where containment or process review is needed.

## Expected analytical behavior
- identify worst references or processes
- compare quality across periods, entities, shifts, or references
- detect major deviations and their likely causes
- recommend containment when appropriate
- distinguish between isolated variation and sustained quality instability

## Role-aware interpretation
- Manager/director: summarize quality risk, trend, and business impact
- Supervisor: explain where deviation is occurring and what to contain first
- Operator: point to the most immediate process checks
- Maintenance: explain if quality deviations may be linked to equipment instability
- Quality roles: emphasize severity, likely cause, and containment

## Alerting expectations
Quality should contribute to heartbeat alerting when there is:
- rejection spike
- sustained deterioration
- reference/process quality collapse
- strong deviation likely to affect output or customer risk

## Missing-data rule
If quality data is not connected or not reliable, state that clearly and recommend contacting the data administrator.
