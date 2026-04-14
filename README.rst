galitime
========

.. |info-badge| image:: https://img.shields.io/badge/Project-Info-blue
   :target: https://github.com/karel-brinda/galitime

.. |github-release-badge| image:: https://img.shields.io/github/release/karel-brinda/galitime.svg
   :target: https://github.com/karel-brinda/galitime/releases/

.. |pypi-badge| image:: https://img.shields.io/pypi/v/galitime.svg
   :target: https://pypi.org/project/galitime/

.. |zenodo-badge| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.10953105.svg
   :target: https://doi.org/10.5281/zenodo.10953105

.. |ci-tests-badge| image:: https://github.com/karel-brinda/galitime/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/karel-brinda/galitime/actions/

|info-badge| |github-release-badge| |pypi-badge| |zenodo-badge| |ci-tests-badge|

Introduction
------------

``galitime`` benchmarks commands and records timing and resource statistics
in a simple tab-delimited format.
It wraps the system ``time`` command, normalizes the output into stable column
names, and can repeat commands across multiple runs.
This is particularly helpful for benchmarking research tools and workflows
that need to be tested and evaluated on different platforms.

The tool is inspired by the benchmarking script in `Phylign <https://github.com/karel-brinda/phylign>`_,
originally developed by `Leandro Lima <https://github.com/leoisl>`_.

Quick example
-------------

Install from PyPI:

.. code-block:: bash

    pip install -U galitime

Benchmark a command and print the result to standard output:

.. code-block:: bash

    galitime -l stdout "sleep 0.1"

Write the benchmark output to a file:

.. code-block:: bash

    galitime --log time.log "ls"

Use GNU Time explicitly:

.. code-block:: bash

    galitime --gtime -l stdout "sleep 0.1"

Installation
------------

Requirements
~~~~~~~~~~~~

* Python 3.7 or newer
* A working ``time`` command on the host system

On macOS, you can optionally install GNU Time with Homebrew:

.. code-block:: bash

    brew install gnu-time

``galitime`` uses the default ``time`` command by default. If GNU Time is
available, run with ``--gtime`` to use it explicitly.

Using Bioconda
~~~~~~~~~~~~~~

.. code-block:: bash

    conda install -y -c bioconda -c conda-forge galitime

Using PyPI
~~~~~~~~~~

.. code-block:: bash

    pip install -U galitime

Standalone usage
----------------

The top-level ``galitime`` file is the canonical standalone executable.

.. code-block:: bash

    chmod +x ./galitime
    ./galitime -l stdout "sleep 0.1"

This is useful when copying a single executable into another repository,
container image, or remote environment.

CLI
---

.. code-block:: text

     
    Program: galitime (benchmarking of computational experiments using GNU time)
    Version: 0.3.0
    Contact: Karel Brinda <karel.brinda@inria.fr>

    usage: galitime [-r INT] [-g] [-l FILE] [-n STR] [-s STR] command

    positional arguments:
      command              the command to be benchmarked

    optional arguments:
      -h                   show this help message and exit
      -v                   show program's version number and exit
      -r INT, --reps INT   number of repetitions [1]
      -g, --gtime          call gtime instead of time (useful on MacOS)
      -l FILE, --log FILE  output (filename/stderr/stdout) [stderr]
      -n STR, --name STR   name of the experiment (for output)
      -s STR, --shell STR  shell for execution [/bin/bash]

Output columns
--------------

``galitime`` writes tab-delimited output with these columns:

1. ``experiment`` – experiment name supplied with ``-n/--name``; otherwise empty
2. ``run`` – repetition number when ``-r/--reps`` is greater than 1; otherwise empty
3. ``real_s`` – wall-clock time reported by ``time``, in seconds
4. ``real_s_py`` – wall-clock time measured by Python around the whole execution
5. ``user_s`` – user CPU time in seconds
6. ``sys_s`` – system CPU time in seconds
7. ``percent_cpu`` – CPU usage percentage reported by ``time``
8. ``max_ram_kb`` – maximum resident memory in kilobytes
9. ``fs_inputs`` – file system input operations
10. ``fs_outputs`` – file system output operations
11. ``exit_code`` – exit status of the benchmarked command
12. ``command`` – normalized command string that was executed

Development
-----------

Repository layout
~~~~~~~~~~~~~~~~~

* ``galitime`` – canonical standalone executable and main source file
* ``galitime_pkg/`` – packaging shim for the Python package / console entry point
* ``tests/`` – smoke tests and release checks

Common local commands
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python -m pip install .
    python -m build
    make test

Issues
------

Please use `GitHub issues <https://github.com/karel-brinda/galitime/issues>`_.

Changelog
---------

See `Releases <https://github.com/karel-brinda/galitime/releases>`_.

License
-------

`MIT <https://github.com/karel-brinda/galitime/blob/main/LICENSE.txt>`_

Contact
-------

* `Karel Brinda <http://brinda.eu>`_ <karel.brinda@inria.fr>
