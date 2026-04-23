# Keep / Move / Refactor / Deprecate Map

## Purpose

This map defines how to evolve the repo from an industrial agent template into the canonical `FactoryOpsBrain` intelligence-plane repository for a SaaS architecture.

This is intentionally opinionated.

---

## Keep

These assets are valuable and should remain part of `factory-ops-brain`.

### 1. Industrial reasoning assets
Keep:
- `docs/modules/*`
- `docs/roles.md`
- `docs/principles.md`
- `docs/hierarchy-and-drilldown.md`
- `docs/severity-and-escalation.md`
- `docs/data-availability.md`
- `docs/kpi-dictionary.md`
- `docs/deviation-*`
- `docs/confidence-model.md`
- `docs/report-quality-standard.md`

Why:
- these define the actual industrial intelligence semantics
- they belong in the intelligence plane
- they are reusable across tenants and runtimes

### 2. Integration direction already introduced
Keep:
- `integrations/README.md`
- `integrations/trim-developer-onboarding.md`
- `integrations/trim-connectors-runtime.md`
- `docs/integrations/quick-integration-path.md`
- `examples/integrations/session-bootstrap.example.json`

Why:
- these are the bridge toward the correct architecture
- they already contain the right control/intelligence/data plane split

### 3. Analytics logic as transitional/reference assets
Keep, but not as the canonical future boundary:
- `analytics/db_query.py`
- `analytics/anomaly_detector.py`
- `analytics/schema_check.py`

Why:
- useful reference logic
- useful bootstrap implementation for early deployments
- useful for validating industrial heuristics

Important caveat:
- keep them as reference/bootstrap capability
- do not let them define the product architecture

### 4. OpenClaw deployment accelerators
Keep:
- `workspace-template/`
- `install.sh`
- `scripts/post_install_check.sh`
- `deployment-config/profile-example.json`

Why:
- OpenClaw remains the execution runtime
- deployment convenience still matters
- but these must become clearly secondary to the architecture docs

---

## Move

These concerns conceptually belong elsewhere, even if files are not physically moved immediately.

### 1. Tenant registry / identity / authorization ownership
Move conceptually to **Trim**:
- tenant registry
- user registry
- role mapping authority
- preference persistence authority
- approval orchestration
- session bootstrap assembly
- conversation/session state authority where product-wide consistency matters

Reason:
- this is control-plane responsibility, not intelligence-plane responsibility

### 2. External system connectivity ownership
Move conceptually to **trim-connectors**:
- connector definitions
- connector auth handling
- connection lifecycle
- discovery/test/read execution
- source capability exposure
- live system normalization
- connector health/readiness

Reason:
- FactoryOpsBrain should not be the primary owner of arbitrary plant-system connectivity

### 3. Low-level runtime/session execution ownership
Move conceptually to **OpenClaw runtime**:
- tool execution substrate
- channel/session runtime behavior
- local workspace memory mechanics
- cron/heartbeat execution engine
- agent runtime process model

Reason:
- this is runtime infrastructure, not intelligence-plane product logic

---

## Refactor

These are the most important items.

### 1. Refactor the repo narrative
Current narrative:
- reusable OpenClaw template for factory agents

Target narrative:
- canonical intelligence-plane repo for FactoryOpsBrain inside a Trim-centered SaaS system

Required refactor:
- README and top-level docs should lead with system architecture and repo boundaries
- OpenClaw template usage should become a deployment section, not the identity of the repo

### 2. Refactor analytics from “direct DB access pattern” to “source-backed intelligence capability”
Current problem:
- `analytics/` implicitly suggests the agent can own raw source access patterns directly

Target:
- analytics logic remains, but framed as one of:
  - reference algorithms
  - internal adapters
  - bootstrap deployment utilities
  - fallback execution paths for controlled environments

Not target:
- universal default integration pattern

### 3. Refactor memory positioning
Current problem:
- memory is well represented, but not strongly constrained as non-authoritative for critical decisions

Target:
- memory is explicitly useful for:
  - continuity
  - preferences
  - recurring patterns
  - user communication style
- memory is explicitly insufficient by itself for:
  - tenant identity
  - authorization
  - live source availability
  - selected operational scope
  - approvals
  - high-risk operational recommendations requiring fresh evidence

### 4. Refactor source routing into a first-class architectural concern
Current problem:
- route selection is implied in a few docs, not canonical

Target routing order:
1. use Trim-resolved session bootstrap and consolidated context
2. answer from Trim consolidated data when sufficient
3. invoke trim-connectors only for fresh/live validation or missing required data
4. do not guess missing source state from memory

### 5. Refactor repo structure to surface architecture first
Suggested information hierarchy:
1. architecture
2. repo responsibility map
3. plane definitions
4. integration path
5. industrial reasoning assets
6. deployment/runtime templates

### 6. Refactor wording from “agent” to “system + runtime + model behavior” where needed
Why:
- too much “the agent does everything” language creates ownership ambiguity
- the system is bigger than the model

---

## Deprecate

These patterns should be explicitly treated as old-model thinking.

### 1. Deprecate “the model can reconstruct missing operational context”
Do not rely on the model to infer:
- tenant
- site/plant/line/machine scope
- user role or permission state
- source availability
- whether live access is allowed
- whether approval is needed
- whether old memory still applies to the current turn

### 2. Deprecate “FactoryOpsBrain as full-stack agent package owner”
Old pattern:
- one repo feels responsible for runtime, domain, access, onboarding, and control state

New pattern:
- clear split across repos and runtime

### 3. Deprecate direct arbitrary plant connectivity as the default path from the intelligence repo
Why:
- weakens tenant isolation
- weakens auditability
- duplicates connector-plane concerns
- makes source routing ambiguous

### 4. Deprecate template/deployment docs as the architectural front door
They still matter, but they should no longer define the repo's identity.

### 5. Deprecate prompt-first system design
Prompts will exist later, but the current transformation should not be prompt-led.

---

## Practical mapping by repository area

| Area | Decision | Rationale |
|---|---|---|
| `docs/modules/` | Keep | Core industrial intelligence semantics |
| `docs/roles.md`, `docs/principles.md`, hierarchy/severity/confidence docs | Keep | Core reasoning behavior |
| `integrations/` | Keep + expand | Seed of the target architecture |
| `docs/integrations/` | Keep + align under architecture | Useful, but should reference canonical architecture docs |
| `analytics/` | Refactor | Keep as reference/bootstrap logic, not system boundary |
| `skills/` | Refactor | Reframe as runtime conveniences, not architecture core |
| `workspace-template/` | Keep + demote in prominence | OpenClaw deployment layer, not product identity |
| `templates/` | Keep | Useful output assets |
| `FACTORY_AGENT_BASE_CONFIG.txt` | Deprecate gradually | Valuable historical spec, but too monolithic and runtime/template-centric |
| deployment docs | Refactor | Keep, but subordinate to architecture |

---

## Simplest safe resolution of the repo's current ambiguity

If only one conceptual change is enforced, it should be this:

> `factory-ops-brain` is the intelligence plane, not the control plane, not the connector plane, and not the runtime itself.

Once that is explicit, many decisions become easier:
- Trim owns authoritative session/business context
- trim-connectors owns external source access
- OpenClaw owns execution/runtime behavior
- FactoryOpsBrain owns interpretation, reasoning orchestration, source selection logic, and response shaping

That is the highest-value simplification available.