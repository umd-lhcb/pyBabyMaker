``ntpdump``
-----------

This script dumps the ntuple tree structure to a YAML file.

Usage
^^^^^

By default, ``ntpdump`` will output tree structure of a ntuple to ``stdout``:

.. code-block:: console

   ntpdump <ntuple_file>

If you want to save the output to a file, you can optionally specify the
``<output_yaml_file>``:

.. code-block:: console

   ntpdump <ntuple_file> <output_yaml_file>
