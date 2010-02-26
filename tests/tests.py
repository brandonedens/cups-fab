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
Unit testing files.
"""

###############################################################################
## Imports
###############################################################################

import sys
import tempfile
import unittest

from cups_fab.job import Job


###############################################################################
## Constants
###############################################################################


###############################################################################
## Classes
###############################################################################

class GhostscriptTest(unittest.TestCase):
    def setUp(self):
        pass

class JobTest(unittest.TestCase):

    def setUp(self):
        pass

    def testInit(self):
        """Test that job loads argv arguments."""
        argv = ["executable", "123", "jdoe", "example.ps", "1", "options"]
        job = Job(argv)
        self.assertEqual(job.number, '123')
        self.assertEqual(job.user, 'jdoe')
        self.assertEqual(job.title, 'example.ps')
        self.assertEqual(job.copies, '1')
        self.assertEqual(job.file, sys.stdin)

    def testInitWithFile(self):
        """Test that job loads argv arguments with filename."""
        fake_input = tempfile.NamedTemporaryFile()
        argv = ["executable", "123", "jdoe", "example.ps", "1", "options", fake_input.name]
        job = Job(argv)
        fake_input.close()

    def testStr(self):
        """Test that job presents correct string information."""
        argv = ["executable", "123", "jdoe", "example.ps", "1", "options"]
        job = Job(argv)
        self.assertEqual(job.__str__(),
                         'number 123 named example.ps for user jdoe')




###############################################################################
## Functions
###############################################################################

if __name__ == '__main__':
    unittest.main()

