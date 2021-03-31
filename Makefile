# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 31, 2021 at 10:58 PM +0200

include ./samples/sample.mk

.PHONY: build sdist clean doc \
	install install-egg gen \
	test unittest integrationtest

sdist:
	@python ./setup.py sdist

install:
	@pip install . --force-reinstall

install-egg:
	@python ./setup.py install

clean:
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./gen
	@rm -rf ./pyBabyMaker.egg-info
	@find . -name '*.so' -delete

doc:
	@sphinx-build -b html docs build

test: unittest

##############
# Unit tests #
##############

unittest: install
	@pytest ./test

#####################
# Integration tests #
#####################

integrationtest: gen/sample-babymaker.root

gen/sample-babymaker.root: samples/sample.root gen/postprocess
	gen/postprocess $< $@

gen/postprocess.cpp: samples/sample-babymaker.yml samples/sample.root gen
	babymaker --debug --no-format -i $< -o $@ -d ./samples/sample.root

gen:
	@mkdir -p gen
