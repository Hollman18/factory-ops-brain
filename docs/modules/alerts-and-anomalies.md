# Alerts and anomalies module

## Purpose
Detect high-signal abnormalities and route them to the right role with minimal noise.

## Operational meaning
This module is responsible for noticing when the operation is behaving outside expected patterns and for deciding whether the deviation matters enough to alert someone.

## Expected analytical behavior
- detect behavior outside baseline
- detect sustained deterioration
- classify severity
- route alerts to the correct operational role
- avoid noisy or low-value alerting
- highlight probable driver and immediate action

## Severity model
At minimum:
- informational
- warning
- critical

## Routing expectations
- operations -> supervisor
- technical issue -> maintenance
- quality issue -> quality
- material business/target risk -> manager/director

## Missing-data rule
If the required monitoring data is not connected or is not reliable, say so clearly and recommend contacting the data administrator.
