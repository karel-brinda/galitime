#!/usr/bin/env python3

import argparse
import collections
import datetime
import os
import re
import subprocess
import sys
import tempfile

from abc import ABC, abstractmethod

from pathlib import Path

PROGRAM = 'galitime'
DESC = 'benchmarking of computational experiments using GNU time'

try:
    sys.path.append(os.path.dirname(__file__))
    import version
    VERSION = version.VERSION
except ImportError:
    VERSION = "(version NA)"

DEFAULT_L = "stderr"


class TimingResults:

    def __init__(self, experiment=None):
        se
        if experiment:
            d['experiment'] = experiment

    def get_header(self):
        return (x for x in self.results)

    def get_values(self):
        return (self.results[x] for x in self.results)

    def get_values_str(self):
        return (str(x) for x in self.get_values())


class TimeCommand(ABC):

    def __init__(self, cmd, experiment=None):
        if experiment:
            d['experiment'] = experiment
        with tempfile.TemporaryDirectory() as dir_fn:
            self.tmp_fn = os.path.join(dir_fn, "gtime_output.txt")

    def run(self, times=1):
        for i in range(times):
            self._execute_time(run=i)
            self._parse_results()
            self._save_results()

    def _execute_time(self, run):
        start_time = datetime.datetime.now()
        main_process = subprocess.Popen(
            f'{benchmark_wrapper} {command}', shell=True, executable='/bin/bash'
        )
        return_code = main_process.wait()
        end_time = datetime.datetime.now()
        if return_code:
            raise subprocess.CalledProcessError(
                return_code, main_process.args, output=main_process.stdout,
                stderr=main_process.stderr
            )

    @abstractmethod
    def _parse_results(self):
        pass

    def _save_results(self):
        pass

    @abstractmethod
    def parse_output(self):
        # 3) elapsed time
        d["real_s_alt"] = str((end_time - start_time).total_seconds())

        # 4) formatted command
        d["command"] = " ".join(command.replace("\\\n", " ").strip().split())


class GnuTime:

    def __init__(self):
        if sys.platform == "linux":
            time_command = "/usr/bin/time"
        elif sys.platform == "darwin":
            time_command = "gtime"
        else:
            raise Exception("Unsupported OS")
        gtime_columns = (
            "real_s", "user_s", "sys_s", "percent_cpu", "max_ram_kb", "exit_code", "fs_inputs",
            "fs_outputs"
        )
        gtime_columns_spec = "%e\t%U\t%S\t%P\t%M\t%x\t%I\t%O"
        self.wrapper = f'{time_command} -o {self.tmp_fn} -f "{gtime_columns_spec}"'

    def parse_output(self):
        with open(tmp_fn) as tmp_fo:
            gtime_output_values = tmp_fo.readline().strip().split("\t")
        for k, v in zip(gtime_columns, gtime_output_values):
            d[k] = v


class MacTime:
    pass


def run(log_file, command, experiment):
    """
    Run a benchmarking command and log the results.

    Args:
        log_file (str): The path to the log file where the results will be logged.
        experiment (str): Optional experiment name to include in the log.
        command (str): The benchmarking command to run.

    Raises:
        subprocess.CalledProcessError: If the benchmarking command returns a non-zero exit code.

    Returns:
        None
    """
    d = run_single_instance(command, experiment)

    output = "\t".join(d.keys()) + "\n" + "\t".join(d.values())

    if log_file == "stdout":
        print(output)
    elif log_file == "stderr":
        print(output, file=sys.stderr)
    else:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w") as fo:
            print(output, file=fo)


def main():
    """
    The main function of the script. It parses the command line arguments, runs the benchmarking command,
    and logs the results.

    Raises:
        subprocess.CalledProcessError: If the benchmarking command returns a non-zero exit code.
    """

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

    parser.add_argument('command', help='the command to be benchmarked')

    parser.add_argument(
        '-v',
        action='version',
        version='{} {}'.format(PROGRAM, VERSION),
    )

    parser.add_argument(
        '-l', '--log', dest='log', metavar='FILE', default=DEFAULT_L,
        help=f'output benchmarking file (or stderr/stdout) [{DEFAULT_L}]'
    )

    parser.add_argument(
        '-n', '--name', metavar='STR', help='name of the experiment', dest='experiment',
        default=None
    )

    args = parser.parse_args()
    run(log_file=args.log, experiment=args.experiment, command=args.command)


if __name__ == "__main__":
    main()
