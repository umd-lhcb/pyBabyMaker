#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sat Aug 29, 2020 at 05:02 PM +0800

import re


class Identifier(object):
    def __init__(self, pattern, groups):
        self.regex = re.compile(pattern)
        self.groups = groups

    def search(self, string):
        return self.strip_whitespaces(self.regex.search(string), self.groups)

    def match(self, string):
        return self.strip_whitespaces(self.regex.match(string), self.groups)

    @staticmethod
    def strip_whitespaces(match, groups):
        if match is not None:
            return [match.group(i).strip() if i > 0 else match.group(i)
                    for i in range(groups+1)]

        else:
            return False


full_line_id = Identifier(r'^(\s*)//\s*\{%\s*(.*)%\}\s*$', 2)
inline_id = Identifier(r'(.*)/\*\s*\{%\s*(.*)%\}(.*)', 3)
