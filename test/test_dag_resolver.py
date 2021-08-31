#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Aug 31, 2021 at 07:54 PM +0200

from collections import defaultdict

from pyBabyMaker.dag_resolver import Variable, Node
from pyBabyMaker.dag_resolver import resolve_var, resolve_vars_in_scope


##############
# Containers #
##############

def test_Variable_simple():
    var = Variable('test')

    assert var.name == 'test'
    assert var.type is None
    assert var.rvals == []
    assert not var.literal


def test_Variable_typical():
    var = Variable('test', rvals=['a+B', 'a'])

    assert list(var) == [
        ('a+B', ['a', 'B']),
        ('a', ['a'])
    ]


def test_Variable_repr():
    var1 = Variable('test', 'Double_t', ['a+b', 'a', 'b'])
    var2 = Variable('pi', rvals=['3.14'], literal=True)

    assert str(var1) == 'Double_t test = a+b|a|b'
    assert str(var2) == 'pi := 3.14'


def test_Node_properties():
    var1 = Node('test')
    var2 = Node('test', literal='a')
    var3 = Node('test', expr='a+b')

    assert var1.fname == 'None_test'
    assert var1.fake is False
    assert var1.rval == 'test'

    assert var2.fname == 'None_test'
    assert var2.fake is False
    assert var2.rval == 'a'

    assert var3.fname == 'None_test'
    assert var3.fake is True
    assert var3.rval == 'a+b'


def test_Node_sub():
    var = Node('test', expr='a+b')
    var.children = [
        Node('a', 'scope1'),
        Node('b', 'scope2')
    ]

    assert var.rval == 'scope1_a+scope2_b'


#############################
# Resolve a single variable #
#############################

def test_resolve_var_trivial():
    var = Variable('id')
    scopes = defaultdict(dict)

    assert resolve_var(var, 'scope1', scopes, ['a', 'b']) == (
        True,
        Node('id', 'scope1'),
        [Node('id', 'scope1')]
    )


def test_resolve_var_simple():
    var = Variable('A', rvals=['a'])
    scopes = {'raw': {'a': Variable('a')}}

    assert resolve_var(var, 'keep', scopes, ['raw']) == (
        True,
        Node('A', 'keep', expr='a'),
        [
            Node('a', 'raw'),
            Node('A', 'keep', expr='a')
        ]
    )


def test_resolve_var_simple_fail():
    var = Variable('a', rvals=['b'])
    scopes = {'raw': {'a': Variable('a')}}

    assert resolve_var(var, 'keep', scopes, ['raw']) == (
        False, Node('a', 'keep', expr='b'), [])


def test_resolve_var_multi_scope():
    scopes = {
        'rename': {
            'x': Variable('x', rvals=['a'])
        },
        'raw': {
            'a': Variable('a'),
            'b': Variable('b')
        }
    }
    var = Variable('a', rvals=['x+b'])

    assert resolve_var(var, 'calc', scopes, ordering=['rename', 'raw']) == (
        True,
        Node('a', 'calc', expr='x+b'),
        [
            Node('a', 'raw'),
            Node('x', 'rename', expr='a'),
            Node('b', 'raw'),
            Node('a', 'calc', expr='x+b')
        ]
    )


def test_resolve_var_multi_scope_literal_shadow():
    scopes = {
        'rename': {
            'x': Variable('x', rvals=['a'])
        },
        'raw': {
            'a': Variable('a'),
            'b': Variable('b')
        },
        'literals': {
            'b': Variable('b', literal='343')
        }
    }
    var = Variable('a', rvals=['x+b'])
    result = resolve_var(
        var, 'calc', scopes, ordering=['literals', 'rename', 'raw'])

    assert result == (
        True,
        Node('a', 'calc', expr='x+b'),
        [
            Node('a', 'raw'),
            Node('x', 'rename', expr='a'),
            Node('a', 'calc', expr='x+b')
        ]
    )
    assert result[1].rval == 'rename_x+343'


def test_resolve_var_multi_scope_fail():
    scopes = {
        'rename': {
            'x': Variable('x', rvals=['a'])
        },
        'raw': {
            'a': Variable('a'),
            'b': Variable('b')
        }
    }
    var = Variable('a', rvals=['b+y'])
    result = resolve_var(var, 'calc', scopes, ordering=['rename', 'raw'])

    assert result == (
        False,
        Node('a', 'calc', expr='b+y'),
        []
    )
    assert result[1].children == [Node('b', 'raw')]


