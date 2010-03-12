# Brandon Edens
# 2010-03-01
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
Software that provides pdf information and functionality. These are wrappers
around the utilities pdftk and pdfinfo.
"""

###############################################################################
## Imports
###############################################################################

import re
import subprocess
import sys
import tempfile
from cStringIO import StringIO

import log
from config import config


###############################################################################
## Functions
###############################################################################

def rotate(pdf_file):
    """
    Execute the pdftk command to rotate the document returning the rotated
    document in a buffer.
    """
    args = [config.pdftk,
            "-",
            "cat",
            "endE",
            "output",
            "-",
            ]

    log.debug("Executing pdftk process with args: %s" % args)
    process = subprocess.Popen(args, cwd=config.tmp_dir,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate(pdf_file.read())
    process.wait()

    if process.returncode != 0:
        log.crit("pdftk failed during execution with returncode = %s."
                 % process.returncode)
        sys.exit(1)
    else:
        # Collect the outputted text.
        rotated_pdf = StringIO(stdoutdata)
        # Return the text.
        return rotated_pdf

def page_size(pdf_file):
    """
    Discover page size of a pdf document through the usage of the pdfinfo
    external command.

    Note that this functionality will not work properly with Python StringIO
    buffers as they do not have proper file handles so instead we utilize a
    named tempfile.
    """

    # Create the tmp file.
    tmp_file = tempfile.NamedTemporaryFile()
    # Write pdf contents to tmp_file
    tmp_file.write(pdf_file.read())
    # Rewind pdf_file and tmp_file.
    pdf_file.seek(0)
    tmp_file.seek(0)

    args = [config.pdfinfo,
            tmp_file.name,
            ]
    log.debug("Executing pdfinfo process with args: %s." % args)
    process = subprocess.Popen(args, cwd=config.tmp_dir,
                               stdout=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate()
    process.wait()
    tmp_file.close()

    if process.returncode != 0:
        log.crit("pdfinfo failed during execution with returncode = %s."
                 % process.returncode)
        sys.exit(1)
    else:
        width = None
        height = None
        buf = StringIO(stdoutdata)
        # Get the page size from the stdout data.
        for line in buf.readlines():
            if line.startswith('Page size:'):
                match = re.search('^Page size: +(\d+) x (\d+) pts', line)
                groups = match.groups()
                width = int(groups[0])
                height = int(groups[1])
        return (width, height)

def to_ps(pdf_file):
    """
    Convert a pdf file to a postscript file.
    """
    args = [config.pdf2ps,
            "-",
            "-",
            ]
    log.debug("Executing pdf2ps to convert pdf to ps with args: %s." % args)
    process = subprocess.Popen(args, cwd=config.tmp_dir,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (stdoutdata, stderrdata) = process.communicate(pdf_file.read())
    process.wait()

    if process.returncode != 0:
        log.crit("pdf2ps failed during execution with returncode = %s."
                 % process.returncode)
        sys.exit(1)
    else:
        # Collect the outputted text.
        ps_file = StringIO(stdoutdata)
        # Return the text.
        return ps_file

