#!/usr/bin/env python3

import importlib.util
import sys
from importlib.machinery import SourceFileLoader
from pathlib import Path


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

    expected_prefix = (
        "experiment",
        "runs_requested",
        "runs_completed",
        "runs_summarized",
        "runs_ok",
        "runs_failed",
        "runs_timeout",
        "runs_timing_error",
        "final_status",
        "final_exit_code",
    )
    expected_suffix = ("command",)
    expected_aggs = ("mean", "stddev", "min", "median", "max")
    expected_base_metrics = (
        "real_s",
        "user_s",
        "sys_s",
        "cpu_s",
        "cpu_pct",
        "max_ram_kb",
    )
    expected_extended_metrics = expected_base_metrics + (
        "fs_inputs",
        "fs_outputs",
        "major_page_faults",
        "minor_page_faults",
        "swaps",
    )

    if mod.STATS_PREFIX_COLUMNS != expected_prefix:
        fail(f"unexpected STATS_PREFIX_COLUMNS: {mod.STATS_PREFIX_COLUMNS!r}")

    if mod.STATS_SUFFIX_COLUMNS != expected_suffix:
        fail(f"unexpected STATS_SUFFIX_COLUMNS: {mod.STATS_SUFFIX_COLUMNS!r}")

    if mod.STATS_AGGS != expected_aggs:
        fail(f"unexpected STATS_AGGS: {mod.STATS_AGGS!r}")

    if mod.BASE_STATS_NUMERIC_METRICS != expected_base_metrics:
        fail(f"unexpected BASE_STATS_NUMERIC_METRICS: {mod.BASE_STATS_NUMERIC_METRICS!r}")

    if mod.EXTENDED_STATS_NUMERIC_METRICS != expected_extended_metrics:
        fail(
            f"unexpected EXTENDED_STATS_NUMERIC_METRICS: "
            f"{mod.EXTENDED_STATS_NUMERIC_METRICS!r}"
        )

    def expected_columns(metrics):
        columns = list(expected_prefix)
        for metric in metrics:
            for agg in expected_aggs:
                columns.append(f"{metric}_{agg}")
        columns.extend(expected_suffix)
        return tuple(columns)

    expected_base = expected_columns(expected_base_metrics)
    expected_extended = expected_columns(expected_extended_metrics)

    if expected_base != mod.BASE_STATS_COLUMNS:
        fail(
            f"BASE_STATS_COLUMNS does not match the expected compact stats schema: "
            f"{mod.BASE_STATS_COLUMNS!r}"
        )

    if expected_extended != mod.EXTENDED_STATS_COLUMNS:
        fail("EXTENDED_STATS_COLUMNS does not match the expected extended stats schema")

    if mod.make_stats_columns(expected_base_metrics) != expected_base:
        fail("make_stats_columns(BASE_STATS_NUMERIC_METRICS) produced the wrong compact tuple")

    if mod.make_stats_columns(expected_extended_metrics) != expected_extended:
        fail(
            "make_stats_columns(EXTENDED_STATS_NUMERIC_METRICS) produced the wrong extended tuple"
        )

    if hasattr(mod, "STATS_COLUMNS"):
        fail("legacy STATS_COLUMNS alias should not remain")

    if hasattr(mod, "STATS_NUMERIC_METRICS"):
        fail("legacy STATS_NUMERIC_METRICS alias should not remain")


if __name__ == "__main__":
    main()