def test_resolve_var_multi_scope_alt_def():
    scopes = {
        'rename': {
            'x': Variable('x', rvals=['a'])
        },
        'raw': {
            'a': Variable('a'),
            'b': Variable('b')
        }
    }
    var = Variable('a', rvals=['b+y', 'x+b'])
    result = resolve_var(var, 'calc', scopes, ordering=['rename', 'raw'])

    assert result == (
        True,
        Node('a', 'calc', expr='x+b'),
        [
            Node('a', 'raw'),
            Node('x', 'rename', expr='a'),
            Node('b', 'raw'),
            Node('a', 'calc', expr='x+b')
        ]
    )
    assert result[1].rval == 'rename_x+raw_b'


def test_resolve_var_existing_var():
    resolved_vars = [Node('a', 'rename', expr='x', children=[Node('x', 'raw')])]
    var = Variable('a', rvals=['x'])
    result = resolve_var(
        var, 'rename', {'raw': {}}, ['raw'], resolved_vars=resolved_vars)

    assert result == (True, Node('a', 'rename', expr='x'), [])
    assert result[1].rval == 'raw_x'


def test_resolve_var_circular():
    var = Variable('x', rvals=['GEV2(x)'])
    scopes = {
        'calc': {
            'x': var,
        },
        'raw': {
            'x': Variable('x'),
        }
    }
    result = resolve_var(var, 'calc', scopes, ordering=['calc', 'raw'])

    assert result == (
        True,
        Node('x', 'calc', expr='GEV2(x)'),
        [
            Node('x', 'raw'),
            Node('x', 'calc', expr='GEV2(x)')
        ]
    )
    assert result[1].rval == 'GEV2(raw_x)'


def test_resolve_var_full_fail():
    scopes = {
        'raw': {},
        'rename': {'a': Variable('x', rvals=['c'])}
    }
    var = Variable('x', rvals=['a+b'])

    assert resolve_var(var, 'calc', scopes, ordering=['rename', 'raw']) == (
        False, Node('x', 'calc', expr='a+b'), []
    )


def test_resolve_var_skip_names_simple():
    var = Variable('x', rvals=['300*GeV'])
    result = resolve_var(var, 'calc', {'raw': {}}, ['raw'], skip_names=['GeV'])

    assert result == (
        True,
        Node('x', 'calc', expr='300*GeV'),
        [Node('x', 'calc', expr='300*GeV')]
    )
    assert result[1].rval == '300*GeV'


def test_resolve_var_selection():
    scopes = {
        'raw': {
            'k_PT': Variable('k_PT'),
            'pi_PT': Variable('pi_PT')
        }
    }
    var = Variable('sel0', rvals=['k_PT + pi_PT > 1400.0*MeV'])

    result = resolve_var(var, 'sel', scopes, ['raw'], skip_names=['MeV'])
    assert result == (
        True,
        Node('sel0', 'sel', expr='k_PT + pi_PT > 1400.0*MeV'),
        [
            Node('k_PT', 'raw'),
            Node('pi_PT', 'raw'),
            Node('sel0', 'sel', expr='k_PT + pi_PT > 1400.0*MeV'),
        ]
    )
    assert result[1].rval == 'raw_k_PT + raw_pi_PT > 1400.0*MeV'
    assert result[1].fake is True


################################################
# Resolve multiple variables in a single scope #
################################################

def test_resolve_vars_in_scope_vars_simple():
    scopes = {
        'calc': {
            'a': Variable('a', rvals=['b/c']),
            'b': Variable('b', rvals=['GEV2(b)']),
        },
        'rename': {
            'c': Variable('c', rvals=['x'])
        },
        'raw': {
            'b': Variable('b'),
            'x': Variable('x')
        }
    }
    result = resolve_vars_in_scope(
        scopes['calc'].values(), 'calc', scopes,
        ordering=['calc', 'rename', 'raw'])

    assert result == (
        [
            Node('b', 'raw'),
            Node('b', 'calc', expr='GEV2(b)'),
            Node('x', 'raw'),
            Node('c', 'rename', expr='x'),
            Node('a', 'calc', expr='b/c')
        ],
        []
    )
    assert result[0][-1].rval == 'calc_b/rename_c'


