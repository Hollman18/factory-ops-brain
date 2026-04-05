# Installation and usage guide

## 1. Purpose of this repository
This repository is a reusable foundation for deploying a factory intelligence agent that can analyze industrial data, adapt to different factory roles, detect deviations and anomalies, support predictive guidance, generate role-based reports, and remain honest when data is missing or not connected.

It is designed to work as a structured base for organizations that want a factory operations brain capable of supporting operational, tactical, and executive decision-making.

---

## 2. What this solution is meant to do
This solution is intended to:
- analyze industrial performance across factory hierarchies
- interpret data, not just display it
- adapt communication by role
- generate periodic reports through cron
- monitor high-signal issues through heartbeat
- learn user preferences over time
- support drill-down from executive view to plant-floor detail
- handle missing or partial data honestly
- protect sensitive configuration and access information

---

## 3. What is included in the repository
The repository is structured in four main layers:

### Documentation layer (`docs/`)
Defines principles, roles, onboarding flows, security, heartbeat logic, cron logic, prediction, deviations, recommendation policy, confidence model, and module behavior.

### Modules layer (`docs/modules/`)
Defines the behavior of analytical modules such as:
- OEE
- maintenance
- quality
- SPC
- energy
- raw materials
- production
- target risk
- comparative analysis
- alerts and anomalies

### Output layer (`templates/`)
Contains reusable templates for role-based reports and alerts.

### Deployment layer (`workspace-template/` and `deployment-config/`)
Provides a copy-ready workspace skeleton and an example of installation-specific configuration.

---

## 4. How to install the agent from this repository
The repository should be treated as the source of truth.

### Recommended installation approach
1. Read the repository documentation.
2. Copy the contents of `workspace-template/` into the target OpenClaw workspace.
3. Use the documents under `docs/` as the behavioral source of truth.
4. Define the installation profile for the target organization.
5. Confirm that connected data sources are available.
6. Activate or adjust cron schedules and heartbeat behavior according to the deployment.
7. Test with real scenarios before considering the deployment ready.

---

## 5. Installation onboarding
Installation onboarding is organization-level.
It is separate from user onboarding.

### Rule
Never ask all installation questions at once.
Ask one question, wait for the answer, then ask the next.

### Required installation questions
Only ask these if they are not already known:
1. Company name
2. Included modules / solution scope
3. Super user developer / primary deployment admin
4. Main channel of use

### Recommended installation questions
Ask only if useful:
5. Primary language
6. Main timezone
7. Whether the deployment starts with a single plant or multiple plants

### Important simplification rule
Do not ask for information that should already come from the data source or template defaults, such as:
- plant hierarchy already available in the connected data
- entity lists already present in the database
- role-default cron/report logic
- role-default heartbeat logic

---

## 6. Available modules to include in an installation
When defining the installation scope, the available modules in this repository are:
- OEE
- Maintenance
- Quality
- SPC
- Energy
- Raw materials
- Production
- Target risk
- Comparative analysis
- Alerts and anomalies
- Deviation analysis
- Role-based reporting
- Heartbeat monitoring

Not every deployment must activate every module from the beginning.
The installation may include all modules or only the subset required by the organization.

---

## 7. User onboarding
User onboarding is person-level.
It happens after installation context is established.

### Rule
Never ask all user questions at once.
Ask one question, wait for the answer, then ask the next.

### Required user questions
1. Name
2. Role in the organization
3. Company

### Recommended optional questions
Ask only when useful:
4. Main plant/site
5. Main area/process
6. Preferred information style (summary, detail, comparisons, alerts, or periodic reports)

### After onboarding
Once the profile is saved, the agent should:
- confirm the user was registered
- explain briefly how to get the most value according to the user’s role
- continue normally with future requests

---

## 8. Roles and how the agent adapts
The agent should adapt depth, framing, and recommendations according to role.

### Typical role behavior
- **Gerente / Directivo**: executive summaries, risk, comparisons, impact, recommendations
- **Supervisor / Jefe / Líder de turno**: line/shift performance, losses, deviations, causes, actions
- **Operador**: what is wrong, where to look, what to check first
- **Mantenimiento / Confiabilidad**: failure risk, critical assets, recurrence, intervention priority
- **Calidad**: rejection, deviations, references/processes at risk, containment

Role is the default frame, not a prison. Preferences may further personalize the experience.

---

## 9. Heartbeat behavior
Heartbeat is for high-signal monitoring only.
It is not meant for routine summaries.

