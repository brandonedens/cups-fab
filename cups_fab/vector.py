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
File that houses the Vector class which defines a device that is used to
produce vector cutting.
"""

###############################################################################
## Imports
###############################################################################

import os
import sys

import log
import pstoedit
from config import config
from device import Device


###############################################################################
## Classes
###############################################################################

class Vector(Device):

    def __init__(self):
        super(Vector, self).__init__()

    def parse_device_uri(self, device_uri):
        super(Vector, self).parse_device_uri(device_uri)

    def run(self, job):
        super(Vector, self).run(job)

        # Generate HPGL text
        log.info('Generating HPGL information from input file.')
        hpgl = pstoedit.execute(job.file)
        if hpgl.strip() == '':
            # No HPGL text generated error and quit.
            log.crit('No vector information found in input file from cups.')
            sys.exit(1)

        if config.debug:
            # Debug is enabled so dump hpgl to filesystem.
            hpgl_file = "%s_%s_%s.hpgl" % (os.getenv('PRINTER'),
                                           job.number,
                                           os.getpid())
            out_filename = config.tmp_dir + hpgl_file
            out_file = open(out_filename, 'w')
            os.fchmod(out_file.fileno(), 0666)
            out_file.write(hpgl)
            out_file.close()

        # Close the job's file as its no longer needed.
        job.file.close()

        # Send data to the device.
        self.send(hpgl)

        # Successfully completed printed job.
        log.info("Job %s printed." % job)



