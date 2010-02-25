# Brandon Edens
# 2010-02-14
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

import re
import subprocess
import tempfile
from cStringIO import StringIO

import log
from config import config


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################


###############################################################################
## Functions
###############################################################################

def execute(in_file, resolution, width, height, raster_mode):
    """
    """

    raster_tmpfile = tempfile.NamedTemporaryFile()

    width = width * resolution
    height = height * resolution

    args = [config.gs,
            "-q",
            "-dBATCH",
            "-dNOPAUSE",
            "-r%s" % resolution,
            "-g%dx%d" % (width, height),
            "-sDEVICE=%s" % raster_mode,
            "-sOutputFile=%s" % raster_tmpfile.name,
            "-",
            ]
    # Execute ghostscript
    log.debug("Opening ghostscript process with args: %s" % args)
    process = subprocess.Popen(args, cwd=config.tmp_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate(in_file.read())
    log.debug("Waiting on ghostscript to terminate.")
    process.wait()

    # Check that ghostscript functioned correctly.
    if process.returncode != 0:
        log.crit("Process ghostscript failed during execution with returncode = %s."
                 % process.returncode)

    # Get raster information into a StringIO
    log.debug("Rewinding the ghostscript raster output and storing it in StringIO")
    raster_tmpfile.seek(0)
    raster = StringIO()
    raster.write(raster_tmpfile.read())
    raster.seek(0)

    # Gather the vector information into a StringIO
    log.debug("Gathering the vector output from ghostscript.")
    vector = StringIO()
    vector.write(stdoutdata)
    vector.seek(0)

    log.debug("Returning ghostscript raster and vector output.")
    return (raster, vector)

def raster_mode_to_ghostscript(mode):
    """
    Given a raster mode return the ghostscript mode.
    """
    if mode == 'mono':
        return 'pngmono'
    if mode in ['gray', 'grey']:
        return 'pnggray'
    elif mode in ['color', 'colour']:
        return 'png16m'

