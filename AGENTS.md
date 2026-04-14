# AGENTS.md

## Repository invariants

These are intentional design decisions. Do not change them unless explicitly asked.

- Version metadata is intentionally stored in `galitime/galitime.py`, do not move or copy version constants elsewhere.
- Do not refactor project layout for "cleanliness" unless the task explicitly requests it.
- Preserve public CLI behavior and import paths unless explicitly requested.
- Prefer minimal patches over broad reorganization.

## Before editing

Check whether the requested change conflicts with any repository invariant above.
If it does, keep the invariant and implement the request around it.

## When unsure

Ask: "Is this an intentional repository convention?"
Default to preserving the existing pattern

