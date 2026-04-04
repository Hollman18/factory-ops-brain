# KPI dictionary

## Purpose
Provide a shared semantic layer for factory metrics so the agent can interpret them consistently across deployments.

## Recommended fields per KPI
- metric name
- business/operational definition
- unit of measure
- formula or derivation logic when applicable
- whether higher is better or worse
- operational interpretation
- common drivers
- common failure/deviation patterns
- alertability / severity relevance
- roles most interested in the KPI

## Example KPI entries

### OEE
- Definition: overall productive effectiveness combining availability, performance, and quality.
- Unit: %
- Higher is better: yes
- Operational meaning: effective use of productive capacity.
- Common drivers: stops, reduced speed, rejects.
- Interested roles: gerente/directivo, supervisor, mantenimiento, calidad.

### Availability
- Definition: proportion of planned time that the asset/process is running.
- Unit: %
- Higher is better: yes
- Common drivers: failures, setups, long stops.

### Performance
- Definition: actual operating speed/output versus expected speed/output.
- Unit: %
- Higher is better: yes
- Common drivers: microstops, reduced speed, flow instability.

### Quality
- Definition: proportion of good output versus total output.
- Unit: %
- Higher is better: yes
- Common drivers: defects, startup instability, process drift.

### MTBF
- Definition: average operating time between failures.
- Unit: time
- Higher is better: yes
- Operational meaning: reliability stability.

### MTTR
- Definition: average time required to restore equipment/process after failure.
- Unit: time
- Higher is better: no
- Operational meaning: recovery efficiency.

### Downtime
- Definition: time lost due to stoppage or failure.
- Unit: time
- Higher is better: no
- Operational meaning: lost capacity and continuity risk.

### Rejection / Scrap / Merma
- Definition: output or material lost due to quality/process failure.
- Unit: %, units, kg, or source unit
- Higher is better: no
- Operational meaning: quality loss, waste, and possible cost impact.

### Production / Throughput
- Definition: produced output over a given period.
- Unit: source unit
- Higher is better: usually yes, within context
- Operational meaning: delivery pace and plan compliance.

### Target compliance
- Definition: actual achievement versus planned target.
- Unit: %, units, or source unit
- Higher is better: yes
- Operational meaning: delivery confidence and planning reliability.

## Rule
The dictionary should grow with deployment maturity and remain editable as each organization defines its own KPI semantics.
