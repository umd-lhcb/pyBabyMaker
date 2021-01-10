#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Jan 10, 2021 at 05:35 AM +0100

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

    assert var1.ok is True
    assert var2.ok is False

    var2.resolved = {'a': 'test_a'}

    assert var2.ok is True


def test_Variable_sub():
    var = Variable('test', rvalues=['a+b'])
    var.resolved = {
        'a': 'scope1_a',
        'b': 'scope2_b',
    }

    assert var.sub == 'scope1_a+scope2_b'


def test_Variable_eq():
    var1 = Variable('test', rvalues=['a+b', 'c+d'])
    var2 = Variable('test', rvalues=['a+b', 'c+d'])
    var1.next()

    assert var1 == var2
    assert var1.idx == 1
    assert var2.idx == 0


#####################
# Variable resolver #
#####################

def test_VariableResolver_trivial():
    namespace = defaultdict(dict)
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('id', Variable('id')) == (True, [
        ('id', Variable('id'))
    ])
    assert resolver._resolved_vars == [
        'id_id'
    ]


def test_VariableResolver_simple():
    namespace = {'raw': {'a': Variable('a')}}
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('keep', Variable('a', rvalues=['a'])) == \
        (True, [
            ('raw', Variable('a')),
            ('keep', Variable('a', rvalues=['a']))
        ])
    assert resolver._resolved_vars == [
        'raw_a',
        'keep_a'
    ]


def test_VariableResolver_simple_fail():
    namespace = {'raw': {'a': Variable('a')}}
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('keep', Variable('a', rvalues=['b'])) == \
        (False, [])
    assert resolver._resolved_vars == []


def test_VariableResolver_multi_scope():
    namespace = {
        'rename': {
            'x': Variable('x', rvalues=['a'])
        },
        'raw': {
            'a': Variable('a'),
            'b': Variable('b')
        }
    }
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('calc', Variable('a', rvalues=['x+b']),
                                ordering=['rename', 'raw']) == \
        (True, [
            ('raw', Variable('a')),
            ('rename', Variable('x', rvalues=['a'])),
            ('raw', Variable('b')),
            ('calc', Variable('a', rvalues=['x+b']))
        ])
    assert resolver._resolved_vars == [
        'raw_a',
        'rename_x',
        'raw_b',
        'calc_a'
    ]
