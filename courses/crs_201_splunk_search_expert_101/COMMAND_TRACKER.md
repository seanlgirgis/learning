# SPL Command Tracker

## Purpose

This file tracks SPL commands, functions, and search patterns introduced in this course.

Each entry should eventually answer:

- What does it do?
- Where did we learn it?
- What is the smallest working example?
- What common mistake should Sean avoid?
- Should this be added to the shared cookbook?

## Command table

| Command / Function | Type | Introduced In | Purpose | Small Example | Common Mistake | Add to Cookbook? |
|---|---|---|---|---|---|---|
| search | Search command | Module 1 | Basic event search | `error` | Staying too broad after finding relevant events | Yes |
| keyword search | Search pattern | Module 1 | Find events containing one or more raw terms | `failed login` | Assuming keyword order means exact phrase matching | Yes |
| incident symptom search | Search pattern | Module 1 | Search for events that match the reported symptom | `failed transaction` | Searching story details instead of reusable symptom patterns | Yes |

## Types

Use these categories:

- Search command
- Transforming command
- Streaming command
- Field command
- Eval function
- Time function
- Lookup command
- Visualization command
- Optimization pattern
- Troubleshooting pattern

## Notes

Add commands as they appear in the course. Do not try to preload the whole SPL language.
