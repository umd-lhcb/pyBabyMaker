# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 27, 2019 at 03:54 PM -0400

.PHONY: build sdist clean

build:
	@python ./compile.py build_ext --inplace

sdist:
	@python ./setup.py sdist

install:
	@python ./setup.py install

clean:
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./pyBabyMaker.egg-info
	@find . -name '*.so' -delete
