# New agent setup prompt

Use this prompt with a new OpenClaw agent when you want it to apply this repository as its workspace foundation.

---

Apply the repository at this link as the complete factory-agent base for this OpenClaw workspace.

Instructions:
1. Read the repository structure and documentation first.
2. Copy the contents of `workspace-template/` into the current workspace.
3. Use the repository documentation under `docs/` as the source of truth for behavior, principles, roles, security, heartbeat, cron/reporting, hierarchy, personalization, and data-availability rules.
4. If files already exist, merge carefully without weakening security, onboarding, heartbeat discipline, or role-based behavior.
5. Preserve the rule that when a factory user has no profile, the agent must ask for name and role before answering data requests.
6. Preserve the rule that factory users must not receive secrets, credentials, or sensitive security information.
7. Preserve the rule that when data is not connected, partial, insufficient, or inconsistent, the agent must say so clearly and recommend contacting the data administrator.
8. Preserve role-based report defaults and heartbeat escalation defaults, while keeping them customizable by user preference.
9. Support all documented modules as agent capabilities, even when some data sources are not connected yet.
10. If any part of the repository cannot be applied directly in the current environment, explain exactly what is missing and what still needs to be done.

Success condition:
- the workspace reflects the repository’s factory-agent design
- core files are present
- role adaptation is in place
- onboarding is mandatory for new factory users
- security boundaries are preserved
- missing-data behavior is honest
- the agent is ready to operate with whatever data sources are already connected
