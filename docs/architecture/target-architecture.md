# Target Architecture

## Canonical statement

The target system is a **multi-tenant SaaS architecture** where `FactoryOpsBrain` operates as the **intelligence plane** inside a broader product composed of:
- **Trim** as the control plane
- **FactoryOpsBrain** as the intelligence plane
- **trim-connectors** as the data/access plane
- **OpenClaw runtime** as the agent execution substrate

This must become the canonical architectural model for the repository.

---

## Why this architecture exists

The current industrial-agent/template approach is not enough for a real SaaS system because it creates recurring failure modes:
- context loss between turns
- excessive dependence on model memory
- ambiguous ownership of data access
- weak tool/source routing
- unclear tenant boundaries
- unclear responsibility for approvals and authorization

The target architecture fixes that by making the model one component of a larger system, not the sole owner of context.

---

## System goal

Enable a FactoryOpsBrain agent to answer industrial questions and produce useful analysis in a SaaS environment where:
- tenants are isolated
- user/session/scope context is explicit
- source access is routed deliberately
- the model can remember useful patterns
- but the model is not trusted as the only source of truth for critical decisions

---

## High-level architecture

```text
User / UI / API client
        |
        v
      Trim
(control plane)
        |
        | session bootstrap + context + policy + consolidated data
        v
 FactoryOpsBrain
(intelligence plane)
        |
        | live/fresh reads only when needed
        v
 trim-connectors
(data/access plane)
        |
        v
 External industrial systems
(MES, SCADA, historian, ERP, CMMS, QMS, PLC-facing layers, APIs, DBs)

FactoryOpsBrain runs inside OpenClaw runtime
for channel/session/tool execution.
```

---

## Canonical flow per turn

### Step 1: Trim resolves authoritative context
Before the model reasons, Trim should resolve and pass at least:
- tenant identity
- user identity
- role / role_class
- current authorized scope
- timezone / locale
- source availability
- allowed operations
- approval requirements when relevant
- consolidated business/industrial context already available in Trim

This is not optional if the turn carries operational importance.

### Step 2: FactoryOpsBrain reasons over explicit context
FactoryOpsBrain should:
- interpret the user request
- classify intent
- decide whether available context and consolidated data are sufficient
- select the right industrial reasoning pattern
- decide whether live validation is required

### Step 3: Prefer Trim-backed consolidated data first
If Trim already provides the necessary KPI, history, scope, or business context, FactoryOpsBrain should answer from that.

Why:
- cheaper
- faster
- easier to audit
- more stable
- better for tenant isolation

### Step 4: Use trim-connectors only when needed
FactoryOpsBrain should call trim-connectors when it requires:
- fresh live readings
- source discovery
- connection validation
- capability checking
- external-system data not already consolidated in Trim

### Step 5: FactoryOpsBrain interprets returned evidence
Once evidence arrives, FactoryOpsBrain should:
- interpret it in industrial/business terms
- state confidence and limitations
- frame it by role
- recommend next actions
- avoid overstating certainty beyond the evidence

### Step 6: Trim stores durable product context as appropriate
Trim should persist product-relevant context such as:
- session state
- conversation state when needed
- preferences/profiles
- approvals/audit references
- business-side metadata

OpenClaw may hold runtime memory, but product authority should not live only there.

---

## Architectural principles

### 1. The model is not the control plane
The model should not be the authority for:
- tenant resolution
- user authorization
- approval state
- official source availability
- connection bindings
- policy enforcement

### 2. The model is not the data plane
The model should not own arbitrary direct connectivity to industrial systems as the default pattern.

### 3. The model is an interpreter and orchestrator of intelligence work
FactoryOpsBrain's core role is to:
- understand the question
- determine what evidence is needed
- route to the right source path
- interpret evidence
- express the answer in useful industrial language

### 4. Memory is helpful, not sovereign
The agent can remember:
- preferences
- recurring entities
- recurring user habits
- historical conversational context
- stable heuristics

But memory alone must not decide critical facts.

### 5. Explicit context beats hidden context
Any context that materially affects correctness, safety, or tenant isolation should be passed explicitly or fetched explicitly.

---

## What FactoryOpsBrain should become

`factory-ops-brain` should become the home of:
- canonical industrial reasoning architecture
- source-routing decision logic
- confidence/grounding rules
- role-aware interpretation logic
- memory-boundary rules
- integration expectations for Trim and trim-connectors
- reference analytics patterns
- OpenClaw deployment guidance for running the intelligence plane

It should stop behaving conceptually like:
- the full product
- the control-plane owner
- the connector platform owner
- the runtime owner

---

## Multi-tenant design stance

The system must assume:
- many tenants
- different source topologies per tenant
- different role models per tenant
- different scope hierarchies per tenant
- different connected capabilities per tenant
- different freshness requirements per workflow

Therefore the architecture cannot rely on:
- a globally shared implicit memory model
- loose assumptions about source availability
- hidden tenant binding inferred from conversation history alone

---

## Decision authority model

### Authoritative system facts should come from systems, not memory
Examples:
- current tenant
- current plant/site/line scope
- whether the user may ask for a given operation
- whether live reads are enabled
- whether a connector exists and is healthy
- whether an approval is required

### Memory may help with continuity but not override authority
Examples of valid memory use:
- preferred detail level
- preferred language/style
- usual comparison window
- known recurring problem areas
- previously discussed equipment names as soft hints

Examples of invalid memory-only use:
- assuming the same plant is still selected
- assuming the same approval still applies
- assuming the same connector remains available
- assuming yesterday's source health is still true now

---

## Source routing model

FactoryOpsBrain should explicitly reason about which source path to use.

### Preferred order
1. **Trim-provided context and consolidated data**
2. **trim-connectors live access** when fresh evidence is required
3. **local/reference analytics paths** only where intentionally allowed and clearly bounded

### Routing decision factors
- question type
- freshness requirement
- operational criticality
- available source coverage
- latency/cost tradeoff
- user authorization
- approval requirements
- connector health

This should be a system rule, not a prompt superstition.

---

## What not to design yet

Out of scope for this phase:
- detailed JSON contracts
- detailed prompt text
- detailed policies and policy engine rules
- testing strategy
- cosmetic repo cleanup

The job here is architectural clarity first.

---

## Success condition

The target architecture is successful when a developer can answer, without ambiguity:
- what Trim does
- what FactoryOpsBrain does
- what trim-connectors does
- what OpenClaw runtime does
- what context must be explicit each turn
- what the model may remember
- what the model must not infer by itself
- why the system does not depend on the model carrying the full operational context

That is the standard this repo should optimize for.