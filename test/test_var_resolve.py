#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jan 10, 2021 at 05:00 AM +0100

from collections import defaultdict

from pyBabyMaker.var_resolver import Variable, VariableResolver


##############
# Containers #
##############

def test_Variable_simple():
    var = Variable('test')

    assert var.name == 'test'
    assert var.type == 'nil'
    assert var.deps == {'': []}
    assert var.resolved == {}
    assert var.idx == 0


def test_Variable_typical():
    var = Variable('test', rvalues=['a+B', 'a'])

    assert var.deps == {
        'a+B': ['a', 'B'],
        'a': ['a']
    }


def test_Variable_next():
    var1 = Variable('test')
    var2 = Variable('test', rvalues=['a', 'b'])

    assert var1.next() is False
    assert var2.next() is True
    assert var2.next() is False
    assert var2.next() is False


def test_Variable_ok():
    var1 = Variable('test')
    var2 = Variable('test', rvalues=['a'])

    assert var1.ok() is True
    assert var2.ok() is False

    var2.resolved = {'a': 'test_a'}

    assert var2.ok() is True


def test_Variable_sub():
    var = Variable('test', rvalues=['a+b'])
    var.resolved = {
        'a': 'scope1_a',
        'b': 'scope2_b',
    }

    assert var.sub() == 'scope1_a+scope2_b'


#####################
# Variable resolver #
#####################

def test_VariableResolver_trivial():
    namespace = defaultdict(list)
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('id', Variable('id')) == (True, [
        ('id', Variable('id'))
    ])