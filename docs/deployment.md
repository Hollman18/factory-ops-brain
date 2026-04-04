# Deployment guide

## Purpose
This guide explains how to apply this repository to a new OpenClaw agent workspace.

## Preconditions
Before applying the template, make sure the target OpenClaw environment already has:
- a working OpenClaw installation
- a writable workspace
- channel configuration handled separately
- credentials and data-source connections handled separately
- any organization-specific authorization rules identified

## What this template is responsible for
This repository provides:
- agent identity and operating rules
- role-based behavior
- onboarding logic
- security boundaries
- heartbeat standards
- cron/reporting standards
- module definitions
- report templates
- a copy-ready workspace skeleton

## What this template does not automatically configure
This repository does not automatically:
- connect data sources
- configure provider credentials
- authorize channels
- create environment-specific cron schedules unless the applying agent actively does so
- resolve tenant-specific security constraints

## Recommended application flow
1. Clone or copy this repository into a reachable location.
2. Review `README.md` and `docs/principles.md`.
3. Copy the contents of `workspace-template/` into the target OpenClaw workspace.
4. Review and adapt `AGENTS.md`, `SOUL.md`, `HEARTBEAT.md`, and automation files if needed.
5. Confirm the target channel identities, primary authorized user, and security boundaries.
6. Confirm data connections and hierarchy availability.
7. Create or adjust cron schedules for that environment.
8. Test onboarding with a new user.
9. Test one report and one high-signal alert path.

## Expected behavior when data is missing
If the target environment does not yet have a connected source for a given module, the agent should not fabricate an analysis. It should clearly state that the required data is not connected or not reliable and recommend contacting the data administrator.

## Minimum validation checklist
- workspace files copied successfully
- onboarding asks for name and role for new users
- role adaptation works
- sensitive data is not exposed
- heartbeat remains lightweight
- cron/reporting follows role defaults
- missing-data responses are honest and clear
