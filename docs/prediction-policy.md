# Prediction policy

## Purpose
Define how the agent should express predictive insights responsibly.

## Prediction types
- descriptive: what happened
- diagnostic: why it happened
- predictive: what is likely to happen next
- prescriptive: what should be done next

## Core rules
- Never present a weak signal as certainty.
- Be explicit about confidence when possible.
- Separate evidence-backed prediction from intuition or analogy.
- Use predictive language carefully: likely, emerging, elevated risk, early signal, trend suggests, etc.
- When evidence is too weak, say so clearly.

## Prediction use cases
- risk of missing monthly target
- emerging machine failure risk
- sustained deterioration likely to continue
- recurring quality/process instability
- expected worsening of a KPI if no action is taken

## Required ingredients for stronger prediction
Examples of useful evidence:
- repeated historical pattern
- consistent deterioration across comparable periods
- recurrence on the same entity
- strong baseline deviation
- aligned signal across multiple KPIs

## Alerting policy for predictions
Predictions may drive:
- heartbeat escalation when the predicted impact is material
- cron report commentary when the signal is relevant but not urgent

## Communication examples
Good:
- “If this trend continues, there is risk of closing the month below target.”
- “The recurrence pattern suggests elevated failure risk on this asset.”
- “Recent deterioration points to a likely continuation unless conditions change.”

Avoid:
- “This machine will fail tomorrow” unless evidence is exceptionally strong and justified.

## Missing-data rule
If the data required for prediction is weak, partial, or absent, the agent must not fabricate a predictive conclusion.
