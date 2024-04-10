#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
import subprocess
import datetime
import os

sys.path.append(os.path.dirname(__file__))
import version

PROGRAM = 'galitime'
VERSION = version.VERSION
DESC = 'benchmarking of computational experiments'


def get_time_command():
    if sys.platform == "linux":
        time_command = "/usr/bin/time"
    elif sys.platform == "darwin":
        time_command = "gtime"
    else:
        raise Exception("Unsupported OS")
    return time_command


def run(log_file, experiment, command):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_log_file = Path(f"{log_file}.tmp")

    with open(log_file, "w") as log_fh:
        formatted_command = " ".join(command.replace("\\\n", " ").strip().split())
        print(f"# Benchmarking command: {formatted_command}", file=log_fh)
        header = [
            "real(s)", "sys(s)", "user(s)", "percent_CPU", "max_RAM(kb)", "FS_inputs", "FS_outputs",
            "elapsed_time_alt(s)"
        ]
        if experiment:
            header = ['experiment'] + header
        print("\t".join(header), file=log_fh)

    time_command = get_time_command()
    benchmark_command = f'{time_command} -o {tmp_log_file} -f "%e\t%S\t%U\t%P\t%M\t%I\t%O"'

    start_time = datetime.datetime.now()
    main_process = subprocess.Popen(f'{benchmark_command} {command}', shell=True, executable='/bin/bash')
    return_code = main_process.wait()
    if return_code:
        raise subprocess.CalledProcessError(
            return_code, main_process.args, output=main_process.stdout, stderr=main_process.stderr
        )

    end_time = datetime.datetime.now()
    elapsed_seconds = (end_time - start_time).total_seconds()
    with open(tmp_log_file) as log_fh_tmp, open(log_file, "a") as log_fh:
        log_line = ""
        if experiment:
            log_line = experiment.replace("\t", " ").strip() + "\t"
        log_line += log_fh_tmp.readline().strip()
        log_line += f"\t{elapsed_seconds}"

        print(log_line, file=log_fh)

    tmp_log_file.unlink()


def main():
    parser = argparse.ArgumentParser(description='Benchmark a command.')
    parser.add_argument('command', help='The command to be benchmarked')
    parser.add_argument(
        '--log', required=True,
        help='Path to the log file with benchmark statistics (if the directory doesn\'t exist, it will be created).'
    )
    parser.add_argument('--experiment', help='Name of the experiment (to be attached to the output)')
    parser.add_argument(
        '-v',
        action='version',
        version='{} {}'.format(PROGRAM, VERSION),
    )

    args = parser.parse_args()
    run(log_file=Path(args.log), experiment=args.experiment, command=args.command)


if __name__ == "__main__":
    main()
