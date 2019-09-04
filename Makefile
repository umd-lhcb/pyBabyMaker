# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Sep 04, 2019 at 06:30 PM -0400

include ./samples/sample.mk

.PHONY: build sdist clean doc test unittest integrationtest

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

test: unittest integrationtest

##############
# Unit tests #
##############

unittest:
	@coverage run --source pyBabyMaker setup.py test

#####################
# Integration tests #
#####################

integrationtest: gen/sample-babymaker.root

gen/sample-babymaker.root: samples/sample.root gen/postprocess
	gen/postprocess $< $@

gen/postprocess.cpp: samples/sample-babymaker.yml samples/sample.root gen
	babymaker -i $< -o $@ -d ./samples/sample.root

gen:
	@mkdir -p gen
