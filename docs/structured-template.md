# Structured template guide

## Purpose
This document explains how the repository is structured so it can be reused as a portable OpenClaw factory-agent template.

## Template layers

### 1. Documentation layer
The `docs/` folder defines how the system should behave:
- principles
- roles
- onboarding
- security
- heartbeat routing
- cron by role
- hierarchy and drill-down
- personalization
- severity and escalation
- module behavior
- data-availability rules

### 2. Output standardization layer
The `templates/` folder defines reusable report and alert patterns for different roles and automation flows.

### 3. Workspace implementation layer
The `workspace-template/` folder contains a copy-ready OpenClaw workspace skeleton.
This is the practical layer that should be copied into a target workspace.

## Why this structure matters
This separation helps the repository serve three purposes at once:
1. explain the system
2. standardize outputs
3. accelerate deployment into new OpenClaw agents

## Application rule
When a new agent applies this repository, `workspace-template/` should be treated as the implementation base, while `docs/` should be treated as the source of truth for the agent’s intended behavior.

## Missing-data rule
The template assumes broad analytical capability, but any specific deployment may have partial or missing data. That does not invalidate the template. It only changes what the running agent can answer with confidence.
