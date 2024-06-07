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

Software for benchmarking programs using the `GNU Time <https://www.gnu.org/software/time/>`_ command,
with extensive benchmarking options and unified behaviour across platforms (including output units).
Inspired by the benchmarking script in `Phylign <https://github.com/karel-brinda/phylign>`_
developed by `Leandro Lima <https://github.com/leoisl>`_.



Quick example
-------------

.. code-block:: bash

    $ if [[ $(uname) == "Darwin" ]]; then brew install gnu-time; fi
    $ conda install -y -c bioconda -c conda-forge galitime

    $ galitime --log time.log ls

    $ cat time.log
    real_s  user_s  sys_s   percent_cpu max_ram_kb  exit_code   fs_inputs   fs_outputs  real_s_alt  command
    0.03    0.00    0.00    10% 2904    0   0   0   0.076661    ls



Installation
------------

Dependencies
~~~~~~~~~~~~

Galitime has no dependencies beyond Python 3. However, on OS X
it requires the GNU version of the :code:`time` command (:code:`gtime`),
which can be installed by :code:`brew install gnu-time`.


Using Bioconda
~~~~~~~~~~~~~~

.. code-block:: bash

    conda install -y -c bioconda -c conda-forge galitime


Using PyPI
~~~~~~~~~~

Install the Galitime Python package:

.. code-block:: bash

    pip install -U galitime



Command-line parameters
-----------------------


.. code-block::

    $ galitime -h
    usage: galitime [-h] --log LOG [--experiment EXPERIMENT] [-v] command

    Benchmark a command.

    positional arguments:
      command               The command to be benchmarked

    options:
      -h, --help            show this help message and exit
      --log LOG             Path to the log file with benchmark statistics (if the directory doesn't exist, it will be created).
      --experiment EXPERIMENT
                            Name of the experiment (to be attached to the output)
      -v                    show program's version number and exit


Output
------

* ``experiment`` - Name of the experiment, if provided via ``-n``
* ``run`` - Number of run in case of multiple repetitions
* ``real_s`` - Real time in seconds (wall clock time)
* ``real_s_py`` - Python-measured real time in seconds (slightly higher than ``real_s``)
* ``user_s`` - User CPU time in seconds (user mode, excluding system calls)
* ``sys_s`` - System CPU time in seconds (kernel mode)
* ``percent_cpu`` - CPU usage percentage
* ``max_ram_kb`` - Maximum RAM usage in kilobytes
* ``exit_code`` - Exit code of the command (0 if everything ok, -1 if command failed)
* ``fs_inputs`` - File system read read operations count
* ``fs_outputs`` - File system write operations count
* ``command`` - Command executed, with tabs replaced by spaces





Issues
------

Please use `Github issues <https://github.com/karel-brinda/galitime/issues>`_.


Changelog
---------

See `Releases <https://github.com/karel-brinda/galitime/releases>`_.


Licence
-------

`MIT <https://github.com/karel-brinda/galitime/blob/master/LICENSE.txt>`_


Contact
-------

* `Karel Brinda <http://brinda.eu>`_ <karel.brinda@inria.fr>
