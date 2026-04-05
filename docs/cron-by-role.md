# Cron by role

## Principle
Periodic reports are standardized by role, but can be customized by each user. Cron standards are defaults, not rigid rules.

## Design rules
- Cron should deliver recurring value without creating noise.
- Report cadence should match the decision horizon of the role.
- The user may ask to change frequency, focus, module mix, format, or detail level.
- If a module lacks data, the report should say so clearly instead of fabricating analysis.
- Reports should highlight the most relevant deviations of the period when they matter.

## Default report logic by role

### Gerente / Directivo
Recommended defaults:
- weekly executive report
- monthly executive report

Typical content:
- main performance trend
- major rises/drops
- main deviations of the period
- target risk
- cross-entity comparison when relevant
- major operational driver
- management recommendation

### Supervisor / Jefe de planta / Líder de turno
Recommended defaults:
- shift-close report
- daily operational report

Typical content:
- line/area/shift summary
- key KPIs
- main losses or deviations
- likely cause
- next action for the following shift/day

### Operador
Recommended defaults:
- no recurring report by default
- targeted alerts only if operationally justified and explicitly enabled

Typical content when enabled:
- short status
- relevant deviation
- what to check
- what to do now

### Mantenimiento / Confiabilidad
Recommended defaults:
- daily technical report
- optional weekly reliability summary
- alert-driven escalation for meaningful risk patterns

Typical content:
- critical assets
- deterioration signals
- technical deviations
- recurrence
- intervention priority
- technical recommendation

### Calidad
Recommended defaults:
- daily quality report
- optional weekly quality summary
- alert-driven escalation for strong deviation

Typical content:
- rejection / scrap / merma summary
- critical process/reference
- quality deviations
- likely cause
- containment recommendation

### Planning / Logistics / BI / Finance-oriented roles
Recommended defaults:
- customized by business need
- often daily/weekly depending on planning cadence

Typical content:
- plan compliance
- output progression
- comparative performance
- bottlenecks, risks, and relevant deviations

### Super User Developer
Recommended defaults:
- no operational cron reports by default
- no role-based periodic reports by default
- only explicit administrative or testing cron if deliberately configured

Typical content when explicitly enabled:
- deployment validation
- configuration status
- onboarding validation
- module availability checks

## Customization policy
Users may request changes in:
- cadence
- recipients
- format
- entities covered
- comparison basis
- modules emphasized
- detail level

## Missing-data policy inside cron
If a scheduled report requires data that is unavailable, the report should explicitly say that the source is not connected or not reliable and recommend contacting the data administrator.
