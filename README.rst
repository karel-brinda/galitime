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

``galitime`` benchmarks shell commands and records timing and resource statistics in
a simple tab-delimited format. It wraps the system ``time`` command, normalizes the
output into stable column names, and can repeat commands for multiple runs.


Quick Example
-------------

Install from PyPI:

.. code-block:: bash

    if [[ $(uname) == "Darwin" ]]; then brew install gnu-time; fi
    pip install -U galitime

Benchmark a command and print the result to standard output:

.. code-block:: bash

    galitime --gtime -l stdout "sleep 0.1"

Write the benchmark output to a file:

.. code-block:: bash

    galitime --log time.log ls


Installation
------------

Requirements
~~~~~~~~~~~~

* Python 3.7 or newer
* A working ``time`` command on the host system

On macOS, you can optionally install GNU Time with Homebrew:

.. code-block:: bash

    brew install gnu-time

``galitime`` uses the default ``time`` command by default. If GNU Time is available,
run with ``--gtime`` to use it explicitly.


Using Bioconda
~~~~~~~~~~~~~~

.. code-block:: bash

    conda install -y -c bioconda -c conda-forge galitime


Using PyPI
~~~~~~~~~~

.. code-block:: bash

    pip install -U galitime


CLI
---

.. code-block:: text

    $ galitime -h

    Program: galitime (benchmarking of computational experiments using GNU time)
    Version: 0.2.0
    Contact: Karel Brinda <karel.brinda@inria.fr>

    usage: galitime [-r INT] [-g] [-l FILE] [-n STR] [-s STR] command

    positional arguments:
      command          the command to be benchmarked

    options:
      -h               show this help message and exit
      -v               show program's version number and exit
      -r, --reps INT   number of repetitions [1]
      -g, --gtime      call gtime instead of time (useful on MacOS)
      -l, --log FILE   output (filename/stderr/stdout) [stderr]
      -n, --name STR   name of the experiment (for output)
      -s, --shell STR  shell for execution [/bin/bash]


Output Columns
--------------

``galitime`` writes tab-delimited output with these columns:

* ``experiment``: experiment name supplied with ``-n/--name``; otherwise empty
* ``run``: repetition number when ``-r/--reps`` is greater than 1; otherwise empty
* ``real_s``: wall-clock time reported by ``time``, in seconds
* ``real_s_py``: wall-clock time measured by Python around the whole execution
* ``user_s``: user CPU time in seconds
* ``sys_s``: system CPU time in seconds
* ``percent_cpu``: CPU usage percentage reported by ``time``
* ``max_ram_kb``: maximum resident memory in kilobytes
* ``fs_inputs``: file system input operations
* ``fs_outputs``: file system output operations
* ``exit_code``: exit status of the benchmarked command
* ``command``: normalized command string that was executed


Development
-----------

Repository layout:

* ``galitime_pkg/``: package source and CLI entry point
* ``tests/``: Makefile-based smoke tests

Common local commands:

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

`MIT <https://github.com/karel-brinda/galitime/blob/master/LICENSE.txt>`_


Contact
-------

* `Karel Brinda <http://brinda.eu>`_ <karel.brinda@inria.fr>
