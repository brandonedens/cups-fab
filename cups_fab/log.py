# Brandon Edens
# 2010-02-12
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
"""

###############################################################################
## Imports
###############################################################################
import sys


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################


###############################################################################
## Functions
###############################################################################

def crit(message):
    sys.stderr.write("CRIT: %s\n" % message)

def error(message):
    sys.stderr.write("ERROR: %s\n" % message)

def warning(message):
    sys.stderr.write("WARNING: %s\n" % message)

def info(message):
    sys.stderr.write("INFO: %s\n" % message)

def debug(message):
    sys.stderr.write("DEBUG: %s\n" % message)


