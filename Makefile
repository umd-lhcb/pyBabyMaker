# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Jul 06, 2019 at 03:03 AM -0400

.PHONY: build clean

build:
	@python ./compile.py build_ext --inplace

clean:
	@rm -rf ./build/*
	@find . -name '*.so' -delete
