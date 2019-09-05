``babymaker``
-------------

This script generates a C++ file that can be compiled to postprocess n-tuples.

Usage
^^^^^

.. code-block:: console

   babymaker -i <yaml_file> -d <ntuple_file> -o <output_cpp>

Note that:

* ``<yaml_file>`` contains the instruction for postprocessing.
* ``<ntuple_file>`` should have the exact tree structure as the n-tuples to be
  processed.

By default, ``babymaker`` tries to reformat the generated C++ file with
``clang-format``, if it's available in user's ``$PATH``. This can be disabled
by providing the ``--no-format`` flag.
