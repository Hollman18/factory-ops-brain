# Control, Intelligence, and Data/Access Planes

## Purpose

This document makes the planes explicit so the system stops behaving like a single vague “agent”.

That vagueness is one of the root causes of:
- context loss
- weak tool calling
- ambiguous source routing
- excessive trust in model memory

---

## Plane 1: Control plane

## Owner
**Trim**

## Mission
Own the authoritative business and product context required to run the system safely and consistently across tenants.

## Control-plane responsibilities

Trim should own:
- tenant registry
- tenant isolation model
- user registry
- role mapping authority
- profile/preferences persistence authority
- session bootstrap assembly
- selected scope authority
- source availability summary
- allowed-operations summary
- approval orchestration
- audit-relevant product state
- product-side conversation/session persistence where shared consistency matters
- orchestration of UI/app state around the agent

## What the control plane must provide to each meaningful turn

At minimum, Trim should resolve or provide:
- `tenant_id`
- `user_id`
- user role / role class
- current scope selection
- timezone / locale
- available sources
- allowed operations
- approval requirements when relevant
- any existing consolidated KPI/business context already available

## What the control plane must not delegate to model inference

Trim must not expect the model to guess:
- which tenant this turn belongs to
- which plant/line/machine is in scope
- whether the user is authorized for live reads
- whether a connector is available
- whether an approval is required
- whether the UI-selected context changed since the last turn

If Trim does not provide this clearly, correctness becomes accidental.

---

## Plane 2: Intelligence plane

## Owner
**FactoryOpsBrain**

## Mission
Turn explicit context and evidence into useful industrial reasoning, source selection, and decision support.

## Intelligence-plane responsibilities

FactoryOpsBrain should own:
- industrial intent interpretation
- analytical reasoning patterns
- role-aware explanation and framing
- source-routing decisions
- evidence sufficiency decisions
- confidence expression
- anomaly interpretation
- comparative and causal interpretation
- recommendation generation
- guardrails about uncertainty and missing data
- memory-boundary behavior
- rules for when fresh/live evidence is required

## What the intelligence plane should explicitly do

For every turn, FactoryOpsBrain should answer internally:
1. what is the user actually asking
2. what scope matters
3. is the Trim-provided context sufficient
4. is consolidated data enough
5. is live evidence required
6. which source path should be used
7. how confident is the answer
8. what should be said to this role

## What the intelligence plane should not own

FactoryOpsBrain should not be the owner of:
- tenant registry
- user authorization enforcement policy source of truth
- connector implementation lifecycle
- runtime session engine
- channel transport execution
- arbitrary low-level plant connectivity as the default model

## Memory in the intelligence plane

FactoryOpsBrain may use memory for:
- continuity
- user preferences
- recurring terminology
- recurring industrial patterns
- known history from prior conversations

But it must not treat memory as sufficient authority for critical context.

### Critical decision rule
If a decision could materially affect correctness, safety, or authorization, the intelligence plane should require explicit context or explicit evidence.

Examples:
- recommending a shutdown escalation
- claiming a live source is healthy
- claiming a connector is available
- asserting a tenant/site scope
- deciding that a privileged operation is allowed

---

## Plane 3: Data/Access plane

## Owner
**trim-connectors**

## Mission
Provide tenant-scoped, policy-aware, auditable access to external industrial systems and data sources.

## Data/access-plane responsibilities

trim-connectors should own:
- connector definitions
- connector-specific auth handling
- connection lifecycle
- discovery/test/read operations
- source capability exposure
- normalized result/status/error envelopes
- live system access boundaries
- readiness/health reporting for connections
- source-side execution safety boundaries

## What the data/access plane should not own

trim-connectors should not own:
- industrial reasoning
- executive/supervisor/operator explanation
- final decision-support wording
- tenant/business product UI state
- long-lived product profile semantics

Its job is access and evidence, not meaning.

---

## Plane 4: Runtime execution substrate

## Owner
**OpenClaw runtime**

## Mission
Run the agent session, tools, files, memory, cron, heartbeat, and channel interactions.

## Runtime responsibilities

OpenClaw should own:
- model invocation runtime
- tool execution
- workspace/file mechanics
- local memory file mechanics
- cron/heartbeat execution
- session/channel runtime behavior
- environment integration for the agent process

## What runtime should not own conceptually

OpenClaw is not the product control plane and not the industrial intelligence definition.

It executes the system; it does not define product truth.

---

## Interaction model across planes

### Normal path
1. Trim resolves authoritative turn context
2. OpenClaw runs FactoryOpsBrain with that context
3. FactoryOpsBrain reasons over the request
4. FactoryOpsBrain uses Trim data first
5. FactoryOpsBrain invokes trim-connectors if fresh/live evidence is required
6. trim-connectors returns normalized evidence
7. FactoryOpsBrain interprets and responds
8. Trim persists product-relevant state as needed

---

## Why memory alone is insufficient

The model can remember, and that is useful.

But the following must not depend only on memory:
- tenant identity
- selected operational scope
- current permissions
- whether a source is enabled
- whether approval exists
- whether a connection is healthy
- whether recent data is still fresh enough for the current decision

Memory is probabilistic and stale-prone.
Operational systems need explicit grounding.

---

## What the model must not infer by itself

The model should not infer, unless explicitly supplied or freshly evidenced:
- active tenant
- active site/plant/line/machine scope
- active role and authorization state
- source connectivity status
- approval state
- whether a connector call is permitted
- whether missing data means zero
- whether a stale memory item still reflects current reality
- whether one tenant's pattern applies to another tenant

These are system facts, not language guesses.

---

## Practical litmus test

If a developer says “the agent should just know that from prior conversation,” the immediate question should be:

> Is that a convenience preference, or an authoritative operational fact?

If it is authoritative, it belongs to explicit context or explicit evidence, not to memory alone.

That single test will prevent a lot of architectural mistakes.