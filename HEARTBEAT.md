# Factory heartbeat

Keep this heartbeat extremely lightweight.

## Purpose
Only surface events that are operationally important enough to justify an unsolicited alert.
Do not generate periodic summaries here. Periodic summaries belong to cron/report schedules.

## Check only for high-signal conditions
- abnormal machine or line behavior versus recent baseline
- KPI deviation outside expected range
- sustained deterioration across recent periods
- quality deviation or rejection spike
- elevated failure risk or instability pattern
- risk of missing monthly target based on current trend

## Response rules
- If there is no high-signal issue: reply exactly `HEARTBEAT_OK`
- If there is an issue: send a short alert with
  1. what changed
  2. severity
  3. probable cause
  4. who should be notified
  5. immediate recommendation

## Token discipline
- Prefer compact checks over broad analysis
- Avoid rehashing known non-issues
- Alert only on meaningful deviations
- Escalate only when impact or risk is material
