###########
pyBabyMaker
###########

.. image:: https://travis-ci.com/umd-lhcb/pyBabyMaker.svg?build
:target: https://travis-ci.com/umd-lhcb/pyBabyMaker
:alt: Travis CI build status
.. image:: https://codecov.io/gh/umd-lhcb/pyBabyMaker/branch/master/graph/badge.svg
:target: https://codecov.io/gh/umd-lhcb/pyBabyMaker
:alt: Codecov status
.. image:: https://readthedocs.org/projects/pybabymaker/badge/?version=latest
:target: https://pybabymaker.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status

Python babymaker (flat ntuple generation tool) library. `babymaker`_ was
originally conceived by Manuel Franco Sevilla and his colleagues at UCSB. It
was later rewritten by Yipeng Sun to make it simpler, and more portable. The
result is this project: `pyBabyMaker`.

The ``pyBabyMaker`` library provides the following tools to aid ntuple
processing:

- ``ntpdump``: Dump ntuple tree structure.
- ``babymaker``: Generate ``C++`` code to process ntuples.


.. _babymaker: https://github.com/manuelfs/babymaker


************
Installation
************

Please make sure ``ROOT``, ``gcc``, ``python3``, and ``pip`` are installed.
Make sure that ``root-config`` is available in your ``$PATH``, and ``gcc``
supports ``-std=c++14``.

``clang-format`` will automatically be used to format generated ``C++`` code,
if it is available in your ``$PATH``.

Currently, ``pyBabyMaker`` is not on ``PyPI``. To install:
.. code-block:: console
   # pip install git+https://github.com/umd-lhcb/pyBabyMaker
   $ pip install --user git+https://github.com/umd-lhcb/pyBabyMaker
