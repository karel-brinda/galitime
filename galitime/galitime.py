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


class TimingResult:

    def __init__(self, experiment=None, run=None, cmd=None):
        """Setup all the fields
        """
        self._data = collections.OrderedDict()

        # 1. prefill table with the mandatory fields in the right order
        mandatory_columns = (
            "experiment", "run", "real_s", "real_s_py", "user_s", "sys_s", "percent_cpu",
            "max_ram_kb", "fs_inputs", "fs_outputs", "exit_code", "command"
        )
        for x in mandatory_columns:
            self._data[x] = None

        # 2. insert experiment parameters
        self['experiment'] = experiment
        self['run'] = run
        self['command'] = cmd

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        assert key in self._data, f"The key '{key}' is not in the TimingResult dict after initialization, likely a bug (present keys: {self._data.keys()})"
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return "\t".join(map(str, self._data.keys())
                         ) + "\n" + "\t".join(map(str, self._data.values()))


class AbstractTime(ABC):

    def __init__(self, cmd, experiment=None):
        self.experiment = experiment
        self.cmd = cmd
        self.cmd_simpl = " ".join(cmd.replace("\\\n", " ").strip().split())
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.results = []  # all processed results
        self.current_i = 0
        self.current_result = None  # currrent result

    def __del__(self):
        self.tmp_dir.cleanup()

    # TODO: add possibility to set up multiple repetitions
    def run(self, times=1):
        """The main loop
        """
        for i in range(times):
            self.current_i += 1
            run = None if times == 1 else self.current_i
            self.current_result = TimingResult(
                experiment=self.experiment, run=run, cmd=self.cmd_simpl
            )
            self._execute_time()
            self._parse_result()
            self._save_result()

    def current_tmp_fn(self):
        return os.path.join(self.tmp_dir.name, f"timing_output.run_{self.current_i}.log")

    def _execute_time(self):
        """Execute time, whatever command it is
        """
        # TODO: change to /usr/bin/env bash
        wrapped_cmd = f'{self.wrapper()} {self.cmd}'
        print(f"Running '{wrapped_cmd}'")
        main_process = subprocess.Popen(wrapped_cmd, shell=True, executable='/bin/bash')

        #TODO: integrate timeout into the whole method
        timeout = None
        start_time = datetime.datetime.now()
        try:
            exit_code = main_process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            exit_code = -1  # timeout
        end_time = datetime.datetime.now()
        self.current_result["real_s_py"] = (end_time - start_time).total_seconds()
        self.current_result["exit_code"] = exit_code

        # TODO: different treating based on the expected behaviour
        if exit_code:
            raise subprocess.CalledProcessError(
                exit_code, main_process.args, output=main_process.stdout, stderr=main_process.stderr
            )

    @abstractmethod
    def _parse_result(self):
        pass

    def _save_result(self):
        self.results.append(self.current_result)
        self.current_result = None

    def __str__(self):
        lines = "\n".join([str(x) for x in self.results]).split("\n")
        seen = set()
        unique_list = []
        for x in lines:
            if x not in seen:
                seen.add(x)
                unique_list.append(x)
        return "\n".join(unique_list)


class GnuTime(AbstractTime):

    def __init__(self, cmd, experiment=None):
        super().__init__(cmd=cmd, experiment=experiment)
        if sys.platform == "linux":
            time_command = "/usr/bin/time"
        elif sys.platform == "darwin":
            # TODO: verify gtime is present
            time_command = "gtime"
        else:
            raise Exception("Unsupported OS")

        self.gtime_columns_spec = "%e\t%U\t%S\t%P\t%M\t%x\t%I\t%O"
        self.gtime_columns = (
            "real_s", "user_s", "sys_s", "percent_cpu", "max_ram_kb", "exit_code", "fs_inputs",
            "fs_outputs"
        )
        self.wrapper = lambda: f'{time_command} -o {self.current_tmp_fn()} -f "{self.gtime_columns_spec}"'

    def _parse_result(self):
        with open(self.current_tmp_fn()) as tmp_fo:
            gtime_output_values = tmp_fo.readline().strip().split("\t")
        for k, v in zip(self.gtime_columns, gtime_output_values):
            self.current_result[k] = v


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
    t = GnuTime(command, experiment)
    t.run()

    if log_file == "stdout":
        print(t)
    elif log_file == "stderr":
        print(t, file=sys.stderr)
    else:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "w") as fo:
            print(t, file=fo)


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