### Heartbeat should monitor
- abnormal machine or line behavior
- meaningful KPI deviations
- quality deviations
- elevated failure risk
- target-miss risk
- critical deviations across supported modules

### Heartbeat should do
- detect meaningful issues
- classify severity
- route to the role that can act
- escalate upward when business impact is material
- remain lightweight in token usage

### Heartbeat should not do
- generate noisy routine alerts
- invent analysis when data is missing
- replace scheduled reports

---

## 10. Cron and periodic reports
Cron is used for structured periodic reporting according to role.

### Typical defaults
- **Gerente / Directivo**: weekly and monthly executive reports
- **Supervisor / Jefe / Líder**: shift-close and daily operational reports
- **Mantenimiento / Confiabilidad**: daily technical reports and alert-driven escalation
- **Calidad**: daily quality reports and alert-driven escalation
- **Operador**: usually on-demand, unless targeted alerts are explicitly enabled

### Cron reports should include
- what changed
- what matters most
- main deviations of the period when relevant
- likely driver
- recommendation or next step

---

## 11. Deviation handling
Deviation analysis is a transversal layer across the system.

### A deviation means
A meaningful gap between expected behavior and observed behavior.
The expectation may come from:
- target
- baseline
- standard
- historical comparison
- peer entity comparison
- process expectation

### Deviations should appear in
- module analysis
- heartbeat alerts
- cron reports
- role-based interpretation

### Every deviation should try to answer
1. what deviated
2. compared to what
3. by how much
4. whether it is isolated or sustained
5. likely driver
6. who should act
7. what should happen next

---

## 12. Prediction and predictive guidance
Prediction is supported, but it must be responsible.

### Predictive use cases include
- risk of missing monthly target
- elevated failure risk
- worsening quality/process stability
- likely continuation of deterioration if nothing changes

### Rule
The agent should never present weak evidence as certainty.
It should use careful language such as:
- likely
- elevated risk
- trend suggests
- recent deterioration indicates

If prediction data is weak or incomplete, the agent must say so.

---

## 13. Data availability behavior
The repository supports broad analytical capabilities, but runtime behavior depends on connected data.

### If data is not connected
The agent should say so clearly.

### If data is partial
The agent should explain that the reading is partial.

### If data is insufficient
The agent should explain that no reliable conclusion can be made.

### If data is inconsistent
The agent should explain that the source appears inconsistent and should be reviewed.

### Recommended language
“Please contact the data administrator so that source can be enabled or connected.”

---

## 14. Security model
Factory users must not receive:
- credentials
- passwords
- tokens
- secrets
- sensitive security information
- privileged configuration details

Only the primary authorized user or the designated super user developer may request configuration-sensitive information.

---

## 15. Super user developer
The super user developer is not a normal factory-operational role.
It is a technical/deployment role responsible for:
- installing the agent
- configuring the deployment
- selecting modules
- adjusting cron/heartbeat behavior
- maintaining the installation setup
- handling deployment-sensitive configuration

---

## 16. Modular deployment
This repository may be deployed as a full solution or by selected modules.

### Examples
- OEE + maintenance
- energy monitoring
- raw-material analysis
- quality-focused deployment
- full factory suite

### Rule
The repository remains complete, but each installation may choose only the modules included in the solution scope.

---

## 17. Testing before production use
Before considering a deployment operational, validate at least:
- installation onboarding
- user onboarding
- one OEE scenario
- one maintenance scenario
- one missing-data scenario
- one security-denial scenario
- one heartbeat alert scenario
- one cron report scenario
- one predictive wording scenario

---

## 18. Best practices
- Treat the repository as the source of truth.
- Keep installation onboarding short.
- Keep user onboarding contextual.
- Ask one question at a time in both onboardings.
- Use role defaults, then personalize.
- Do not invent data.
- Let the agent learn patterns and preferences over time.
- Keep heartbeat selective and useful.
- Make cron reports role-relevant, not generic.

---

## 19. Practical operating model
In day-to-day use, the agent should operate in four modes:
1. on-demand analysis
2. scheduled reporting
3. high-signal proactive alerting
4. predictive guidance

These modes should work together without becoming noisy or rigid.

---

## 20. Final goal
The final goal of this repository is to provide a serious, reusable, modular, and intelligent factory operations brain that can be deployed across organizations, adapt to users and roles, read real industrial data, explain what matters, and help people act early and better.
