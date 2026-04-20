#!/usr/bin/env python3

import importlib.util
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_galitime_module():
    module_path = Path(__file__).resolve().parents[2] / "galitime"
    loader = SourceFileLoader("galitime_script", str(module_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        fail(f"unable to load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    mod = load_galitime_module()
    compact_result = mod.TimingResult(
        experiment="demo",
        run=1,
        command="true",
        extended=False,
    )
    extended_result = mod.TimingResult(
        experiment="demo",
        run=1,
        command="true",
        extended=True,
    )

    compact_lines = str(compact_result).splitlines()
    extended_lines = str(extended_result).splitlines()

    if compact_lines[0].split("\t") != list(mod.COMPACT_COLUMNS):
        fail("compact TimingResult header does not match COMPACT_COLUMNS")

    if extended_lines[0].split("\t") != list(mod.EXTENDED_COLUMNS):
        fail("extended TimingResult header does not match EXTENDED_COLUMNS")

    if len(compact_lines[1].split("\t")) != len(mod.COMPACT_COLUMNS):
        fail("compact TimingResult row width does not match COMPACT_COLUMNS")

    if len(extended_lines[1].split("\t")) != len(mod.EXTENDED_COLUMNS):
        fail("extended TimingResult row width does not match EXTENDED_COLUMNS")

    for key in (
        "backend",
        "fs_inputs",
        "fs_outputs",
        "major_page_faults",
        "minor_page_faults",
        "swaps",
    ):
        if extended_result[key] != mod.NA_VALUE:
            fail(f"expected {key}=NA, got {extended_result[key]!r}")

    if "backend" in compact_lines[0].split("\t"):
        fail("compact TimingResult unexpectedly includes extended-only columns")

    if list(mod.ALL_COLUMNS) != list(mod.EXTENDED_COLUMNS):
        fail("ALL_COLUMNS must remain identical to EXTENDED_COLUMNS")


if __name__ == "__main__":
    main()
