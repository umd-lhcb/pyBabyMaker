# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 31, 2019 at 12:42 AM -0400

.PHONY: build sdist clean doc test

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

doc:
	@sphinx-build -b html docs build

test:
	@coverage run --source pyBabyMaker,pyBabyMaker.io setup.py test
