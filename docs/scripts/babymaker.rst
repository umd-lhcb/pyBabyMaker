``babymaker``
-------------

This script generates a C++ file that can be compiled to postprocess ntuples.

Usage
^^^^^

.. code-block:: console

   babymaker -i <yaml_file> -n <main_ntuple> -f [<friend_ntuple1> ...] -o <output_cpp> -t <template_file> -V "<var:name>"

Note that:

* ``<yaml_file>`` contains the instruction for postprocessing.
* ``<main_file>`` main ntuples to be processed.
* ``<friend_ntuple1>`` friend ntuples get their trees add as friends to the
  main if the tree names are the same
* ``<template_file>`` refers to the input C++ template with embedded template
  macros.
* ``<var:name>`` additional literal variables

By default, ``babymaker`` tries to reformat the generated C++ file with
``clang-format``, if it's available in user's ``$PATH``. This can be disabled
by providing the ``--no-format`` flag.


Compile Generated ``.cpp``
^^^^^^^^^^^^^^^^^^^^^^^^^^

To compile generated ``.cpp`` files, create a ``gen`` folder in project root,
then copy the file, say ``test.cpp`` to ``gen``. After that, type in:

.. code-block:: console

    make gen/test

Now the executable ``test`` will be compiled and placed inside ``gen``.

To learn more about the compilation rules, please take a look at `samples/sample.mk`_.

.. _samples/sample.mk: https://github.com/umd-lhcb/pyBabyMaker/blob/master/samples/sample.mk

The rules defined in the file above can be copied to your project's
``Makefile`` for ``pyBabyMaker`` integration.
