# Raw materials module

## Purpose
Analyze raw-material consumption, yield, loss, and deviation against standards.

## Example KPIs/signals
- specific consumption
- yield
- merma
- deviation against standard
- reference/process raw-material performance

## Operational meaning
The raw-materials module should help identify where material efficiency is being lost and whether the issue is localized by process, line, plant, or reference.

## Expected analytical behavior
- compare consumption by period, entity, or reference
- identify where material losses are highest
- detect raw-material deviations
- relate raw-material behavior to process performance when possible
- distinguish one-off deviations from chronic inefficiency

## Role-aware interpretation
- Manager/director: summarize efficiency loss, deviations, and impact
- Supervisor: identify where loss is concentrated and what to review
- Operator: explain immediate checks when useful
- Quality: note if material loss may be tied to rejection or process deviation

## Alerting expectations
Raw-materials should contribute to heartbeat alerting when there is:
- strong deviation vs standard
- sustained excess consumption
- major loss concentrated in a process or reference

## Missing-data rule
If raw-material data is not connected or not reliable, state that clearly and recommend contacting the data administrator.
