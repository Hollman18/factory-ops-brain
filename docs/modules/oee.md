# OEE module

## Purpose
Analyze overall equipment effectiveness across the available hierarchy and explain what is happening operationally.

## Core KPIs
- OEE
- Availability
- Performance
- Quality

## Operational meaning
The agent should never treat OEE as just a percentage. It should interpret OEE as a signal of effective productive capacity, hidden instability, and potential risk to target achievement.

## Expected analytical behavior
- compare periods, entities, shifts, references, plants, lines, machines, or areas
- detect meaningful rises, drops, stability, and deterioration
- identify the pillar that explains the main change
- connect pillar changes to likely operational losses
- explain whether the change is noise or sustained signal
- connect OEE behavior to production and target risk when relevant

## Typical questions
- How is OEE going?
- Which line has the worst OEE?
- Which shift performed best?
- What reference is best or worst by OEE?
- What changed vs last week/month?
- Which pillar is dragging the result down?
- What is the best-performing plant or line?

## Drill-down expectations
The agent must support roll-up and drill-down across whatever hierarchy the connected data source provides.

## Diagnostic logic
If OEE changes materially, the agent should try to determine:
1. which pillar changed most
2. whether the change is operationally meaningful
3. which entity or level explains the difference
4. what loss mechanism is the most likely driver

Typical guidance:
- Availability deterioration -> investigate breakdowns, changeovers, extended stops
- Performance deterioration -> investigate microstops, reduced speed, flow instability
- Quality deterioration -> investigate startup rejects, production rejects, process variability

## Comparison rules
The agent should support at least:
- period vs period
- entity vs entity
- shift vs shift
- reference vs reference
- plant vs plant
- line vs line
- machine vs machine
- today vs yesterday
- this week vs last week
- this month vs last month

## Role-aware interpretation
- Manager/director: summarize trend, impact, target risk, executive recommendation
- Supervisor: identify worst-performing area/line/shift, likely cause, corrective action
- Operator: explain what is wrong and what to check first
- Maintenance: highlight OEE loss when availability or repeated stoppages are the driver
- Quality: highlight OEE loss when quality is the driver

## Alerting expectations
OEE should contribute to heartbeat alerting when there is:
- strong drop vs recent baseline
- sustained deterioration
- severe underperformance in a key entity
- target-miss risk driven by current OEE trend

## Units and presentation
Use source units and percentages as delivered by the data source unless the user asks for another unit or format.

## Missing-data rule
If OEE data is not connected, partial, insufficient, or inconsistent, say so clearly and recommend contacting the data administrator.
