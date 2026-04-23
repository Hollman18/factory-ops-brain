# Integrations

Canonical integration guides between Factory Ops Brain, Trim, Trim Connectors, and OpenClaw runtime.

## Goal
Keep integration simple, tenant-scoped, and reliable.

## Principles
- Trim is the control plane.
- Trim Connectors is the data/access plane.
- Factory Ops Brain is the intelligence plane.
- OpenClaw executes the agent runtime.
- The agent should not depend on implicit memory for critical context.
- Every operational turn should have tenant, user, role, scope, and source availability resolved.
