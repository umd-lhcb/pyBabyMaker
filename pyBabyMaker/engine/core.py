#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Thu Sep 03, 2020 at 09:40 PM +0800
"""
This module glues all submodules in ``engine`` together to parse and evaluate
template macros in a C++ file.
"""

from .identifiers import full_line_id, inline_id
from .eval import DelayedEvaluator
from .eval import TransForTemplateMacro
from .syntax import template_macro_parser


def helper_eval_args(match, pattern, evaluator):
    """
    Helper function to figure out how to put identifier groups into 'format'
    function properly.

    :param list match: regexp search groups.
    :param Identifier pattern: Identifier used for the regexp search.
    :param Any evaluator: Transformed template macro evaluator.
    """
    return [match[i] if i != pattern.macro_idx else evaluator
            for i in range(1, pattern.groups+1)]


def helper_flatten(lst, result=None):
    """
    Helper function to flatten a multi-depth list.

    :param list lst: list to be flattened.
    :param list result: (partially) flattened list. Optional
    """
    result = [] if result is None else result

    for i in lst:
        if type(i) == list:
            helper_flatten(i, result)
        else:
            result.append(i)

    return result


def template_transformer(file_content, directive, do_check=True, eol='\n'):
    """
    Transform raw template into fully working C++ code.

    :param Iterable file_content: content of the raw template.
    :param dict directive: Parsed YAML directive.
    """
    known_symb = {'directive': directive}
    parsed = []
    scope = [parsed]

    transformer = TransForTemplateMacro(scope, known_symb)

    for lineno, line in enumerate(file_content, 1):
        for pattern in [full_line_id, inline_id]:
            match = pattern.search(line)
            if match:
                break

        if match:
            macro = template_macro_parser.parse(match[pattern.macro_idx])
            eva = transformer.transform(macro, lineno=lineno)

            if type(eva) == DelayedEvaluator:
                scope[-1].append(DelayedEvaluator(
                    'format', ('{}'*pattern.groups+eol, *helper_eval_args(
                        match, pattern, eva))))

            elif type(eva) != list:
                scope[-2].append(eva)

        else:  # Line without any template macro
            scope[-1].append(DelayedEvaluator('identity', (line,)))

    if do_check:
        for stmt, counter in transformer.stmt_counters.items():
            if counter > 0:
                raise ValueError('Mismatch: statement "{}" has a non-zero counter value of {}'.format(
                    stmt, counter))

    return parsed


def template_evaluator(parsed):
    """
    Trivial function to evaluate all transformed evaluator.

    :param list parsed: list of transformed evaluators.
    """
    return helper_flatten([eva.eval() for eva in parsed])
