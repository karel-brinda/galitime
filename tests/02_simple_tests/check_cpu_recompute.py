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


def assert_equal(actual, expected, message):
    if actual != expected:
        fail(f"{message}: expected {expected!r}, got {actual!r}")


def main():
    mod = load_galitime_module()

    class DummyTime(mod.AbstractTime):
        def __init__(self):
            super().__init__(
                command="true",
                shell="/bin/sh",
                experiment="demo",
                time="dummy",
                extended=True,
                backend_name=mod.BACKEND_GNU,
            )
            self.wrapper = lambda: "true"

        def _parse_result(self):
            raise AssertionError("not used in this test")

    timing = DummyTime()
    timing.current_result = mod.TimingResult(
        experiment="demo",
        run=1,
        command="true",
        extended=True,
        backend=mod.BACKEND_GNU,
    )
    timing.current_result.set("real_s", "2.5")
    timing.current_result.set("user_s", "1.25")
    timing.current_result.set("sys_s", "0.75")
    timing.current_result.set("cpu_s", "999")
    timing.current_result.set("cpu_pct", "999")
    timing._set_cpu_time()
    timing._set_cpu_pct()

    assert_equal(timing.current_result["cpu_s"], 2.0, "cpu_s should be recomputed centrally")
    assert_equal(
        timing.current_result["cpu_pct"],
        80.0,
        "cpu_pct should be recomputed centrally from cpu_s / real_s",
    )

    timing.current_result.set("real_s", "0")
    timing._set_cpu_pct()
    assert_equal(
        timing.current_result["cpu_pct"],
        mod.NA_VALUE,
        "cpu_pct should become NA when real_s <= 0",
    )

    gnu = mod.GnuTime(
        command="true",
        shell="/bin/sh",
        experiment="demo",
        time="/usr/bin/env time",
        extended=True,
        backend_name=mod.BACKEND_GNU,
    )
    gnu.current_i = 1
    gnu.current_result = mod.TimingResult(
        experiment="demo",
        run=1,
        command="true",
        extended=True,
        backend=mod.BACKEND_GNU,
    )
    gnu.current_result.set("cpu_pct", "777")

    output_path = Path(gnu.current_tmp_fn())
    output_path.write_text("2.0\t1.0\t0.5\t9999%\t123\t4\t5\t6\t7\t8\n", encoding="utf-8")

    gnu._parse_result()

    assert_equal(
        gnu.current_result["cpu_pct"],
        "777",
        "GNU percent_cpu should be ignored during backend parsing",
    )

    gnu._set_cpu_time()
    gnu._set_cpu_pct()
    assert_equal(
        gnu.current_result["cpu_s"],
        1.5,
        "GNU backend cpu_s should still be recomputed from parsed user/sys values",
    )
    assert_equal(
        gnu.current_result["cpu_pct"],
        75.0,
        "GNU backend final cpu_pct should be recomputed from parsed real/user/sys values",
    )


if __name__ == "__main__":
    main()
