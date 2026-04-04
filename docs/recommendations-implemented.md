# Implemented design recommendations

## 1. Analytical user profile
User profiles should store not only name and role, but also analytical preferences:
- preferred detail level
- preferred report cadence
- preferred format (executive, tactical, technical, ranking, comparison)
- preferred units when applicable
- common KPIs and modules consulted
- alert tolerance

## 2. Separate role from preference
Every profile should distinguish:
- `role`: literal title from the user
- `role_class`: internal response category
- `preferences`: personalized behavior

## 3. Data confidence policy
Every answer should conceptually reason about one of these states:
- data available
- data partial
- data insufficient
- data inconsistent
- data not connected

## 4. Explainability as a transversal rule
Every module must do more than show a KPI. It should interpret likely drivers, severity, and next action.

## 5. Severity system
Alerts and findings should be classified at least as informational, warning, or critical.

## 6. Corporate vs plant lens
The agent should support:
- corporate view: cross-plant, target risk, strategic trends
- plant view: line, machine, shift, immediate action

## 7. Ask outside-role questions without becoming rigid
If a user asks for useful data outside their typical role focus, answer when authorized and data exists, but package the explanation in the style most useful to that user.

## 8. Fallback behavior for missing data
Recommended standard responses:
- No data connected: “I do not have that data connected right now. Please contact the data administrator so that source can be enabled or connected.”
- Partial data: “I can give you a partial reading, but not a complete conclusion.”
- Insufficient data: “The available information is not enough for a reliable conclusion.”
- Inconsistent data: “The available data appears inconsistent and should be reviewed before drawing conclusions.”

## 9. Include business objectives, not only technical KPIs
Where relevant, connect technical behavior to:
- monthly target risk
- production loss
- operational impact
- quality risk
- cost or efficiency impact

## 10. Modular growth policy
The architecture should allow new factory modules to be added without rewriting the role, heartbeat, cron, memory, or security model.

## Most valuable recommendation implemented
A dedicated principles document should exist and anchor all behavior, especially:
- no invented data
- role adaptation
- original units by default
- learning user preferences
- proper escalation
- drill-down on real hierarchy
- separation between capacity and data availability
- operational impact first
