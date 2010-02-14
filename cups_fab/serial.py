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
Software for interfacing to the serial port.
"""

###############################################################################
## Imports
###############################################################################
import os
import serial
import stat


###############################################################################
## Constants
###############################################################################

# Default serial bps.
SERIAL_BAUD='9600'

# Default serial port.
SERIAL_PORT='ttyS0'

# Serial port PATH.
SERIAL_PORT_DIR="/dev/"

# Serial timeout value.
SERIAL_TIMEOUT=2

# Serial hardware flow control.
SERIAL_HARDWARE_FLOW=True


###############################################################################
## Functions
###############################################################################

def is_serial_port(device_name):
    """
    Given a device name check if the given device is a serial port in the
    device filesystem and that the given device is a character device
    (requirement for serial ports). Return True for success, false otherwise.
    """
    # Create complete serial port name.
    serial_port = SERIAL_PORT_DIR+device_name
    # Check to make sure the serial port is a character device
    try:
        mode = os.stat(serial_port)[stat.ST_MODE]
        if stat.S_ISCHR(mode):
            # We have a character device, return true.
            return True
        # The device name is not a valid serial port.
        return False
    except OSError:
        # File did not exist so obviously its not a serial port.
        return False

def serial_send(hpgl_text,
                port=SERIAL_PORT,
                baud=SERIAL_BAUD,
                timeout=SERIAL_TIMEOUT,
                hardware_flow_control=SERIAL_HARDWARE_FLOW):
    """
    Send the HPGL text to the serial port. By default the port opened is
    defined by the global SERIAL_PORT (ttyS0) at 9600 baud.
    """
    # Open the serial port
    # by default:
    #  ser.xonxoff = False
    #  ser.rtscts = False
    ser = serial.Serial(SERIAL_PORT_DIR+SERIAL_PORT, SERIAL_BAUD,
                        timeout=timeout,
                        rtscts=hardware_flow_control)
    # Flush output (removing any initial contents)
    ser.flushOutput()
    # Write contents of text to the serial port
    ser.write(text)
    # Close the serial port
    ser.close()

