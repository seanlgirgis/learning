# Analytics Schema Change Runbook

## Purpose

This runbook explains how to safely change fields used by analytics reports.

## Before the Change

The engineer must identify all downstream dashboards, scheduled reports, and document summaries that depend on the field.

The engineer must run migration contract tests before merging the change.

The product owner must approve changes to shared reporting fields.

## During the Change

Deploy schema changes during the low-traffic maintenance window.

Monitor worker pool saturation, query failure rate, and dashboard refresh latency.

## After the Change

Confirm that InsightBoard dashboards refresh successfully.

Confirm that scheduled reports complete successfully.

Confirm that DocuPilot summaries that reference analytics data are refreshed.

## Rollback

If query failure rate rises above 5 percent for more than 10 minutes, rollback the schema change.
