# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 06:26 PM -0400

include ./samples/sample.mk

.PHONY: build sdist clean doc test unittest integratedtest

build:
	@python ./compile.py build_ext --inplace

sdist:
	@python ./setup.py sdist

install:
	@python ./setup.py install

clean:
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./gen
	@rm -rf ./pyBabyMaker.egg-info
	@find . -name '*.so' -delete

doc:
	@sphinx-build -b html docs build

test: unittest integratedtest

##############
# Unit tests #
##############

unittest:
	@coverage run --source pyBabyMaker setup.py test

####################
# Integrated tests #
####################

integratedtest: gen/sample-babymaker.root
	@mkdir -p gen

gen/sample-babymaker.root: samples/sample.root gen/postprocess
	gen/postprocess $< $@

gen/postprocess.cpp: samples/sample-babymaker.yml samples/sample.root
	babymaker -i $< -o $@ -d ./samples/sample.root
