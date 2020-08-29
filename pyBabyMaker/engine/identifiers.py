#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Aug 30, 2020 at 03:32 AM +0800
"""
This module defines various identifiers to extract macros from C++ files.
"""

import re


class Identifier(object):
    """
    Abstraction of an identifiers. This class provide wrappers to ``re``
    objects.

    These wrappers will provide saner return value, and strip heading/trailing
    white spaces if configured.
    """
    def __init__(self, pattern, groups, strip_policy):
        """
        Initialize identifier.

        :param str pattern: pattern to be compiled into a ``re`` object.
        :param int: Specify number of groups in the matching regex
        :param list: A list of boolean, indicating if group(``idx+1``) should
                     be stripped. ``idx`` is the index of the boolean in this
                     list.
        """
        self.regex = re.compile(pattern)
        self.groups = groups
        self.strip_policy = [False] + strip_policy

        assert len(self.strip_policy) == self.groups+1, \
            'Mismatch: number of groups and number of strip policy!'

        self.macro_idx = None
        for i in range(len(self.strip_policy)):
            if self.strip_policy[i]:
                self.macro_idx = i

    def search(self, string):
        """
        Wrapper to ``re.search``.
        """
        return self.strip_whitespaces(self.regex.search(string))

    def match(self, string):
        """
        Wrapper to ``re.match``.
        """
        return self.strip_whitespaces(self.regex.match(string))

    def strip_whitespaces(self, match):
        """
        Strip white spaces if regular expression has a match, and the strip
        policy for a particular group is set to ``True``.
        """
        if match is not None:
            return [match.group(i).strip() if self.strip_policy[i] else
                    match.group(i)
                    for i in range(self.groups+1)]

        else:
            return False


full_line_id = Identifier(r'^(\s*)//\s*\{%\s*(.*)%\}\s*$', 2, [False, True])
inline_id = Identifier(r'^(.*)/\*\s*\{%\s*(.*)%\}\s*\*/(.*)$', 3,
                       [False, True, False])
