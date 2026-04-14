# AGENTS.md

## Repository rules

- Keep patches minimal.
- Do not change test expectations.
- Prefer targeted fixes over refactors.
- Treat subprocess/shell wait status as the canonical exit code.
- GNU time output is for metrics only.
- Run the smallest relevant test first, then re-run the failing test.
- If parsing external tool output, validate shape and fail with an explicit error.

## Repository invariants

These are intentional design decisions. Do not change them unless explicitly asked.

- Version metadata is intentionally stored in `galitime_pkg/galitime.py`; do not move or copy version constants elsewhere.
- Do not refactor project layout for "cleanliness" unless the task explicitly requests it.
- Preserve public CLI behavior and import paths unless explicitly requested.
- Prefer minimal patches over broad reorganization.

## Before editing

Check whether the requested change conflicts with any repository invariant above.
If it does, keep the invariant and implement the request around it.

## When unsure

Default to preserving the existing pattern.
Ask: "Is this an intentional repository convention?" only if the task is blocked by ambiguity.
