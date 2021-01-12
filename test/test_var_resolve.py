#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Jan 12, 2021 at 04:36 AM +0100

from collections import defaultdict
from pytest import raises

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

    assert var.rval == 'scope1_a+scope2_b'


def test_Variable_eq():
    var1 = Variable('test', rvalues=['a+b', 'c+d'])
    var2 = Variable('test', rvalues=['a+b', 'c+d'])
    var1.next()

    assert var1 == var2
    assert var1.idx == 1
    assert var2.idx == 0


def test_Variable_repr():
    var = Variable('test', 'Double_t', ['a+b', 'a', 'b'])
    assert str(var) == 'Double_t test = a+b|a|b'


#############################
# Resolve a single variable #
#############################

def test_VariableResolver_trivial():
    namespace = defaultdict(dict)
    resolver = VariableResolver(namespace)
    var = Variable('id')

    assert resolver.resolve_var('id', Variable('id')) == (
        True,
        [('id', var)],
        [('id', 'id')]
    )
    assert resolver._resolved_names == []


def test_VariableResolver_simple():
    namespace = {'raw': {'a': Variable('a')}}
    resolver = VariableResolver(namespace)
    var = Variable('a', rvalues=['a'])

    assert resolver.resolve_var('keep', var) == (
        True,
        [
            ('raw', Variable('a')),
            ('keep', var)
        ],
        [
            ('raw', 'a'),
            ('keep', 'a')
        ]
    )
    assert resolver._resolved_names == []

    # Do it again (and again) and the result should be the same
    assert resolver.resolve_var('keep', var) == \
        resolver.resolve_var('keep', var)
    assert resolver._resolved_names == []


def test_VariableResolver_simple_fail():
    namespace = {'raw': {'a': Variable('a')}}
    resolver = VariableResolver(namespace)
    var = Variable('a', rvalues=['b'])

    assert resolver.resolve_var('keep', var) == (False, [], [])
    assert resolver._resolved_names == []


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
    var = Variable('a', rvalues=['x+b'])

    assert resolver.resolve_var('calc', var, ordering=['rename', 'raw']) == (
        True,
        [
            ('raw', Variable('a')),
            ('rename', Variable('x', rvalues=['a'])),
            ('raw', Variable('b')),
            ('calc', var)
        ],
        [
            ('raw', 'a'),
            ('rename', 'x'),
            ('raw', 'b'),
            ('calc', 'a')
        ]
    )


def test_VariableResolver_multi_scope_fail():
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
    var = Variable('a', rvalues=['b+y'])

    assert resolver.resolve_var('calc', var, ordering=['rename', 'raw']) == (
        False,
        [('raw', Variable('b'))],
        [('raw', 'b')]
    )


def test_VariableResolver_multi_scope_alt_def():
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
    var = Variable('a', rvalues=['b+y', 'x+b'])

    assert resolver.resolve_var('calc', var, ordering=['rename', 'raw']) == (
        True,
        [
            ('raw', Variable('a')),
            ('rename', Variable('x', rvalues=['a'])),
            ('raw', Variable('b')),
            ('calc', var)
        ],
        [
            ('raw', 'a'),
            ('rename', 'x'),
            ('raw', 'b'),
            ('calc', 'a')
        ]
    )
    assert var.idx == 1
    assert var.rval == 'rename_x+raw_b'


def test_VariableResolver_existing_var():
    resolver = VariableResolver({})
    resolver._resolved_names = [('rename', 'a')]
    var = Variable('a', rvalues=['x'])

    assert resolver.resolve_var('rename', var) == (
        True, [], []  # No need to resolve since it's already loaded before
    )


def test_VariableResolver_circular():
    var = Variable('x', rvalues=['GEV2(x)'])
    namespace = {
        'calc': {
            'x': var,
        },
        'raw': {
            'x': Variable('x'),
        }
    }
    resolver = VariableResolver(namespace)

    assert resolver.resolve_var('calc', var, ordering=['calc', 'raw']) == (
        True,
        [
            ('raw', Variable('x')),
            ('calc', var)
        ],
        [
            ('raw', 'x'),
            ('calc', 'x')
        ]
    )
    assert var.rval == 'GEV2(raw_x)'


def test_VariableResolver_full_fail():
    resolver = VariableResolver({
        'raw': {},
        'rename': {'a': Variable('x', rvalues=['c'])}
    })
    var = Variable('x', rvalues=['a+b'])

    assert resolver.resolve_var('calc', var, ordering=['rename', 'raw']) == (
        False, [], []
    )
    assert var.idx == 0
    assert not var.ok


################################################
# Resolve multiple variables in a single scope #
################################################

def test_VariableResolver_vars_simple():
    namespace = {
        'calc': {
            'a': Variable('a', rvalues=['b/c']),
            'b': Variable('b', rvalues=['GEV2(b)']),
        },
        'rename': {
            'c': Variable('c', rvalues=['x'])
        },
        'raw': {
            'b': Variable('b'),
            'x': Variable('x')
        }
    }
    resolver = VariableResolver(namespace)
    result = resolver.resolve_vars_in_scope(
        'calc', namespace['calc'].values(), ordering=['calc', 'rename', 'raw'])

    assert result == (
        [
            ('raw', Variable('b')),
            ('calc', Variable('b', rvalues=['GEV2(b)'])),
            ('raw', Variable('x')),
            ('rename', Variable('c', rvalues=['x'])),
            ('calc', Variable('a', rvalues=['b/c']))
        ],
        []
    )
    assert result[0][4][1].rval == 'calc_b/rename_c'


def test_VariableResolver_vars_partial():
    namespace = {
        'calc': {
            'a': Variable('a', rvalues=['d/c']),
            'b': Variable('b', rvalues=['GEV2(b)']),
        },
        'rename': {
            'c': Variable('c', rvalues=['x'])
        },
        'raw': {
            'b': Variable('b'),
            'x': Variable('x')
        }
    }
    resolver = VariableResolver(namespace)
    result = resolver.resolve_vars_in_scope(
        'calc', namespace['calc'].values(), ordering=['calc', 'rename', 'raw'])

    assert result == (
        [
            ('raw', Variable('b')),
            ('calc', Variable('b', rvalues=['GEV2(b)'])),
        ],
        [
            Variable('a', rvalues=['d/c']),
        ]
    )
    assert result[0][1][1].rval == 'GEV2(raw_b)'


###########################################
# Resolve all variables in a single scope #
###########################################

def test_VariableResolver_scope_unknown():
    resolver = VariableResolver({})

    with raises(KeyError) as e:
        assert resolver.resolve_scope('test')
    assert e.value.args[0] == 'Unknown scope: test.'


def test_VariableResolver_scope_resolve():
    namespace = {
        'calc': {
            'a': Variable('a', rvalues=['c/b']),
            'b': Variable('b', rvalues=['GEV2(b)']),
            'c': Variable('c', rvalues=['b*b'])
        },
        'rename': {
            'c': Variable('c', rvalues=['x'])
        },
        'raw': {
            'b': Variable('b'),
            'x': Variable('x')
        }
    }
    resolver = VariableResolver(namespace)
    result = resolver.resolve_scope('calc')

    assert result == (
        [
            ('raw', Variable('b')),
            ('calc', Variable('b', rvalues=['GEV2(b)'])),
            ('calc', Variable('c', rvalues=['b*b'])),
            ('calc', Variable('a', rvalues=['c/b']))
        ],
        []
    )
    assert result[0][1][1].rval == 'GEV2(raw_b)'
    assert result[0][2][1].rval == 'calc_b*calc_b'
    assert result[0][3][1].rval == 'calc_c/calc_b'
