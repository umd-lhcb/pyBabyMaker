#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Las Change: Tue Aug 31, 2021 at 11:38 PM +0200

import re
import logging

from collections import defaultdict
from copy import deepcopy

from pyBabyMaker.base import TermColor as TC
from pyBabyMaker.base import UniqueList, BaseMaker
from pyBabyMaker.base import update_config
from pyBabyMaker.engine.core import template_transformer, template_evaluator
from pyBabyMaker.dag_resolver import resolve_scope
from pyBabyMaker.dag_resolver import Variable


###########
# Helpers #
###########

class BabyResolver:
    def __init__(self, scopes, skip_names=[]):
        self.scopes = scopes
        self.skip_names = skip_names
        self.resolved = UniqueList()

    def resolve(self, scope,
                ordering=['literals', 'calculation', 'rename', 'raw'],
                **kwargs):
        resolved, unresolved = resolve_scope(
            scope, self.scopes, ordering, postprocess=self.postprocess,
            resolved_vars=self.resolved, **kwargs)
        self.resolved += resolved
        return resolved, unresolved

    @staticmethod
    def postprocess(var, node):
        node.input = var.input
        node.output = var.output


########################
# Configuration parser #
########################

class BabyConfigParser:
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntuple,
                 literals={}, debug=False):
        """
        Initialize the config parser with parsed YAML file and dumped ntuple
        structure.
        """
        self.parsed_config = parsed_config
        self.dumped_ntuple = dumped_ntuple
        self.literals = literals
        self.debug = debug

        if debug:
            logging.basicConfig(level=logging.DEBUG)
            self._resolvers = []

    def parse(self):
        """
        Parse the loaded YAML dict (in ``self.parsed_config``) and dumped ntuple
        tree structure (in ``self.dumped_ntuple``).
        """
        directive = {
            'system_headers': UniqueList(),
            'user_headers': UniqueList(),
            'trees': {},
            'input_trees': UniqueList(),
        }
        self.parse_headers(self.parsed_config, directive)
        parsed_literals = {k: Variable(k, literal=v)
                           for k, v in self.literals.items()}

        for output_tree, config in self.parsed_config['output'].items():
            input_tree = config['input']
            try:
                known_warnings = config['mute']
            except KeyError:
                known_warnings = []

            try:
                dumped_tree = self.dumped_ntuple[input_tree]
            except KeyError:
                print('{}Input tree {} not found, skipping {}...{}'.format(
                    TC.BOLD+TC.YELLOW, input_tree, output_tree, TC.END
                ))
                continue

            print('{}=== Handling output tree {} ==={}'.format(
                TC.BOLD+TC.BLUE, output_tree, TC.END))
            directive['input_trees'].append(input_tree)

            # Merge raw tree-specific directive with the global one.
            merge = config['inherit'] if 'inherit' in config else True
            config = update_config(self.parsed_config, config, merge=merge)
            namespace = defaultdict(dict)
            namespace['literals'] = parsed_literals
            namespace['raw'] = {n: Variable(n, t, input=True, output=False)
                                for n, t in dumped_tree.items()}

            # Load all variables in separate namespaces
            self.parse_drop_keep_rename(config, namespace)
            self.parse_calculation(config, namespace)
            self.parse_selection(config, namespace)

            skip_names = config['skip_names'] if 'skip_names' in config else []
            resolver = BabyResolver(namespace, skip_names)

            # Resolve variables needed for selection
            selection, unresolved_selection = resolver.resolve('selection')

            # Resolve all other variables
            keep, unresolved_keep = resolver.resolve('keep', ['raw'])
            rename, unresolved_rename = resolver.resolve('rename', ['raw'])
            calculation, unresolved_calculation = resolver.resolve(
                'calculation')
            resolved_vars = selection + keep + rename + calculation
            most_unresolved_vars = unresolved_keep + unresolved_rename + \
                unresolved_calculation

            # Warn about variables that can't be resolved
            most_unresolved_vars = [
                v for v in most_unresolved_vars
                if not self.match(known_warnings, v.name)]
            unresolved_selection = [
                v for v in unresolved_selection
                if not self.match(known_warnings, v.rval)]

            for var in unresolved_selection:
                print("{}Selection expr {} cannot be resolved...{}".format(
                    TC.YELLOW, var.rval, TC.END))

            for var in most_unresolved_vars:
                if var.output:
                    print("{}Output branch {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))
                else:
                    print("{}Temp variable {} cannot be resolved...{}".format(
                        TC.YELLOW, var.name, TC.END))

            directive['trees'][output_tree] = {
                'input_tree': input_tree,
                'sel': ['true']+[v.rval for v in selection if v.fake],
                'pre_sel_vars':
                [v for v in selection if not v.fake and not v.input],
                'post_sel_vars':
                [v for v in keep+rename+calculation
                 if not v.fake and not v.input],
                'input': [v for v in resolved_vars if v.input],
                'output': [v for v in resolved_vars if v.output],
                'tmp':
                [v for v in resolved_vars
                 if True not in [v.input, v.output, v.fake]],
                'input_br': [v.fname for v in resolved_vars if v.input],
            }

            # Merge raw config sections that doesn't override keys above
            config_to_merge = {k: v for k, v in config.items()
                               if k not in directive['trees'][output_tree] and
                               k not in ['headers', 'keep', 'rename',
                                         'calculation', 'selection']}
            directive['trees'][output_tree].update(config_to_merge)

        return directive

    @staticmethod
    def parse_headers(config, directive):
        """
        Parse ``headers`` section.
        """
        for header_type in ('system', 'user'):
            if 'headers' in config and header_type in config['headers']:
                directive['{}_headers'.format(header_type)] += \
                    config['headers'][header_type]

    @classmethod
    def parse_drop_keep_rename(cls, config, namespace):
        """
        Parse ``drop, keep, rename`` sections.
        """
        if 'rename' in config:
            rename_dict = config['rename']

        for var in namespace['raw'].values():
            if 'drop' in config and cls.match(config['drop'], var.name):
                print('Dropping branch: {}'.format(var.name))
                continue

            if 'rename' in config and var.name in config['rename']:
                renamed_var = rename_dict[var.name]
                namespace['rename'][renamed_var] = Variable(
                    renamed_var, var.type, [var.name])

            if 'keep' in config and cls.match(config['keep'], var.name):
                namespace['keep'][var.name] = Variable(
                    var.name, var.type, [var.name])

    @staticmethod
    def parse_calculation(config, namespace):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config:
            for name, code in config['calculation'].items():
                datatype, *rvals = [i.strip() for i in code.split(';')]
                if not rvals:
                    raise ValueError('Illegal specification for {}: {}.'.format(
                        name, code
                    ))

                output = True
                if '^' in datatype:
                    datatype = datatype.strip('^')
                    output = False

                namespace['calculation'][name] = Variable(
                    name, datatype, rvals, output=output)

    @classmethod
    def parse_selection(cls, config, namespace):
        """
        Parse ``selection`` section.
        """
        selections = deepcopy(config['global_selection']) \
            if 'global_selection' in config else []

        if 'selection' in config:
            selections += config['selection']

        for idx, expr in enumerate(selections):
            namespace['selection']['sel'+str(idx)] = Variable(
                'sel'+str(idx), rvals=[expr], input=False, output=False)

    @staticmethod
    def match(patterns, string, return_value=True):
        """
        Test if ``string`` matches at least one element in the ``patterns`` (a
        list of regular expression).

        If there's a match, return ``return_value``.
        """
        for p in patterns:
            if bool(re.search(r'{}'.format(p), string)):
                return return_value
        return not return_value


#############
# BabyMaker #
#############

class BabyMaker(BaseMaker):
    """
    ``babymaker`` class to glue parser and code generator together.
    """
    def __init__(self, config_filename, ntuple_filename, friend_filenames,
                 template_filename,
                 use_reformatter=True):
        """
        Initialize with path to YAML file and ntuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.friend_filenames = friend_filenames
        self.template_filename = template_filename
        self.use_reformatter = use_reformatter

    def gen(self, filename, literals={}, blocked_trees=[], debug=False):
        """
        Generate C++ file based on inputs.
        """
        parsed_config = self.read(self.config_filename)
        dumped_ntuple, tree_relations = self.dump_ntuples(blocked_trees)
        directive = self.directive_gen(
            parsed_config, dumped_ntuple, literals, debug)

        # Adding ntuple info to the directive
        directive['ntuple'] = self.ntuple_filename
        directive['friends'] = self.friend_filenames
        directive['tree_relations'] = tree_relations

        with open(self.template_filename) as tmpl:
            macros = template_transformer(tmpl, directive)

        output_cpp = template_evaluator(macros)

        with open(filename, 'w') as f:
            f.write(''.join(output_cpp))
        if self.use_reformatter:
            self.reformat(filename)

    def debug(self, filename, literals={}, blocked_trees=[], debug=False):
        """
        Generate a debug file for the directives that will be used for C++
        generation.
        """
        parsed_config = self.read(self.config_filename)
        dumped_ntuple, _ = self.dump_ntuples(blocked_trees)
        directive = self.directive_gen(
            parsed_config, dumped_ntuple, literals, debug)

        with open(filename, 'w') as f:
            f.write(self.directive_debug(directive))

    def dump_ntuples(self, blocked_trees=[]):
        """
        Dump main ntuple and all friend ntuples.
        """
        trees = self.dump(self.ntuple_filename)
        # Remove blocked input trees
        trees = {k: v for k, v in trees.items() if k not in blocked_trees}
        tree_relations = {k: [] for k in trees}

        for friend in self.friend_filenames:
            friend_trees = self.dump(friend)

            for t in trees:
                in_friend = t in friend_trees
                tree_relations[t].append(in_friend)

                if in_friend:
                    # Mark branches in friend trees as available
                    trees[t].update(friend_trees[t])

        return trees, tree_relations

    @staticmethod
    def directive_gen(parsed_config, dumped_ntuple,
                      literals={}, debug=False):
        """
        Generate data structure (``directive``) needed for the C++ macro
        template.
        """
        parser = BabyConfigParser(parsed_config, dumped_ntuple, literals, debug)
        return parser.parse()

    @staticmethod
    def directive_debug(directive):
        """
        Generate a plain-text representation of the directive.

        Currently we only generate the 'trees' part
        """
        output = ''

        for tree, val in directive['trees'].items():
            output += '# {}, from {}\n\n'.format(tree, val['input_tree'])

            output += '## Selection-related\n\n'
            for key, repl in [('sel', 'Cuts'),
                              ('pre_sel_vars', 'Pre-cut variables'),
                              ('post_sel_vars', 'Post-cut variables')]:
                output += '### {}\n'.format(repl)
                for i in val[key]:
                    output += ' - {}\n'.format(i)
                output += '\n'

            output += '## Input, output and temp variables\n\n'
            for key, repl in [('input', 'Input variables'),
                              ('output', 'Output variables'),
                              ('tmp', 'Temp variables')]:
                output += '### {}\n'.format(repl)
                for i in val[key]:
                    output += ' - {}\n'.format(i)
                output += '\n'

            output += '## Input variable full names\n'
            for i in val['input_br']:
                output += ' - {}\n'.format(i)

            output += '\n'

        return output
