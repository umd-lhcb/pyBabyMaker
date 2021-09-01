``babymaker``
-------------

This script generates a markdown file that represents operations defined in the
input YAML with given ntuples.

Usage
^^^^^

This is very similar to that of the ``babymaker``

.. code-block:: console

   babymaker -i <yaml_file> -n <main_ntuple> -f [<friend_ntuple1> ...] -o <output_markdown> -t <template_file> -V "<var:name>"

Note that:

* ``<yaml_file>`` contains the instruction for postprocessing.
* ``<main_file>`` main ntuples to be processed.
* ``<friend_ntuple1>`` friend ntuples get their trees add as friends to the
  main if the tree names are the same
* ``<var:name>`` additional literal variables

Output sample
^^^^^^^^^^^^^

In the root of this project, type in:

.. code-block:: console

	debugmaker -i samples/sample-babymaker.yml -o test.md \
		-n ./samples/sample.root -f ./samples/sample_friend.root \
		--debug \
		-V "pi:3.14" -B "TupleB0WSPi/DecayTree"

You'll get the following input:

.. code-block::

    # ATuple, from TupleB0/DecayTree

    ## Selection-related

    ### Cuts
     - true
     - raw_Y_ISOLATION_BDT > 0
     - raw_Y_PT > 10000

    ### Pre-cut variables

    ### Post-cut variables
     - double keep_Y_PT = raw_Y_PT
     - double keep_Y_PE = raw_Y_PE
     - double keep_Y_PX = raw_Y_PX
     - double keep_Y_PY = raw_Y_PY
     - double keep_Y_PZ = raw_Y_PZ
     - UInt_t keep_runNumber = raw_runNumber
     - ULong64_t keep_eventNumber = raw_eventNumber
     - ULong64_t keep_GpsTime = raw_GpsTime
     - double keep_random_pt = raw_random_pt
     - double rename_y_pt = raw_Y_PT
     - double rename_y_px = raw_Y_PX
     - double rename_y_py = raw_Y_PY
     - double rename_y_pz = raw_Y_PZ
     - double calculation_TempStuff = raw_D0_P+raw_Y_PT
     - double calculation_RandStuff = calculation_TempStuff*3.14
     - double calculation_some_var = rename_y_pt + rename_y_pz
     - double calculation_some_other_var = calculation_some_var*3.14
     - double calculation_alt_def = raw_Y_PE

    ## Input, output and temp variables

    ### Input variables
     - double raw_Y_ISOLATION_BDT = Y_ISOLATION_BDT
     - double raw_Y_PT = Y_PT
     - double raw_Y_PE = Y_PE
     - double raw_Y_PX = Y_PX
     - double raw_Y_PY = Y_PY
     - double raw_Y_PZ = Y_PZ
     - UInt_t raw_runNumber = runNumber
     - ULong64_t raw_eventNumber = eventNumber
     - ULong64_t raw_GpsTime = GpsTime
     - double raw_random_pt = random_pt
     - double raw_D0_P = D0_P

    ### Output variables
     - double keep_Y_PT = raw_Y_PT
     - double keep_Y_PE = raw_Y_PE
     - double keep_Y_PX = raw_Y_PX
     - double keep_Y_PY = raw_Y_PY
     - double keep_Y_PZ = raw_Y_PZ
     - UInt_t keep_runNumber = raw_runNumber
     - ULong64_t keep_eventNumber = raw_eventNumber
     - ULong64_t keep_GpsTime = raw_GpsTime
     - double keep_random_pt = raw_random_pt
     - double rename_y_pt = raw_Y_PT
     - double rename_y_px = raw_Y_PX
     - double rename_y_py = raw_Y_PY
     - double rename_y_pz = raw_Y_PZ
     - double calculation_RandStuff = calculation_TempStuff*3.14
     - double calculation_some_other_var = calculation_some_var*3.14
     - double calculation_alt_def = raw_Y_PE

    ### Temp variables
     - double calculation_TempStuff = raw_D0_P+raw_Y_PT
     - double calculation_some_var = rename_y_pt + rename_y_pz

    ## Input variable full names
     - raw_Y_ISOLATION_BDT
     - raw_Y_PT
     - raw_Y_PE
     - raw_Y_PX
     - raw_Y_PY
     - raw_Y_PZ
     - raw_runNumber
     - raw_eventNumber
     - raw_GpsTime
     - raw_random_pt
     - raw_D0_P

    # AnotherTuple, from TupleB0/DecayTree

    ## Selection-related

    ### Cuts
     - true
     - raw_Y_ISOLATION_BDT > 0
     - rename_b0_pt > 10000
     - raw_Y_PE > (100 * pow(10, 3))

    ### Pre-cut variables
     - double rename_b0_pt = raw_Y_PT

    ### Post-cut variables
     - double rename_b0_pt = raw_Y_PT
     - double keep_Y_PT = raw_Y_PT
     - double keep_Y_PE = raw_Y_PE
     - double keep_Y_PX = raw_Y_PX
     - double keep_Y_PY = raw_Y_PY
     - double keep_Y_PZ = raw_Y_PZ
     - UInt_t keep_runNumber = raw_runNumber
     - ULong64_t keep_eventNumber = raw_eventNumber
     - ULong64_t keep_GpsTime = raw_GpsTime
     - double keep_random_pt = raw_random_pt
     - double calculation_TempStuff = raw_D0_P+raw_Y_PT
     - double calculation_RandStuff = calculation_TempStuff*3.14

    ## Input, output and temp variables

    ### Input variables
     - double raw_Y_ISOLATION_BDT = Y_ISOLATION_BDT
     - double raw_Y_PT = Y_PT
     - double raw_Y_PE = Y_PE
     - double raw_Y_PX = Y_PX
     - double raw_Y_PY = Y_PY
     - double raw_Y_PZ = Y_PZ
     - UInt_t raw_runNumber = runNumber
     - ULong64_t raw_eventNumber = eventNumber
     - ULong64_t raw_GpsTime = GpsTime
     - double raw_random_pt = random_pt
     - double raw_D0_P = D0_P

    ### Output variables
     - double rename_b0_pt = raw_Y_PT
     - double keep_Y_PT = raw_Y_PT
     - double keep_Y_PE = raw_Y_PE
     - double keep_Y_PX = raw_Y_PX
     - double keep_Y_PY = raw_Y_PY
     - double keep_Y_PZ = raw_Y_PZ
     - UInt_t keep_runNumber = raw_runNumber
     - ULong64_t keep_eventNumber = raw_eventNumber
     - ULong64_t keep_GpsTime = raw_GpsTime
     - double keep_random_pt = raw_random_pt
     - double calculation_RandStuff = calculation_TempStuff*3.14

    ### Temp variables
     - double calculation_TempStuff = raw_D0_P+raw_Y_PT

    ## Input variable full names
     - raw_Y_ISOLATION_BDT
     - raw_Y_PT
     - raw_Y_PE
     - raw_Y_PX
     - raw_Y_PY
     - raw_Y_PZ
     - raw_runNumber
     - raw_eventNumber
     - raw_GpsTime
     - raw_random_pt
     - raw_D0_P
