# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 07:22 PM -0400

.PHONY: build sdist clean

build:
	@python ./compile.py build_ext --inplace

sdist:
	@python ./setup.py sdist

clean:
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./pyBabyMaker.egg-info
	@find . -name '*.so' -delete
