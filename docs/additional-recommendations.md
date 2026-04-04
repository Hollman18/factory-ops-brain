# Additional recommendations and likely blind spots

## 1. Add data contract documentation
Even if the hierarchy comes from the connected database, document what the agent expects from each source:
- entity identifiers
- names and labels
- units
- timestamps/timezone handling
- null/no-data behavior
- confidence/quality flags if available

## 2. Add timezone policy
For multinational or multi-plant deployments, define how dates, shifts, and monthly targets should be interpreted across time zones.

## 3. Add authorization by channel and tenant
If this ever serves multiple organizations or multiple trust boundaries, define isolation rules:
- per company
- per plant
- per tenant
- per channel identity

## 4. Add auditability of key actions
Track important decisions such as:
- profile created or changed
- cron changed
- preferences changed
- alert routing changed
- security-sensitive requests denied

## 5. Add report versioning and consistency rules
To avoid drift over time, define expected minimum sections for each report type.

## 6. Add KPI dictionary
For long-term maintainability, create a machine- and human-readable KPI dictionary:
- metric name
- definition
- unit
- higher-is-better or lower-is-better
- typical interpretation

## 7. Add ambiguity-handling rules
If an entity or period is ambiguous, define whether the agent should:
- infer from context
- ask a clarifying question
- default to a standard period

## 8. Add language and localization policy
If users may ask in Spanish, English, or mixed industrial language, define preferred response language behavior.

## 9. Add rollout maturity model
Useful stages:
- Stage 1: OEE + maintenance + role reporting
- Stage 2: quality + target risk + stronger anomaly logic
- Stage 3: energy + raw materials + SPC
- Stage 4: financial/operational optimization and cross-site benchmarking

## 10. Add human override policy
The user should always be able to:
- change cron frequency
- pause reports
- reduce alert volume
- request more or less detail
- reset or update preferences

## 11. Add distinction between descriptive, diagnostic, predictive, and prescriptive outputs
This helps both design and user expectations:
- descriptive: what happened
- diagnostic: why it happened
- predictive: what may happen
- prescriptive: what to do next

## 12. Add organization memory boundaries
Decide whether learned patterns should be global, per company, per plant, or per user profile to avoid contaminating one operation with another.
