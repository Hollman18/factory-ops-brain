# Quick Integration Path

## Fastest clean path
1. Trim builds session bootstrap.
2. Factory Ops Brain receives tenant/user/role/scope/source context.
3. Factory Ops Brain uses Trim consolidated data first.
4. Factory Ops Brain uses Trim Connectors only when fresh/live validation is needed.
5. Responses stay role-aware and tenant-scoped.

## Why this path is preferred
- simpler
- less brittle
- less model-dependent
- easier to audit
- better tenant isolation
