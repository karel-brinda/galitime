# AGENTS.md

## Invariants

* The primary artifact is the top-level executable `./galitime`.
* The canonical implementation and version metadata live in `./galitime`, not in `galitime_pkg/`.
* The main intended use is to take `./galitime` out of the repository and run it directly.
* Python packaging is secondary. `pip install` must work, but packaging must adapt to the standalone script design, not the reverse.
* Do not refactor this into a normal package-first Python project.
* Do not move the main implementation under `galitime_pkg/`.
* Do not turn `./galitime` into a thin wrapper unless explicitly requested.
* Do not treat `galitime_pkg/galitime.py` as the canonical home for CLI behavior, version metadata, or imports.
* Avoid duplicated implementations across `./galitime` and `galitime_pkg/`.

## Packaging

* `galitime_pkg/` exists to support installation, not to define the primary structure or source of truth.
* If packaging needs adjustment, prefer packaging metadata, build wiring, or lightweight mirroring/symlinking.
* Do not "simplify" the project by making `galitime_pkg/` the canonical implementation unless explicitly requested.

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


## Tests

* Keep tests aligned with the standalone-first design.
* Prefer small, focused test directories with one clear purpose each.
* In Makefile-based tests, prefer a declarative `all:` target with named step targets.
* Keep test output readable and stable, with numbered step messages such as `[1/3] ...`.
* Prefer one semantic check per step target.
* Helper scripts should be silent on success and print only on failure.
* Preserve the validation order defined above when changing packaging, entry points, or layout.
* Platform-specific checks are fine when needed, but the default path should stay covered first.
* Do not shift tests toward a package-first worldview.
