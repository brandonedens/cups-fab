# Brandon Edens
# 2010-02-13
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
Software that represents a CUPS job. This software is specific to the
DEVICE_URI environment variable that cups provides.
"""

###############################################################################
## Imports
###############################################################################

import sys
from cStringIO import StringIO

import log


##############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################

class Job(object):

    def __init__(self, argv):
        log.info('Parsing arguments for print job.')
        self.number = argv[1]
        self.user = argv[2]
        self.title = argv[3]
        self.copies = argv[4]
        self.options = argv[5]
        self.filename = ""
        self.file = None
        try:
            self.filename = argv[6]
            log.debug("Loadings cups data from file at %s." % self.filename)
            self.file = open(self.filename, 'r+b')
        except IndexError:
            log.debug('Input file not specified.')
            log.debug('Loading cups data from stdin.')
            self.file = StringIO()
            self.file.write(sys.stdin.read())

    def __str__(self):
        return "number %s named %s for user %s" % (self.number,
                                                   self.title,
                                                   self.user)

    def is_ps(self):
        """
        Return True if the beginning magick of the input file is %!PS, False
        otherwise.
        """
        label = self.file.read(4)
        self.file.seek(0)
        if label == '%!PS':
            return True
        return False

    def is_pdf(self):
        """
        Return True if the beginning magick of the input file is %PDF, False
        otherwise.
        """
        label = self.file.read(4)
        self.file.seek(0)
        if label == '%PDF':
            return True
        return False



###############################################################################
## Functions
###############################################################################


