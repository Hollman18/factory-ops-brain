# Heartbeat rules for factory intelligence

## Objective
Use heartbeat only for high-signal, low-noise surveillance.
It should detect critical anomalies or risks and escalate to the right role.
It must not become a periodic reporting channel.

## High-signal conditions to monitor
- machine or line behavior outside recent baseline
- strong KPI deviation outside expected range
- sustained deterioration over recent comparable periods
- quality instability or rejection spike
- elevated failure-risk pattern
- trend suggesting monthly target miss

## Escalation guidance
- operational deviation -> Supervisor
- technical instability / failure risk -> Mantenimiento
- quality deviation -> Calidad
- target miss risk / material business impact -> Gerente or Directivo

## Alert format
Keep alerts short:
1. What changed
2. Severity
3. Probable cause
4. Who should act
5. Recommended immediate action

## Token discipline
- Use compact heuristics first
- Avoid long narratives
- Ignore weak/noisy changes
- Re-alert only if the issue worsens, persists materially, or changes scope

## Learning expectation
Over time, improve anomaly quality by learning:
- normal machine patterns
- recurrent deviation signatures
- which early signals usually precede bigger failures or target misses
