# Operating modes

## Purpose
Define the major ways the agent may operate in practice.

## Mode 1 - On-demand analysis
The user asks a question and the agent responds immediately using the available data, hierarchy, role, and preferences.

## Mode 2 - Scheduled reporting
Cron generates role-based reports on a recurring cadence.

## Mode 3 - High-signal proactive alerting
Heartbeat watches for meaningful abnormalities and routes alerts to the role that should act.

## Mode 4 - Predictive guidance
The agent highlights likely future risk when supported by sufficient evidence.

## Rule
The same deployment may use all four modes, but each should remain clearly governed by role, severity, and data confidence.
