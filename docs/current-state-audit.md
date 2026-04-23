# Current State Audit

## Executive summary

`factory-ops-brain` is currently a **strong documentation/template repo for an industrial OpenClaw agent**, not yet a canonical SaaS intelligence-plane repo.

That distinction matters.

Today the repository is optimized for:
- OpenClaw workspace bootstrapping
- industrial prompting and behavior shaping
- role-aware reporting rules
- analytics scripts against a customer PostgreSQL schema
- deployment guidance for a single agent/workspace pattern

It is **not yet cleanly shaped** as:
- a multi-tenant intelligence plane
- a runtime-facing application boundary with explicit context contracts
- a source-routing orchestration layer across Trim and trim-connectors
- a system with hard separation between control plane, intelligence plane, and data/access plane

The repo already contains useful seeds for that transition, especially under `integrations/` and `docs/integrations/`, but the canonical architecture is still mostly implicit and partially mixed with the old template-first approach.

---

## What exists today

### 1. OpenClaw workspace/template layer dominates the repo

Main evidence:
- `README.md`
- `FACTORY_AGENT_BASE_CONFIG.txt`
- `workspace-template/`
- `AGENTS.md`, `SOUL.md`, `HEARTBEAT.md`, `USER.md`, `MEMORY.md`
- `install.sh`
- `docs/deployment.md`
- `docs/structured-template.md`
- `docs/repo-structure-blueprint.md`

This is the repo's center of gravity today.

The current mental model is:
1. define how the factory agent should behave
2. provide a reusable OpenClaw workspace skeleton
3. plug analytics/data access into that workspace
4. let the model operate with industrial guidance and some scripts

That is useful, but it biases architecture toward **agent template packaging** instead of **product system boundaries**.

### 2. Industrial domain knowledge is rich

The repo is strong in industrial intent and operator value.

Evidence:
- `docs/modules/*.md`
- `docs/roles.md`
- `docs/principles.md`
- `docs/hierarchy-and-drilldown.md`
- `docs/severity-and-escalation.md`
- `docs/data-availability.md`
- `docs/deviation-*`
- `docs/kpi-dictionary.md`

This material should be preserved. It is one of the repo's main assets.

### 3. Analytics logic exists, but as local scripts tied to assumed schemas

Evidence:
- `analytics/db_query.py`
- `analytics/anomaly_detector.py`
- `analytics/schema_check.py`
- `skills/data-connector/SKILL.md`

Current reality:
- useful as reference and bootstrap capability
- suitable for early deployments and schema-driven analytics
- tightly coupled to assumed SQL tables and naming
- oriented to direct DB access from the agent/runtime side
- not yet expressed as a clean intelligence-plane service boundary

This is one of the biggest architectural tensions in the repo.

### 4. Integration thinking has started, but is still thin and not yet canonical

Evidence:
- `integrations/README.md`
- `integrations/trim-developer-onboarding.md`
- `integrations/trim-connectors-runtime.md`
- `docs/integrations/quick-integration-path.md`
- `examples/integrations/session-bootstrap.example.json`

These files already point in the right direction:
- Trim as control plane
- FactoryOpsBrain as intelligence plane
- trim-connectors as data/access plane
- OpenClaw as runtime execution layer
- explicit per-turn bootstrap context
- no critical dependence on implicit memory

This is the correct direction.

But today those files are still **adjacent guidance**, not the organizing center of the repository.

### 5. Multi-tenant SaaS boundaries are not yet first-class

The repo mentions tenants in the integration docs, but the repository as a whole still behaves conceptually like:
- a reusable per-agent template
- a deployment package for a customer-specific workspace
- a local analytics + prompting foundation

What is still missing as first-class architecture:
- clear tenant boundary model across the whole repo
- canonical per-turn context resolution model
- explicit source selection hierarchy
- explicit distinction between durable system state vs agent memory
- explicit rules for what the model may not infer by itself
- explicit system responsibility map across Trim / FactoryOpsBrain / trim-connectors / OpenClaw

---

## Repo structure assessment

### Strong areas

#### `docs/`
Strong coverage of industrial behavior and operational logic.

Good for:
- role-aware intelligence behavior
- industrial analytical scope
- severity/escalation semantics
- hierarchical interpretation
- reporting conventions

Weakness:
- too many docs are organized around the old template/deployment worldview rather than the target SaaS architecture worldview.