def test_reslove_vars_in_scope_vars_partial():
    scopes = {
        'calc': {
            'a': Variable('a', rvals=['d/c']),
            'b': Variable('b', rvals=['GEV2(b)']),
        },
        'rename': {
            'c': Variable('c', rvals=['x'])
        },
        'raw': {
            'b': Variable('b'),
            'x': Variable('x')
        }
    }
    result = resolve_vars_in_scope(
        scopes['calc'].values(), 'calc', scopes,
        ordering=['calc', 'rename', 'raw'])

    assert result == (
        [
            Node('b', 'raw'),
            Node('b', 'calc', expr='GEV2(b)'),
        ],
        [
            Node('a', 'calc', expr='d/c')
        ]
    )
    assert result[1][0].children == [
        Node('c', 'rename', expr='x')
    ]
    assert result[1][0].children[0].children == [
        Node('x', 'raw')
    ]


###########################################
# Resolve all variables in a single scope #
###########################################

# def test_VariableResolver_scope_unknown():
    # resolver = VariableResolver({})
    # assert resolver.resolve_scope('test') == ([], [])


# def test_VariableResolver_scope_resolve():
    # namespace = {
        # 'calc': {
            # 'a': Variable('a', rvalues=['c/b']),
            # 'b': Variable('b', rvalues=['GEV2(b)']),
            # 'c': Variable('c', rvalues=['b*b'])
        # },
        # 'rename': {
            # 'c': Variable('c', rvalues=['x'])
        # },
        # 'raw': {
            # 'b': Variable('b'),
            # 'x': Variable('x')
        # }
    # }
    # resolver = VariableResolver(namespace)
    # result = resolver.resolve_scope('calc')

    # assert result == (
        # [
            # ('raw', Variable('b')),
            # ('calc', Variable('b', rvalues=['GEV2(b)'])),
            # ('calc', Variable('c', rvalues=['b*b'])),
            # ('calc', Variable('a', rvalues=['c/b']))
        # ],
        # []
    # )
    # assert result[0][1][1].rval == 'GEV2(raw_b)'
    # assert result[0][2][1].rval == 'calc_b*calc_b'
    # assert result[0][3][1].rval == 'calc_c/calc_b'


# # NOTE: In a real use case, the dependency variables in 'selection' were
# #       resolved multiple times, thus an error message was emitted.
# def test_VariableResolver_scope_duplicated_resolution():
    # namespace = {
        # 'sel': {
            # 'sel0': Variable('sel0', rvalues=['mu_pid > 0']),
            # 'sel1': Variable('sel1', rvalues=['test > 0'])
        # },
        # 'calc': {
            # 'mu_pid': Variable('mu_pid',
                               # rvalues=['MU_PID(mu_true_id)',
                                        # 'MU_PID(mu_is_mu, mu_pid_mu)']),
            # 'test': Variable('test', rvalues=['TEST(mu_pid_mu, mu_is_mu)'])
        # },
        # 'rename': {
            # 'mu_true_id': Variable('mu_true_id', rvalues=['mu_TRUEID']),
            # 'mu_is_mu': Variable('mu_is_mu', rvalues=['mu_isMuon']),
            # 'mu_pid_mu': Variable('mu_pid_mu', rvalues=['mu_PIDmu'])
        # },
        # 'raw': {
            # # 'mu_TRUEID': Variable('mu_TRUEID'),
            # 'mu_isMuon': Variable('mu_isMuon'),
            # 'mu_PIDmu': Variable('mu_PIDmu')
        # }
    # }
    # resolver = VariableResolver(namespace)
    # result = resolver.resolve_scope('sel', ordering=['calc', 'rename', 'raw'])

    # assert result == (
        # [
            # ('raw', Variable('mu_isMuon')),
            # ('rename', Variable('mu_is_mu', rvalues=['mu_isMuon'])),
            # ('raw', Variable('mu_PIDmu')),
            # ('rename', Variable('mu_pid_mu', rvalues=['mu_PIDmu'])),
            # ('calc', Variable('mu_pid',
                              # rvalues=['MU_PID(mu_true_id)',
                                       # 'MU_PID(mu_is_mu, mu_pid_mu)'])),
            # ('sel', Variable('sel0', rvalues=['mu_pid > 0'])),
            # ('calc', Variable('test', rvalues=['TEST(mu_pid_mu, mu_is_mu)'])),
            # ('sel', Variable('sel1', rvalues=['test > 0']))
        # ],
        # []
    # )


