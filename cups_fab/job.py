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
"""

###############################################################################
## Imports
###############################################################################

import sys
from cStringIO import StringIO

import log
from config import config


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
            if config.debug:
                log.debug('Loading cups data via stdin and creating StringIO to hold file text.')
                self.file = StringIO()
                self.file.write(sys.stdin.read())
                self.file.seek(0)
            else:
                self.file = sys.stdin
                log.debug('Cups did not specify input filename. Using stdin.')

    def __str__(self):
        return "number %s named %s for user %s" % (self.number, self.title, self.user)


###############################################################################
## Functions
###############################################################################


