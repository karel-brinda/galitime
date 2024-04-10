galitime
========

.. |info-badge| image:: https://img.shields.io/badge/Project-Info-blue
    :target: https://github.com/karel-brinda/galitime
.. |github-release-badge| image:: https://img.shields.io/github/release/karel-brinda/galitime.svg
    :target: https://github.com/karel-brinda/galitime/releases/
.. |pypi-badge| image:: https://img.shields.io/pypi/v/galitime.svg
    :target: https://pypi.org/project/galitime/
.. |doi-badge| image:: https://zenodo.org/badge/DOI/110.5281/zenodo.10945896.svg
    :target: https://doi.org/10.5281/zenodo.10945896
.. |ci-tests-badge| image:: https://github.com/karel-brinda/galitime/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/karel-brinda/galitime/actions/

|info-badge| |github-release-badge| |pypi-badge| |doi-badge| |ci-tests-badge|


Introduction
------------

Software for benchmarking programs using [GNU Time](https://www.gnu.org/software/time/).


Installation
------------

Using Bioconda
~~~~~~~~~~~~~~

.. code-block:: bash

    conda install -y -c bioconda -c conda-forge galitime


Using PyPI
~~~~~~~~~~

First, install the following dependencies:

* `Mash <https://github.com/marbl/Mash>`_
* `QuickTree <https://github.com/khowe/quicktree>`_


Then install the Galitime Python package:

.. code-block:: bash

    pip install -U galitime


Quick example
-------------

.. code-block:: bash

    conda install galitime
    galitime ls


Command-line parameters
-----------------------


.. code-block::

    $ galitime -h
    
    usage: galitime [-h] --log LOG [--experiment EXPERIMENT] command

    Benchmark a command.

    positional arguments:
      command               The command to be benchmarked

    options:
      -h, --help            show this help message and exit
      --log LOG             Path to the log file with benchmark statistics (if the directory doesn't exist, it will be created).
      --experiment EXPERIMENT
                            Name of the experiment (to be attached to the output)
    

Issues
------

Please use `Github issues <https://github.com/karel-brinda/galitime/issues>`_.


Changelog
---------

See `Releases <https://github.com/karel-brinda/galitime/releases>`_.


Licence
-------

`MIT <https://github.com/karel-brinda/galitime/blob/master/LICENSE.txt>`_


Authors
-------

* `Karel Brinda <http://brinda.eu>`_ <karel.brinda@inria.fr>
* `Leandro Lima <https://github.com/leoisl>`_
