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
Global configuration for the cups_fab software.
"""

###############################################################################
## Classes
###############################################################################

class Config(object):

    def __init__(self):

        # Debug state
        self.debug = True

        # Device filesystem path.
        self.device_dir = '/dev/'

        # Serial baud rate.
        self.serial_baud = '9600'
        # Timeout for serial connections in seconds
        self.serial_timeout = 2
        # Serial hardware flow control.
        self.serial_hardware_flow = True

        # Socket default port
        self.socket_port = 6001
        # Socket test timeout
        self.socket_test_timeout = 20
        # Socket timeout for connection in seconds
        self.socket_timeout = 60

        # Xscale and Yscale factors
        self.xscale = 1.416666
        self.yscale = 1.416666

        # pstoedit related settings
        self.pstoedit = '/usr/bin/pstoedit'
        self.pstoedit_format = 'hpgl:-pen'

        # ghostscript related settings
        self.gs = '/usr/bin/gs'

        # Location for temporary files
        self.tmp_dir = '/tmp/'


###############################################################################
## Statements
###############################################################################

config = Config()

