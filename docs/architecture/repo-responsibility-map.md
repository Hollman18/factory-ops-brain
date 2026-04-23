# Repo Responsibility Map

## Purpose

This document answers one question with no ambiguity:

**Which repo or runtime owns what?**

---

## Canonical ownership map

| Component | Role in system | Owns | Must not own |
|---|---|---|---|
| **Trim** | Control plane | tenant/user/session context, scope, approvals, product-side persistence, consolidated data access, source availability summary | industrial reasoning, connector execution internals, runtime tool engine |
| **FactoryOpsBrain** | Intelligence plane | industrial reasoning, source routing, evidence sufficiency, confidence framing, role-aware interpretation, recommendation logic, memory boundaries | control-plane authority, connector platform ownership, runtime substrate ownership |
| **trim-connectors** | Data/access plane | connector lifecycle, source discovery/test/read, normalized live-access results, connection health and readiness | industrial explanation, business/user context authority, final answer semantics |
| **OpenClaw runtime** | Execution substrate | model execution, tools, file/memory runtime, cron/heartbeat, channel/session mechanics | business control-plane truth, intelligence product definition, external connector ownership |

---

## 1. Trim

## What Trim is
Trim is the **system-of-record control plane** for the SaaS product context around the agent.

## Trim is responsible for
- tenant registry and tenant isolation
- user registry and identity linkage
- role mapping authority
- selected scope authority
- preference/profile persistence authority
- approval/authorization orchestration at product level
- session bootstrap assembly
- consolidated KPI/business context delivery
- app/UI context delivery when relevant
- persistence of product-relevant conversation/session state

## Trim should hand FactoryOpsBrain
Per meaningful turn, Trim should provide enough explicit context so the intelligence plane does not have to guess critical facts.

Examples:
- who is asking
- which tenant they belong to
- what scope is selected
- what sources are available
- what actions are allowed
- whether live access is possible

## Trim should not delegate to FactoryOpsBrain
- authoritative tenant resolution
- authoritative scope resolution
- authoritative approval state
- product-side authorization truth
- source availability truth as a hidden assumption

---

## 2. FactoryOpsBrain

## What FactoryOpsBrain is
FactoryOpsBrain is the **intelligence plane**.

It is the part that should be best at deciding:
- what the request means
- what evidence is needed
- whether current evidence is enough
- how to interpret results industrially
- how to communicate the answer usefully for the user's role

## FactoryOpsBrain is responsible for
- intent interpretation
- industrial analytical logic
- anomaly interpretation
- comparative reasoning
- hierarchy-aware explanation
- confidence expression
- recommendation generation
- source-routing logic
- deciding when live reads are necessary
- deciding when the answer must remain limited because evidence is missing
- using memory carefully without over-trusting it

## FactoryOpsBrain may remember
- user preferences
- recurring entity names
- typical report framing
- prior discussion context
- recurring industrial patterns

## FactoryOpsBrain must not depend only on memory for
- tenant identity
- active scope
- current authorization state
- live source availability
- approval state
- fresh evidence for high-stakes conclusions

## FactoryOpsBrain should not own
- connector implementations
- connector credentials handling as the default product pattern
- runtime session engine
- control-plane persistence authority

---

## 3. trim-connectors

## What trim-connectors is
trim-connectors is the **data/access plane**.

It is the system that knows how to reach external industrial systems safely and consistently.

## trim-connectors is responsible for
- implementing connectors
- connection configuration lifecycle
- source discovery
- test/discover/read execution
- capability exposure
- normalized envelopes for success/error/status
- source readiness and health information
- policy-aware access boundaries for external systems

## trim-connectors should return
Not business prose, but evidence and execution truth:
- status
- source metadata
- normalized data payloads
- errors
- readiness info
- capability info
- next-action hints when appropriate

## trim-connectors should not own
- executive/supervisor/operator communication
- tenant business reasoning
- recommendation wording
- final answer composition

---

## 4. OpenClaw runtime

## What OpenClaw is
OpenClaw is the **runtime that executes the agent**.

It provides the practical environment in which FactoryOpsBrain runs.

## OpenClaw is responsible for
- model execution
- tools and tool calling
- local workspace files
- local memory files
- cron jobs and heartbeats
- session/channel execution
- runtime process behavior

## OpenClaw should not be confused with
- the product control plane
- the intelligence-plane definition
- the connector platform

It is the execution layer, not the business/system authority layer.

---

## Responsibility boundaries in one sentence each

- **Trim** decides the authoritative context of the turn.
- **FactoryOpsBrain** decides how to reason and what evidence is needed.
- **trim-connectors** obtains live/source evidence safely.
- **OpenClaw runtime** executes the agent session and tools.

If any component starts doing another component's job, ambiguity and fragility return.

---

## What this means for this repo

This repo should primarily document and implement the concerns that belong to **FactoryOpsBrain**:
- industrial reasoning model
- source-routing model
- evidence/grounding rules
- memory-boundary rules
- role-aware interpretation behavior
- expectations of Trim and trim-connectors
- OpenClaw deployment guidance only insofar as needed to run the intelligence plane

This repo should not drift into becoming the main home for:
- Trim control-plane implementation
- trim-connectors implementation details
- generic OpenClaw runtime ownership

---

## Final rule

When in doubt, ask:

1. Is this authoritative product context? → **Trim**
2. Is this industrial reasoning and decision support? → **FactoryOpsBrain**
3. Is this external source access? → **trim-connectors**
4. Is this model/tool/session execution? → **OpenClaw runtime**

That rule should be enough for most architectural decisions.