#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 29, 2020 at 05:52 PM +0800

import re


class Identifier(object):
    def __init__(self, pattern, groups, strip_policy):
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
        return self.strip_whitespaces(self.regex.search(string))

    def match(self, string):
        return self.strip_whitespaces(self.regex.match(string))

    def strip_whitespaces(self, match):
        if match is not None:
            return [match.group(i).strip() if self.strip_policy[i] else
                    match.group(i)
                    for i in range(self.groups+1)]

        else:
            return False


full_line_id = Identifier(r'^(\s*)//\s*\{%\s*(.*)%\}\s*$', 2, [False, True])
inline_id = Identifier(r'^(.*)/\*\s*\{%\s*(.*)%\}\s*\*/(.*)$', 3,
                       [False, True, False])
