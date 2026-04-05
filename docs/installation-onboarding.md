# Installation onboarding

## Purpose
Define the onboarding flow for setting up the agent in a new organization or deployment.

## Principle
Installation onboarding should be simple. It should only ask what is truly needed and should not ask for data that will already come from connected sources or from built-in role defaults.

## Installation-vs-user rule
Installation onboarding is organization-level.
User onboarding is person-level and must happen after installation context is established.

## One-question-at-a-time rule
Never ask all installation questions at once.
Always ask one question, wait for the answer, then ask the next one.

## Missing-only rule
If part of the installation context is already known, ask only for the missing fields.
Do not repeat confirmed installation information unnecessarily.

## Required installation questions
Only ask these if they are not already known:
1. What is the company name?
2. Which modules/solution scope are included in this installation?
3. Who will be the super user developer / primary deployment admin for this installation?
4. What will be the main channel of use?

## Recommended installation questions
Ask these only when useful, also one by one:
5. What is the primary language?
6. What is the main timezone?
7. Will this deployment start with a single plant or multiple plants?

## Structured module suggestion message
When asking about modules, present the available options clearly, for example:

Available modules in this repository:
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

Please tell me which modules should be included in this installation.

## Do not ask during installation onboarding
Do not ask for things that should come from connected data or existing defaults, such as:
- plant hierarchy that already comes from the data source
- entity lists already present in the database
- default cron/report logic already defined by role
- default heartbeat logic already defined by role and severity model

## Goal
Keep installation onboarding short, practical, and deployment-focused.