# # NOTE: In a real use case, two selection variables have common dependencies. If
# #       the first one can't be fully resolved, the dependencies of the second
# #       variable were not fully resolved
# # NOTE: The 'simple' case initially worked; the 'complex' one doesn't
# def test_VariableResolver_partial_common_deps_simple():
    # namespace = {
        # 'sel': {
            # 'sel0': Variable('sel0', rvalues=['flag_d0mu']),
            # 'sel1': Variable('sel1', rvalues=['flag_mu'])
        # },
        # 'calc': {
            # 'flag_d0mu': Variable(
                # 'flag_d0mu',
                # rvalues=['FLAG_D0MU(mu_isMuon, k_isMuon, pi_isMuon)']
            # ),
            # 'flag_mu': Variable('flag_mu', rvalues=['FLAG_MU(mu_isMuon)'])
        # },
        # 'raw': {
            # # 'mu_TRUEID': Variable('mu_TRUEID'),
            # 'mu_isMuon': Variable('mu_isMuon'),
            # 'k_isMuon': Variable('k_isMuon'),
        # }
    # }
    # resolver = VariableResolver(namespace)
    # result = resolver.resolve_scope('sel', ordering=['calc', 'raw'])

    # assert result == (
        # [
            # ('raw', Variable('mu_isMuon')),
            # ('calc', Variable('flag_mu', rvalues=['FLAG_MU(mu_isMuon)'])),
            # ('sel', Variable('sel1', rvalues=['flag_mu']))
        # ],
        # [
            # Variable('sel0', rvalues=['flag_d0mu'])
        # ]
    # )


# def test_VariableResolver_partial_common_deps_complex():
    # namespace = {
        # 'sel': {
            # 'sel0': Variable('sel0', rvalues=['flag_d0mu']),
            # 'sel1': Variable('sel1', rvalues=['flag_mu'])
        # },
        # 'calc': {
            # 'flag': Variable('flag', rvalues=['FLAG(mu_PT)']),
            # 'flag_d0mu': Variable(
                # 'flag_d0mu',
                # rvalues=['FLAG_D0MU(flag, mu_isMuon, k_isMuon, pi_isMuon)']
            # ),
            # 'flag_mu': Variable('flag_mu', rvalues=['FLAG_MU(flag, mu_isMuon)'])
        # },
        # 'raw': {
            # # 'mu_TRUEID': Variable('mu_TRUEID'),
            # 'mu_isMuon': Variable('mu_isMuon'),
            # 'k_isMuon': Variable('k_isMuon'),
            # 'mu_PT': Variable('mu_PT')
        # }
    # }
    # resolver = VariableResolver(namespace)
    # result = resolver.resolve_scope('sel', ordering=['calc', 'raw'])

    # assert result == (
        # [
            # ('raw', Variable('mu_PT')),  # This one was missing!
            # ('calc', Variable('flag', rvalues=['FLAG(mu_PT)'])),
            # ('raw', Variable('mu_isMuon')),
            # ('calc', Variable('flag_mu', rvalues=['FLAG_MU(flag, mu_isMuon)'])),
            # ('sel', Variable('sel1', rvalues=['flag_mu']))
        # ],
        # [
            # Variable('sel0', rvalues=['flag_d0mu'])
        # ]
    # )


# # NOTE: In a case, when using an alternative rvalue, the dependencies of its
# #       dependencies are not resolved correctly
# def test_VariableResolver_alternative_rvalue_dep_deep():
    # namespace = {
        # 'calc': {
            # 'other_trk': Variable(
                # 'other_trk', rvalues=['VEC(trk_k, trk_pi, trk_spi)',
                                      # 'VEC(trk_k, trk_pi)']),
            # 'trk_k': Variable('trk_k', rvalues=['FAKE(k_PT)']),
            # 'trk_pi': Variable('trk_pi', rvalues=['FAKE(pi_PT)']),
            # 'trk_spi': Variable('trk_spi', rvalues=['FAKE(spi_PT)'])
        # },
        # 'raw': {
            # 'k_PT': Variable('k_PT'),
            # 'pi_PT': Variable('pi_PT'),
            # # 'spi_PT': Variable('spi_PT')
        # }
    # }
    # resolver = VariableResolver(namespace)
    # result = resolver.resolve_scope('calc', ordering=['calc', 'raw'])

    # assert result == (
        # [
            # ('raw', Variable('k_PT')),
            # ('calc', Variable('trk_k', rvalues=['FAKE(k_PT)'])),
            # ('raw', Variable('pi_PT')),
            # ('calc', Variable('trk_pi', rvalues=['FAKE(pi_PT)'])),
            # ('calc', Variable('other_trk',
                              # rvalues=['VEC(trk_k, trk_pi, trk_spi)',
                                       # 'VEC(trk_k, trk_pi)'])),
        # ],
        # [
            # Variable('trk_spi', rvalues=['FAKE(spi_PT)'])
        # ]
    # )