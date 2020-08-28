#!/usr/bin/env python3
#
# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri Aug 28, 2020 at 07:15 PM +0800

import re

full_line_id = re.compile(r'^(\s*)//\s*\{% (.*) %\}$')
