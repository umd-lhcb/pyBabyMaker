#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Sep 04, 2020 at 02:40 AM +0800

from pyBabyMaker.base import UniqueList, BaseMaker, Variable


########################
# Configuration parser #
########################


class BabyConfigParser(object):
    """
    Basic parser for YAML C++ code instruction.
    """
    def __init__(self, parsed_config, dumped_ntuple):
        """
        Initialize the config parser with parsed YAML file and dumped n-tuple
        structure.
        """
        self.parsed_config = parsed_config
        self.dumped_ntuple = dumped_ntuple

        # Components in the template macro directive
        self.system_headers = UniqueList()
        self.user_headers = UniqueList()
        self.input_branches = UniqueList()
        self.output_variables = UniqueList()
        self.transient_variables = UniqueList()

    def gen_directive(self):
        """
        Parse the loaded YAML dict (in ``self.parsed_config`) and dumped ntuple
        tree structure (in ``self.dumped_ntuple``).
        """
        directive = {
            'system_headers': UniqueList(),
            'user_headers': UniqueList(),
        }

        for output_tree, config in self.parsed_config.items():
            input_tree = config['input_tree']
            dumped_tree = self.dumped_ntuple[input_tree]

            directive[output_tree] = {
                'input_tree': input_tree,
                'input_branches': UniqueList(),
                'output_branches': UniqueList(),
                'transient_variables': UniqueList(),
            }

            self.parse_headers(config, directive)
            self.parse_drop_keep_rename(config, dumped_tree,
                                        directive[output_tree])
            self.parse_calculation(config, dumped_tree, directive)
            self.parse_selection(config, dumped_tree, directive)

        return directive

    def parse_headers(self, config, directive):
        """
        Parse ``headers`` section.
        """
        for header_type in ('system', 'user'):
            try:
                directive['{}_headers'.format(header_type)] += \
                    config['headers'][header_type]
            except KeyError:
                pass

    def parse_drop_keep_rename(self, config, dumped_tree, directive):
        """
        Parse ``drop, keep, rename`` sections.
        """
        branches_to_keep = []
        for br_in, datatype in dumped_tree.items():
            if 'drop' in config.keys() and self.match(config['drop'], br_in):
                print('Dropping branch: {}'.format(br_in))
            elif 'keep' in config.keys() and self.match(config['keep'], br_in):
                branches_to_keep.append((datatype, br_in))
            elif 'rename' in config.keys() and br_in in config['rename']:
                branches_to_keep.append((datatype, br_in))

        for datatype, br_in in branches_to_keep:
            directive['input_branches'].append(Variable(datatype, br_in))
            # Handle branch rename here
            try:
                br_out = config['rename'][br_in]
                directive['output_branches'].append(
                    Variable(datatype, br_out, br_in))
            except KeyError:
                directive['output_branches'].append(
                    Variable(datatype, br_in, br_in))

    def parse_calculation(self, config, dumped_tree, data_store):
        """
        Parse ``calculation`` section.
        """
        if 'calculation' in config.keys():
            for name, code in config['calculation'].items():
                datatype, rvalue = code.split(';')
                if datatype == '^':
                    self.__getattribute__(rvalue)(name, dumped_tree, data_store)
                elif '^' in datatype:
                    datatype = datatype.strip('^')
                    data_store.append_transient(
                        Variable(datatype, name, rvalue)
                    )
                    self.load_missing_variables(rvalue, dumped_tree, data_store)
                else:
                    data_store.append_output_br(
                        Variable(datatype, name, rvalue)
                    )
                    self.load_missing_variables(rvalue, dumped_tree, data_store)

    def parse_selection(self, config, dumped_tree, data_store):
        """
        Parse ``selection`` section.
        """
        if 'selection' in config.keys():
            data_store.selection = ' '.join(config['selection'])
            self.load_missing_variables(data_store.selection, dumped_tree,
                                        data_store)

    def load_missing_variables(self, expr, dumped_tree, data_store):
        """
        Load missing variables required for calculation or comparison, provided
        that the variables are available directly in the n-tuple.
        """
        variables = find_all_vars(expr)
        for v in variables:
            if v not in data_store.loaded_variables:
                try:
                    self.LOAD(v, dumped_tree, data_store)
                except Exception:
                    print('WARNING: {} is not a known branch name.'.format(v))

    @staticmethod
    def match(patterns, string, return_value=True):
        """
        Test if ``string`` (a regular expression) matches at least one element
        in the ``patterns``. If there's a match, return ``return_value``.
        """
        for p in patterns:
            if bool(re.search(r'{}'.format(p), string)):
                return return_value
        return not return_value

    @staticmethod
    def LOAD(name, dumped_tree, data_store):
        """
        Load variable ``name`` from n-tuple, if it's available.
        """
        try:
            datatype = dumped_tree[name]
            data_store.append_input_br(
                Variable(datatype, name))
        except KeyError:
            raise KeyError('Branch {} not found.'.format(name))


#############
# BabyMaker #
#############

class BabyMaker(BaseMaker):
    """
    ``babymaker`` class to glue parser and code generator together.
    """
    def __init__(self, config_filename, ntuple_filename, use_reformater=True):
        """
        Initialize with path to YAML file and n-tuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.use_reformater = use_reformater

    def gen(self, filename, **kwargs):
        parsed_config = self.read(self.config_filename)
        dumped_ntuple = self.dump(self.ntuple_filename)
        parser = self.parse_config(parsed_config, dumped_ntuple)
        generator = BabyCppGenerator(parser.instructions,
                                     parser.system_headers,
                                     parser.user_headers,
                                     **kwargs)
        content = generator.gen()

        with open(filename, 'w') as f:
            f.write(content)
        if self.use_reformater:
            self.reformat(filename)

    def parse_config(self, parsed_config, dumped_ntuple):
        parser = BaseConfigParser(parsed_config, dumped_ntuple)
        parser.parse()
        return parser
