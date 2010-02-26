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
Software specific to printing to a vinyl cutter.
"""

###############################################################################
## Imports
###############################################################################

import os
import sys
import traceback

import log
from job import Job
from vector import Vector


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################


###############################################################################
## Functions
###############################################################################

def main():
    """
    Main entry of vinyl cutter program.
    """
    try:
        if len(sys.argv) == 1:
            device_class = "direct"
            device_uri = os.path.basename(sys.argv[0])
            device_make_and_model = "Unknown"
            device_info = "Vinyl Cutter (thin red lines vector cut)"
            print "%s %s \"%s\" \"%s\"\n" % (device_class,
                                             device_uri,
                                             device_make_and_model,
                                             device_info)
            sys.exit(1)

        job = Job(sys.argv)
        printer = Vector(os.getenv('DEVICE_URI'))
        printer.run(job)
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        log.crit("Unexpected failure %s." % e)
        sys.exit(1)


