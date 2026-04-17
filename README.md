# galitime

[![Project Info](https://img.shields.io/badge/Project-Info-blue)](https://github.com/karel-brinda/galitime)
[![GitHub release](https://img.shields.io/github/release/karel-brinda/galitime.svg)](https://github.com/karel-brinda/galitime/releases/)
[![PyPI](https://img.shields.io/pypi/v/galitime.svg)](https://pypi.org/project/galitime/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10953105.svg)](https://doi.org/10.5281/zenodo.10953105)
[![CI tests](https://github.com/karel-brinda/galitime/actions/workflows/ci.yml/badge.svg)](https://github.com/karel-brinda/galitime/actions/)

## Introduction

`galitime` benchmarks commands and records timing and resource statistics
in a simple tab-delimited format.
It wraps the system `time` command, normalizes the output into stable column
names, and can repeat commands across multiple runs.
This is particularly helpful for benchmarking research tools and workflows
that need to be tested and evaluated on different platforms.

The tool is inspired by the benchmarking script in [Phylign](https://github.com/karel-brinda/phylign),
originally developed by [Leandro Lima](https://github.com/leoisl).

## Quick example

Install from PyPI:

```bash
pip install -U galitime
```

Benchmark a command and print the result to standard output:

```bash
galitime -l stdout sleep 0.1
```

Benchmark a raw shell command string when you need shell syntax:

```bash
galitime -l stdout "echo a && echo b"
```

Write the benchmark output to a file:

```bash
galitime --log time.log "ls"
```

Write per-run logs and a separate summary TSV in one invocation:

```bash
galitime -r 5 --log runs.tsv --stats stats.tsv "sleep 0.1"
```

Use GNU Time explicitly:

```bash
galitime --gtime -l stdout "sleep 0.1"
```

## Installation

### Requirements

* Python 3.7 or newer
* A working `time` command on the host system

On macOS, you can optionally install GNU Time with Homebrew:

```bash
brew install gnu-time
```

`galitime` uses the default `time` command by default. If GNU Time is
available, run with `--gtime` to use it explicitly.

### Using Bioconda

```bash
conda install -y -c bioconda -c conda-forge galitime
```

### Using PyPI

```bash
pip install -U galitime
```

## Standalone usage

The top-level `galitime` file is the canonical standalone executable.

```bash
chmod +x ./galitime
./galitime -l stdout sleep 0.1
```

This is useful when copying a single executable into another repository,
container image, or remote environment.

## CLI

```text
Program: galitime (benchmarking of computational experiments using GNU time)
Version: 0.4.0
Contact: Karel Brinda <karel.brinda@inria.fr>

usage: galitime [-d] [-r INT] [-g] [-l FILE] [-S FILE] [-n STR] [-s STR] [--] command [arg ...]

command modes:
  argv-like mode:      galitime sleep 0.1
  shell-command mode:  galitime "echo a && echo b"

notes:
  - use quotes when your command includes shell syntax such as: redirection ('>'),
    pipelines ('|'), '&&', ';', globbing, or command substitution
  - use -- to explicitely mark the start of the benchmarked command when needed
  - argv-like mode is only guaranteed for POSIX-like shells

positional arguments:
  command          the command to be benchmarked

options:
  -h               show this help message and exit
  -v               show program's version number and exit
  -d, --debug      print detailed debug trace to stderr
  -r, --reps INT   number of repetitions [1]
  -g, --gtime      call gtime instead of time (useful on MacOS)
  -l, --log FILE   output (filename/stderr/stdout) [stderr]
  -S, --stats FILE write summary statistics TSV to FILE [disabled]
  -n, --name STR   name of the experiment (for output)
  -s, --shell STR  shell for execution [/bin/bash]
```

## Command Modes

`galitime` accepts commands in two explicit forms:

* argv-like convenience mode for ordinary POSIX-like argv tails:

  ```bash
  galitime sleep 0.1
  ```

* raw shell-command mode for shell expressions and shell syntax:

  ```bash
  galitime "echo a && echo b"
  ```

Quotes are still required for shell syntax such as redirection, pipelines,
`&&`, `;`, globbing, and command substitution.

`--` the recommended escape hatch whenever there is any ambiguity,
especially when the benchmarked command or one of its arguments begins with
`-`:

```bash
galitime -- sleep 0.1
```

The argv-like convenience mode is supported for POSIX-like shells. If you set
`--shell` to a non-POSIX shell, that reconstruction path is not guaranteed.

## Output columns

`galitime` writes tab-delimited output with these columns:

1. `experiment` – experiment name supplied with `-n/--name`; otherwise `NA`
2. `run` – 1-based repetition number
3. `real_s` – wall-clock time reported by `time`, in seconds
4. `user_s` – user CPU time in seconds
5. `sys_s` – system CPU time in seconds
6. `cpu_s` – total CPU time in seconds (`user_s + sys_s`)
7. `cpu_pct` – Average CPU utilization percentage, computed as `100 * (user_s + sys_s) / real_s`.
   Values above 100 indicate parallel CPU use.
8. `max_ram_kb` – maximum resident memory in decimal kilobytes (`1 KB = 1000 bytes`)
9. `status` – run outcome: `ok`, `failed`, `timeout`, or `timing_error`
10. `exit_code` – exit status of the benchmarked command; `NA` when unavailable
11. `command` – command string: the raw single-string shell command, or the argv-like tail reconstructed with `shlex.join(...)`

## Stats file

Use `-S/--stats` to write a separate TSV file with one summary row per
`galitime` invocation.

Numeric summaries are computed only from runs where `status=ok`. Count
columns reflect all completed runs, including failures, timeouts, and timing
errors. The `stddev` columns use sample standard deviation and are `NA`
when fewer than 2 runs were summarized.

# Comparison

Legend: ✅ yes; ❌ no; ⚠️ partial, indirect, platform-dependent, or tool-dependent.

| Feature | Galitime | `time` | Snakemake `benchmark` | Hyperfine | Profilers |
|---|---|---|---|---|---|
| Repeated runs | ✅ | ❌ | ✅ | ✅ | ⚠️ manual |
| Structured output | ✅ TSV | ⚠️ limited/custom | ✅ TSV/JSONL | ✅ | ⚠️ tool-specific |
| Normalized columns | ✅ | ❌ | ✅ | ✅ | ❌ |
| Same output schema across machines | ✅ | ⚠️ if pinned GNU `time`; otherwise ❌ | ✅ | ✅ | ❌ |
| CPU metrics | ✅ | ✅ | ⚠️ platform/version-dependent | ❌ | ⚠️ tool-dependent |
| Peak memory/RSS | ✅ | ⚠️ | ⚠️ platform/version-dependent | ❌ | ⚠️ profiling-specific |
| I/O statistics | ✅ | ⚠️ | ⚠️ platform/version-dependent | ❌ | ⚠️ limited/specific |
| Command labels | ✅ | ❌ | ⚠️ via rule/extended metadata | ✅ | ⚠️ |
| Custom shell | ✅ | ⚠️ manual wrapper | ✅ | ✅ | ⚠️ manual wrapper |
| Statistical summaries | ✅ separate TSV | ❌ | ❌ | ✅ | ❌ |

## Development

### Repository layout

* `galitime` – canonical standalone executable and main source file
* `galitime_pkg/` – packaging shim for the Python package / console entry point
* `tests/` – smoke tests and release checks

### Common local commands

```bash
python -m pip install .
python -m build
make test
```

## Issues

Please use [GitHub issues](https://github.com/karel-brinda/galitime/issues).

## Changelog

See [Releases](https://github.com/karel-brinda/galitime/releases).

## License

[MIT](https://github.com/karel-brinda/galitime/blob/main/LICENSE.txt)

## Contact

* [Karel Brinda](http://brinda.eu) <karel.brinda@inria.fr>
