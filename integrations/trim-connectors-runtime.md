# Trim Connectors Runtime Integration

## Purpose
Define the cleanest and simplest integration between Factory Ops Brain and Trim Connectors.

## Integration rule
Factory Ops Brain should not connect directly to arbitrary plant systems as its primary integration pattern.
Instead, it should request tenant-scoped access through Trim Connectors.

## Responsibilities
### Trim Connectors owns
- connector discovery
- test/discover/read execution
- live validation against external systems
- source capability exposure
- connection health/readiness
- policy-aware execution boundaries

### Factory Ops Brain owns
- industrial reasoning
- KPI interpretation
- anomaly interpretation
- comparative analysis
- role-aware explanation
- recommendation generation
- deciding when live validation is needed

## Recommended call flow
1. Agent receives tenant/user/session context from Trim.
2. Agent answers from Trim consolidated data when sufficient.
3. If fresh validation or live lookup is needed, agent requests Trim Connectors through a tenant-scoped integration layer.
4. Trim Connectors returns normalized result/status/errors/metadata.
5. Factory Ops Brain interprets the result and responds in industrial language.

## Minimal request contract
Factory Ops Brain should send at least:
- tenant_id
- plant_id or site scope
- user_role
- operation (test/discover/read)
- source_preference
- connection_id when already known
- requested metric/entity/time context

## Minimal response contract expected from Trim Connectors
- status
- source
- tenant_id
- scope
- data
- errors
- metadata
- next_actions

## Operational rule
If live data is not required, prefer Trim consolidated data first.
