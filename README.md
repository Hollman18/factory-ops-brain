# factory-ops-brain

Factory Ops Brain is a **factory intelligence framework** for OpenClaw-based industrial agents.

It is designed to run **per tenant** on top of an OpenClaw runtime, integrating with:
- **Trim** as control plane
- **trim-connectors** as data/access plane
- **OpenClaw** as the agent execution runtime

The goal is to keep the agent inside a strong operational “cube” so it responds with the right tenant context, uses the right sources, respects policy boundaries, and stays focused on factory intelligence instead of drifting into generic assistant behavior.

---

## Current status

This repository is now **very strong as a pre-integration baseline**.

It already includes:
- architecture and repo boundaries
- multi-tenant contracts and session bootstrap
- source routing and tenant-aware retrieval rules
- operational policies and safety boundaries
- runtime governance and enforcement design
- runtime core local implementation baseline
- local adapter baseline/mocks
- local harness and fixtures
- executable tests
- deployment and validation runbooks

### Honest statement
`factory-ops-brain` is **ready for real integration work**, but it is **not yet a fully connected production runtime**.

What is still mainly pending is:
- integration with **real Trim backends**
- integration with **real trim-connectors runtimes**
- integration with **real OpenClaw tenant runtimes**
- live validation with real permissions, approvals, contexts, and data sources

---

## System role in the target architecture

### Trim
Acts as the **control plane**:
- tenant/user/session context
- role and scope
- product UX and chat surface
- consolidated historical data
- approval orchestration and backend truth

### trim-connectors
Acts as the **data/access plane**:
- live discovery
- live read
- validation against external systems
- source capability exposure
- plant/system access boundaries

### Factory Ops Brain
Acts as the **intelligence plane**:
- industrial reasoning
- KPI interpretation
- anomaly interpretation
- context-aware responses
- policy-aware operational decision framing
- tenant-aware source selection and abstention

### OpenClaw
Acts as the **execution runtime**:
- runs one agent runtime per tenant
- loads the Factory Ops Brain workspace/framework
- executes the conversational/runtime flow

---

## What this repository now provides

## 1. Architecture and governance
- target architecture
- control/intelligence/data plane separation
- repo responsibility mapping
- memory/context/policy boundaries
- final consistency and governance notes

## 2. Multi-tenant contracts and context
- tenant context
- user context
- session bootstrap
- source availability
- source resolution
- policy context
- approval artifact

## 3. Retrieval and source routing
- deterministic source selection order
- tenant-aware retrieval layers
- fallback behavior
- confidence/evidence discipline
- abstention rules when source resolution is insufficient

## 4. Policies and boundaries
- allowed operations
- approval policy
- live access policy
- source trust policy
- missing-context policy
- cross-tenant isolation
- factory-intelligence-only mode

## 5. Runtime baseline
- runtime request/result models
- abstention, evidence, error and trace envelopes
- local runtime core
- approval/revalidation/permit chain
- local runtime harness
- runtime adapters base/mocks

## 6. Examples, fixtures and runbooks
- integration payload examples
- runtime examples
- fixtures for local simulation
- OpenClaw per-tenant deployment guidance
- Trim integration checklists
- trim-connectors integration checklists
- real-world validation checklists

## 7. Validation
- executable test suite
- runtime, contracts, policies and routing validation
- local end-to-end scenarios with harness + fixtures

---

## Repository structure

```text
factory-ops-brain/
├── README.md
├── FACTORY_AGENT_BASE_CONFIG.txt
├── contracts/
├── context/
├── retrieval/
├── policies/
├── runtime/
├── integrations/
├── examples/
├── tests/
├── analytics/
├── automation/
├── templates/
├── workspace-template/
├── docs/
└── legacy/
```

### Canonical domains
- `contracts/` → cross-boundary and backend-issued schemas
- `context/` → bootstrap and context templates/examples
- `retrieval/` → source routing and tenant-aware retrieval rules
- `policies/` → operational and safety boundaries
- `runtime/` → runtime models, services, adapters, harness
- `integrations/` → Trim / trim-connectors / OpenClaw integration guidance
- `examples/` → payloads and runtime examples
- `tests/` → executable validation
- `docs/` → architecture, deployment, readiness, audits, runbooks

### Preserved/supporting domains
- `analytics/` → preserved analytical utilities and assets
- `automation/` → automation-related scaffolding
- `templates/` → reusable templates
- `workspace-template/` → OpenClaw workspace foundation
- `legacy/` → preserved non-canonical historical/reference material

---

## Runtime model

The repository now supports a local conceptual/executable path like this:

1. load `session-bootstrap`
2. validate context and ownership
3. normalize intent and scope
4. resolve source
5. evaluate policy
6. validate approval when required
7. revalidate backend truth when required
8. emit `ExecutionPermit` when allowed
9. hand off to adapter layer
10. build runtime result or abstention

This path is already modeled, documented, and locally exercised through tests and harnesses.

---

## What is still intentionally not claimed

This repository should **not** be described yet as:
- a fully connected production application
- a complete live runtime already integrated with customer systems
- a replacement for real backend, connector, or deployment work
- sufficient on its own without tenant-specific OpenClaw/Trim/trim-connectors integration

---

## What remains after this baseline

After the current work, the remaining gap is mainly:

### Real integration
- real OpenClaw tenant runtime setup
- real Trim backend/session/bootstrap integration
- real trim-connectors integration
- real backend truth, approvals, and revalidation hooks

### Real validation
- real historical path validation
- real live path validation
- real denied/approval path validation
- real cross-tenant isolation validation
- real refresh/revocation validation

### Known residual caveat
A preserved residual area still exists under `analytics/mqtth/`.
It is explicitly documented and isolated, but it remains preserved/supporting material rather than the cleanest canonical runtime domain.

---

## Recommended use now

### Per tenant
1. deploy an OpenClaw runtime for the tenant
2. load/apply Factory Ops Brain into that workspace/runtime
3. connect Trim as control plane
4. connect trim-connectors as data/access plane
5. run the validation checklists and real-world pilot checks

### For developers
Use this repo as the **source of truth for pre-integration behavior**, contracts, runtime semantics, local validation, and integration guidance.

---

## Final honest summary

`factory-ops-brain` is now:
- **very strong as a factory intelligence framework**
- **very strong as a multi-tenant pre-integration baseline**
- **strongly prepared for real integration work**

The main remaining work is no longer large-scale repo design.
The main remaining work is:
- **real integration**
- **real deployment per tenant**
- **real validation in live environments**
