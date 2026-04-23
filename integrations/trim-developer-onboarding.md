# Trim Developer Onboarding for Factory Ops Brain Integration

## Goal
Help Trim developers integrate Factory Ops Brain cleanly and quickly.

## Mental model
- Trim = control plane
- Factory Ops Brain = intelligence plane
- Trim Connectors = data/access plane

## What Trim must provide to the agent per session
### Required session bootstrap
- tenant_id
- tenant_name
- user_id
- user_name
- role
- role_class
- selected plant/site/line/machine scope
- timezone
- language
- available sources
- allowed operations
- connector bindings summary
- current screen or interaction context when available

## What Trim should own
- tenant registry
- user registry
- role mapping
- profile/preferences persistence
- session context assembly
- consolidated KPI and historical access
- authorization and approval orchestration

## What Trim should not force Factory Ops Brain to infer
- current tenant
- current plant
- current user role
- available sources
- whether live access is enabled
- whether an operation requires approval

## Simplest integration path
### Step 1
Trim assembles a session bootstrap payload.

### Step 2
Trim sends the user message + bootstrap context into the Factory Ops Brain/OpenClaw runtime.

### Step 3
Factory Ops Brain answers from consolidated Trim data first.

### Step 4
When the answer requires live validation, Factory Ops Brain triggers a tenant-scoped request to Trim Connectors.

### Step 5
Trim renders the answer and stores conversation/context updates.

## Recommended developer checklist
- ensure every turn has tenant_id
- ensure every turn has user role
- ensure every turn has selected scope
- ensure live-access capability is explicit
- ensure approvals are explicit, not implied
- ensure source failures return structured status/errors
- ensure historical KPI access is available without live connectors when possible

## Success condition
A Trim developer can wire the system without relying on hidden assumptions or model memory.
