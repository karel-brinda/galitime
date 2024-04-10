#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
import subprocess
import datetime
import os
import re

sys.path.append(os.path.dirname(__file__))
import version

PROGRAM = 'galitime'
VERSION = version.VERSION
DESC = 'benchmarking of computational experiments using GNU time'


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
    main_process = subprocess.Popen(
        f'{benchmark_command} {command}', shell=True, executable='/bin/bash'
    )
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

    class CustomArgumentParser(argparse.ArgumentParser):

        def __init__(self, prog=None, **kwargs):
            super().__init__(prog="galitime", **kwargs)

        def print_help(self):
            """
            Prints the help message.

            Returns:
                None
            """
            msg = self.format_help()
            repl = re.compile(r'\]\s+\[')
            msg = repl.sub("] [", msg)
            msg = msg.replace(" [-h] [-v]", "")
            msg = msg.replace(", --help", "        ")
            print(msg)

        def format_help(self):
            formatter = self._get_formatter()
            formatter.add_text(" \n" + self.description)
            formatter.add_usage(self.usage, self._actions, self._mutually_exclusive_groups)
            formatter.add_text(self.epilog)

            # positionals, optionals and user-defined groups
            for action_group in self._action_groups:
                formatter.start_section(action_group.title)
                formatter.add_text(action_group.description)
                formatter.add_arguments(action_group._group_actions)
                formatter.end_section()

            return formatter.format_help()

    parser = CustomArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Program: {} ({})\n".format(PROGRAM, DESC) + "Version: {}\n".format(VERSION) +
        "Contact: Karel Brinda <karel.brinda@inria.fr>",
    )

    parser.add_argument('command', help='The command to be benchmarked')

    parser.add_argument(
        '-v',
        action='version',
        version='{} {}'.format(PROGRAM, VERSION),
    )

    parser.add_argument(
        '-l', '--log', required=True, dest='log', metavar='FILE', help='output benchmarking file'
    )

    parser.add_argument(
        '-n', '--name', metavar='STR', help='name of the experiment', dest='experiment',
        default=None
    )

    args = parser.parse_args()
    run(log_file=Path(args.log), experiment=args.experiment, command=args.command)


if __name__ == "__main__":
    main()
