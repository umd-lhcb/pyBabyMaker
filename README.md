# pyBabyMaker
Python babymaker (flat ntuple generation tool) library. [`babymaker`](https://github.com/manuelfs/babymaker)
was original conceived by Manuel Franco Sevilla and his colleagues
at UCSB. It was later rewritten by Yipeng Sun to make it simpler, and more
portable. The result is this project: `pyBabyMaker`.

The `pyBabyMaker` library provides the following tools to aid ntuple
processing:
* `pyBabyMaker.io.TupleDump`: There is a `PyTupleDump` class that dumps the
  tree structure, as well as the datatype, of a given ntuple.
* `babymaker`: Generate `C++` file to postprocess ntuple based on user input.
* `ntpdump`: Utilize `PyTupleDump` to generate a text file that represents the
  ntuple tree structure. Currently the output formats are:
  * `YAML`


## Installation
Please make sure `ROOT`, `gcc`, `python3`, and `pip` are installed. Make sure
that `root-config` is available in your `$PATH`, and `gcc` supports `-std=c++17`.

`babymaker` will automatically use `clang-format` to format generated `C++`
code, if `clang-format` is available in your `$PATH`.

Currently, `pyBabyMaker` is not on `PyPI`. To install:
```
pip install git+https://github.com/yipengsun/pyBabyMaker
```


## `babymaker`
`babymaker` generates `C++` source code that can do the following things to
ntuple:
* renaming
* making selections
* dropping
* doing additional calculations on selected branches of the input `.root` file

Below we list the usage of `babymaker`:
```
$ babymaker -h
usage: babymaker [-h] [-i [INPUT]] -o [OUTPUT] [-d [DATA]]
                 [-H HEADERS [HEADERS ...]]

generate compilable C++ source file for ntuple processing.

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        path to input YAML file.
  -o [OUTPUT], --output [OUTPUT]
                        path to output C++ file.
  -d [DATA], --data [DATA]
                        path to data ntuple file.
  -H HEADERS [HEADERS ...], --headers HEADERS [HEADERS ...]
                        additional headers to be included in generated C++.
```

We also provide a sample `YAML` configuration:
```yaml
ATuple:
    force_lowercase: false
    input:
        - TupleY/DecayTree
    keep:
        - ^Y_P\w$
    rename:
        Y_PT: y_pt
        Y_PX: y_px
        Y_PY: y_py
        Y_PZ: y_pz
        selection:
Y_PT: "> 10000"

AnotherTuple:
    force_lowercase: true
    headers:
        - cmath
    input:
        - TupleY/DecayTree
    keep:
        - Y_P.*
    selection:
        Y_PT: "> 10000"
        Y_PE: "> (100 * pow(10, 3))"

YetAnotherTuple:
    force_lowercase: true
    headers:
        - cmath
    input:
        - TupleY/DecayTree
        - TupleYWSPi/DecayTree
    # Drop arrays. We don't support them (yet).
    drop:
        - Y_OWNPV_COV_
    keep:
        - Y_OWNPV_.*
        - Y_ISOLATION_.*

YetYetAnotherTuple:
    force_lowercase: true
    headers:
        - functor/basic.h
    input:
        - TupleY/DecayTree
    drop:
        - Y_PE
    keep:
        - Y_P.*
    selection:
        Y_PT: "> 10000"
    calculation:
        SUM: "SUM(Y_PE, Y_P)"
```

> The `drop` section will always execute before `keep`.
>
> Also, `drop` and `keep` fully utilize regular expressions so the expressions
> `Y_P*` should not be used in most cases.


## `ntpdump`
`ntpdump` output ntuple tree structure and datatype to a text file. We list its
usage below:

```
$ ntpdump -h
usage: ntpdump [-h] [-f [{yaml,plain}]] input output

dump ntuple tree-branch structure, and branch datatype.

positional arguments:
  input                 specify path to input ntuple file.
  output                specify path to output YAML file.

optional arguments:
  -h, --help            show this help message and exit
  -f [{yaml,plain}], --output-format [{yaml,plain}]
                        select output format.
```
