# Incident Report — May 2026 Analytics Outage

## Summary

On May 14, 2026, the analytics query service experienced a 47-minute outage.

The outage affected dashboard refreshes in InsightBoard and delayed several scheduled reports.

DocuPilot remained available, but some answers referencing analytics summaries were stale.

## Root Cause

A schema migration changed the name of the field `customer_region` to `region_code`.

One downstream query still expected the old field name.

The failed query caused repeated retries and overloaded the analytics worker pool.

## Resolution

Engineering rolled back the migration and restarted the worker pool.

The incident was resolved at 10:42 AM Central Time.

## Follow-up Actions

1. Add migration contract tests.
2. Add worker pool saturation alerts in SignalWatch.
3. Update the runbook for analytics schema changes.
4. Require product owner approval before changing shared reporting fields.

## Lesson Learned

The outage showed that schema changes need stronger validation before deployment.
