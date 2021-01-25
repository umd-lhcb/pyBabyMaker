#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jan 25, 2021 at 04:41 AM +0100
"""
This module glues all submodules in ``engine`` together to parse and evaluate
template macros in a C++ file.
"""

from .identifiers import full_line_id, inline_id
from .eval import DelayedEvaluator
from .eval import TransForTemplateMacro
from .eval import Scope
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
    transformer = TransForTemplateMacro(Scope(), {'directive': directive})

    for lineno, line in enumerate(file_content, 1):
        for pattern in [full_line_id, inline_id]:
            match = pattern.search(line)
            if match:
                break

        if match:
            macro = template_macro_parser.parse(match[pattern.macro_idx])
            exe = transformer.transform(macro, lineno=lineno)

            if exe is False:
                pass

            elif isinstance(exe, DelayedEvaluator):
                transformer.scope.append(DelayedEvaluator(
                    'format', ('{}'*pattern.groups+eol, *helper_eval_args(
                        match, pattern, exe))))

            else:
                transformer.scope.parent.append(exe)

        else:  # Line without any template macro
            transformer.scope.append(DelayedEvaluator('identity', (line,)))

    if do_check:
        error = ''
        while transformer.scope.parent is not None:
            error += 'Unclosed {} statement\n'.format(
                transformer.scope.evaluator.name)
            transformer.scope = transformer.scope.parent
        if len(error) > 0:
            raise ValueError(error)

    return transformer.scope


def template_evaluator(parsed):
    """
    Trivial function to evaluate all transformed evaluator.

    :param list parsed: list of transformed evaluators.
    """
    return helper_flatten([eva.eval() for eva in parsed])
