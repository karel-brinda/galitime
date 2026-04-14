# AGENTS.md

## Invariants

* The primary artifact is the top-level executable `./galitime`.
* The main intended use is to take `./galitime` out of the repository and run it directly.
* Python packaging is secondary. `pip install` must work, but packaging must adapt to the standalone script design – not the reverse.
* Do not refactor this into a normal package-first Python project.
* Do not move the main implementation under `galitime_pkg/`.
* Do not turn `./galitime` into a thin wrapper unless explicitly requested.
* Keep a single source of truth for CLI behavior and version metadata.
* Avoid duplicated implementations across `./galitime` and `galitime_pkg/`.

## Packaging

* `galitime_pkg/` exists to support installation, not to define the primary structure.
* If packaging needs adjustment, prefer packaging metadata, build wiring, or lightweight mirroring/symlinking.
* Do not 'simplify' the project by making `galitime_pkg/` the canonical implementation unless explicitly requested.

## Validation order

When changing packaging, entry points, or layout, test in this order:

1. Copy `./galitime` alone to a temporary directory and run it.
2. Run the top-level `./galitime` from the repo.
3. Install into a fresh virtual environment and run `galitime`.
4. Run the existing behavioral tests.

## Change rules

* Prefer minimal patches.
* Do not do broad cleanup just because the layout looks unusual.
* Keep README and tests aligned with the standalone-first design.
