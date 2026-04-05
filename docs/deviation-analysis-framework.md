# Deviation analysis framework

## Purpose
Define how the agent should detect, interpret, prioritize, route, and communicate deviations across all modules.

## Definition
A deviation is a meaningful gap between expected behavior and observed behavior.
The expectation may come from:
- standard
- target
- baseline
- comparable historical period
- peer entity comparison
- process control expectation

## Universal deviation dimensions
For any module, the agent should try to determine:
1. what deviated
2. compared to what expectation
3. by how much
4. whether it is isolated or sustained
5. what is the likely driver
6. who should act
7. what should happen next

## Deviation types
- target deviation
- baseline deviation
- cross-entity deviation
- process deviation
- quality deviation
- technical deviation
- efficiency deviation
- material-consumption deviation

## Severity logic
At minimum:
- informational
- warning
- critical

Severity should consider:
- magnitude
- persistence
- business impact
- spread across entities
- relationship to target risk or continuity risk

## Routing rule
Deviations should be routed to the role that can best act, then escalated upward if the business impact is material.

## Prediction link
A deviation is a present-state signal.
If the deviation persists, worsens, or aligns with known patterns, it may also support predictive guidance.

## Missing-data rule
If the expectation or comparison basis is unavailable, the agent should be explicit that deviation assessment is limited.
