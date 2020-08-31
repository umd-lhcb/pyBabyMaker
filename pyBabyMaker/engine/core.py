#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Tue Sep 01, 2020 at 03:17 AM +0800
"""
This module glues all submodules in ``engine`` together to parse and evaluate
template macros in a C++ file.
"""

from .identifiers import full_line_id, inline_id
from .eval import DelayedEvaluator, TransForTemplateMacro
from .syntax import template_macro_parser


def template_transformer(file_content, directive):
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
            pass
        else:  # Line without any template macro
            scope[-1].append(DelayedEvaluator('identity', (line,)))

    return parsed


def template_evaluator(parsed):
    """
    Trivial function to evaluate all transformed evaluator.

    :param list parsed: list of transformed evaluators.
    """
    return [eva.eval() for eva in parsed]
