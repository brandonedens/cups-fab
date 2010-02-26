# Brandon Edens
# 2009-12-18
# Copyright (C) 2009 Brandon Edens <brandon@as220.org>
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
Software for interacting with pstoedit an external program which converts
postscript/pdf to a vector format.
"""

###############################################################################
## Imports
###############################################################################

from cStringIO import StringIO
import log
import subprocess

from config import config


###############################################################################
## Functions
###############################################################################

def execute(in_file,
            xscale=config.xscale,
            yscale=config.yscale):
    """
    Execute pstoedit returning the generated HPGL to the calling function.
    """
    # Arguments to pass to pstoedit
    args = [config.pstoedit,
            "-f",
            config.pstoedit_format,
            "-dt", # Draw the text rather than assume cutter can handle text
            "-pta", # Precision text spacing (spaces handled gracefully)
            "-xscale",
            "%s" % xscale,
            "-yscale",
            "%s" % yscale,
            "-",
            ]

    # Execute pstoedit
    process = subprocess.Popen(args, cwd=config.tmp_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate(in_file.read())
    process.wait()

    # Check that pstoedit functioned correctly.
    if process.returncode != 0:
        log.crit("Process pstoedit failed during execution with returncode = %s."
                 % process.returncode)
        # Printing out stdout and stderr
        log.debug("Standard output for pstoedit was:")
        out = StringIO(stdoutdata)
        for line in out.readlines():
            log.debug(line)
        out = StringIO(stderrdata)
        log.debug("Standard error for pstoedit was:")
        for line in out.readlines():
            log.debug(line)
        return ""
    else:
        # Collect the outputted text.
        text = stdoutdata
        # Return the text.
        return text