#### `analytics/`
Useful bootstrap analytical capability.

Good for:
- proving the repo can do real industrial work
- encoding initial KPI/anomaly logic
- serving as reference behavior for future services

Weakness:
- direct DB pattern encourages bypassing Trim and trim-connectors
- schema assumptions are embedded close to execution
- multi-tenant and source-routing concerns are not encoded as architecture

#### `workspace-template/`
Good deployment accelerator for OpenClaw-based agent workspaces.

Weakness:
- too central for the target future architecture
- risks making FactoryOpsBrain look like “the whole agent package” instead of “the intelligence plane”

#### `integrations/`
The most strategically important folder for the future direction.

Weakness:
- still small and not yet governing the rest of the repo
- important ideas exist, but they have not yet displaced the older repo narrative

---

## Main architectural conflicts detected

### Conflict 1: Template repo vs product-plane repo

Current state:
- the repo presents itself mainly as a reusable OpenClaw workspace/template

Target state:
- the repo should present itself primarily as the **canonical intelligence-plane definition** for the FactoryOpsBrain product

Why this matters:
- if not resolved, developers keep mixing runtime behavior, domain logic, deployment scaffolding, and system-of-record responsibilities
- this leads to context loss, hidden assumptions, and weak integration boundaries

### Conflict 2: Agent memory vs system context

Current state:
- the repo strongly embraces OpenClaw memory patterns
- that is useful for personalization and continuity
- but the broader repo does not yet draw a hard line between:
  - memory for convenience and continuity
  - authoritative context required for critical decisions

Target state:
- the agent may remember
- but critical decisions must rely on resolved system context from Trim and/or explicit source reads
- memory cannot be treated as the sole authority for tenant, scope, authorization, source availability, or operational approvals

### Conflict 3: Direct analytics access vs explicit data/access plane

Current state:
- analytics scripts and skills encourage direct DB-centric querying patterns

Target state:
- FactoryOpsBrain should prefer:
  1. Trim consolidated context/data
  2. trim-connectors for tenant-scoped live access when needed
- direct DB analytics should become a transitional/internal implementation detail, not the default mental model

### Conflict 4: Prompting-first architecture vs orchestration-first architecture

Current state:
- many materials describe what the agent should say and how it should behave

Target state:
- canonical architecture must first answer:
  - what context enters each turn
  - which plane resolves what
  - how source routing is decided
  - when live access is triggered
  - what the model is forbidden to infer

Prompting comes later, not first.

---

## Current maturity assessment by capability

### A. Industrial reasoning model: medium-high
Strong conceptual maturity.

### B. OpenClaw workspace packaging: high
Well developed.

### C. SaaS multi-tenant architecture: low-medium
Emerging, but not yet repo-defining.

### D. Integration contract thinking: medium
Correct direction exists, but still thin.

### E. Source routing / tool calling architecture: low-medium
Intent exists, but the current repo does not yet provide a canonical orchestration model.

### F. Separation of responsibilities across repos: low-medium
Partially documented, not yet explicit enough to remove ambiguity.

---

## What should be considered the real current state

The honest description is:

> `factory-ops-brain` is currently a reusable industrial OpenClaw agent foundation with some analytics implementation and early integration guidance toward Trim + trim-connectors, but it is not yet fully reframed as the canonical intelligence plane inside a real SaaS architecture.

That is the right starting point for the next step.

---

## Implications for the target redesign

The architectural transformation should not throw away the repo's strengths.

What must survive:
- industrial semantics
- role-aware reasoning goals
- hierarchy/drill-down logic
- severity/escalation logic
- honest missing-data behavior
- useful analytics heuristics as reference implementations
- OpenClaw deployment practicality

What must change:
- repo narrative
- canonical boundaries
- source-routing logic
- authority model for context
- treatment of memory
- ownership split with Trim and trim-connectors

---

## Final audit conclusion

The repo has real value, but today it still mixes four things that should be separated conceptually:
1. industrial reasoning rules
2. local bootstrap analytics
3. OpenClaw workspace packaging
4. SaaS system architecture

The correct next move is **not** to add more decorative docs or more prompts.

The correct next move is to make the architecture canonical and explicit:
- Trim = control plane
- FactoryOpsBrain = intelligence plane
- trim-connectors = data/access plane
- OpenClaw runtime = execution substrate

And then force the rest of the repo to align to that model.