#!/usr/bin/env python
# Brandon Edens
# 2010-02-26
# Copyright (C) 2010 Brandon Edens <brandon@as220.org>
#
# This file is part of cups_fab.
#
# cups_fab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cups_fab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cups_fab. If not, see <http://www.gnu.org/licenses/>.
"""
Test driver for cups_fab.

Script executes the cups_fab test suite.
"""

###############################################################################
## Imports
###############################################################################
import sys
import os

sys.path.insert(0, path.join(path.dirname(__file__), path.pardir))
try:
    import nose
except ImportError:
    print "The nose package is needed to run the cups_fab test suite."
    sys.exit(1)


###############################################################################
## Statements
###############################################################################

print "Running cups_fab test suite..."
nose.main()

