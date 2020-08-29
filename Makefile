# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Aug 30, 2020 at 01:23 AM +0800

include ./samples/sample.mk

.PHONY: build sdist clean doc \
	install gen \
	test unittest unittest-local integrationtest

build:
	@python ./compile.py build_ext --inplace

sdist:
	@python ./setup.py sdist

install:
	@pip install . --force-reinstall

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

unittest: install
	@pip list
	@tree /home/travis/virtualenv/python3.8.1/lib/site-packages
	@coverage run -m pytest ./test

unittest-local: install
	@pytest ./test

#####################
# Integration tests #
#####################

integrationtest: install gen/sample-babymaker.root

gen/sample-babymaker.root: samples/sample.root gen/postprocess
	gen/postprocess $< $@

gen/postprocess.cpp: samples/sample-babymaker.yml samples/sample.root gen
	babymaker -i $< -o $@ -d ./samples/sample.root

gen:
	@mkdir -p gen
