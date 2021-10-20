# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Oct 21, 2021 at 01:27 AM +0200

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
		-V "pi:3.14" -B "TupleB0WSPi/DecayTree"

##############
# Validation #
##############

.PHONY: validation

validation: integrationtest
	@tools/validate_with_rdf.py ./samples/sample.root ./gen/ATuple.root

#########
# Debug #
#########

debug: gen/directive.md

gen/directive.md: samples/sample-babymaker.yml samples/sample.root samples/sample_friend.root
	@mkdir -p gen
	debugmaker -i $< -o $@ \
		-n ./samples/sample.root -f ./samples/sample_friend.root \
		--debug \
		-V "pi:3.14" -B "TupleB0WSPi/DecayTree" -X ATuple
