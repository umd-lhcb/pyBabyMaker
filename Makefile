# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jun 21, 2021 at 05:16 AM +0200

include ./samples/sample.mk

.PHONY: sdist clean doc \
	install install-egg gen \
	test unittest integrationtest

sdist:
	@python ./setup.py sdist

clean:
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./gen
	@rm -rf ./pyBabyMaker.egg-info

doc:
	@sphinx-build -b html docs build

install:
	@pip install . --force-reinstall

install-egg:
	@python ./setup.py install

gen:
	@mkdir -p gen

test: unittest

##############
# Unit tests #
##############

unittest: install
	@cd test; pytest .

#####################
# Integration tests #
#####################

integrationtest: gen/sample-babymaker.root

gen/sample-babymaker.root: gen/postprocess
	gen/postprocess . gen

gen/postprocess.cpp: samples/sample-babymaker.yml samples/sample.root samples/sample_friend.root
	@mkdir -p gen
	babymaker --no-format -i $< -o $@ \
		-n ./samples/sample.root -f ./samples/sample_friend.root \
		--debug \
		-V "pi:3.14"
