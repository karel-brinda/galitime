# AGENTS.md

## Core invariants

* The primary artifact is the top-level executable `./galitime`.
* The canonical implementation and version metadata live in `./galitime`, not in `galitime_pkg/`.
* The intended use is to copy `./galitime` out of the repository and run it directly.
* Packaging is secondary: `pip install` must work, but packaging must adapt to the standalone-script design, not the reverse.
* `galitime_pkg/` exists to support installation, not to define the primary structure or source of truth.
* If packaging needs adjustment, prefer metadata changes, build wiring, or lightweight mirroring over structural refactoring.
* Do not refactor this into a package-first project.
* Do not move the main implementation under `galitime_pkg/`.
* Do not turn `./galitime` into a thin wrapper unless explicitly requested.
* Do not treat `galitime_pkg/galitime.py` as the canonical home of CLI behavior, version metadata, or imports.
* Avoid duplicated implementations across `./galitime` and `galitime_pkg/`.

## Validation order

When changing packaging, entry points, or project layout, test in this order:

1. Copy `./galitime` alone to a temporary directory and run it.
2. Run the top-level `./galitime` from the repository.
3. Install into a fresh virtual environment and run `galitime`.
4. Run the behavioral tests.

## Change rules

* Prefer minimal patches.
* Do not do broad cleanup just because the layout looks unusual.
* Keep README and tests aligned with the standalone-first design.
* Keep tests small, focused, and stable in output.
* In Makefile-based tests, prefer a declarative `all:` target with named step targets and numbered step messages such as `[1/3] ...`.
* Prefer one semantic check per step target.
* Helper scripts should be silent on success and print only on failure.
* Platform-specific checks are fine when needed, but always keep the default path covered first.
* Do not shift tests toward a package-first worldview.
