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
Utilities for cups_fab. This consists of short functions that accomplish small
tasks ranging from checking serial connections, host connections to converting
a string representation of some length to a length in postscript points.
"""

###############################################################################
## Imports
###############################################################################

import os
import re
import socket
import stat

import log


###############################################################################
## Constants
###############################################################################

# Number of pts per an inch.
PTS_PER_INCH = 72

# Number of pts per a foot.
PTS_PER_INCH = 864

# Number of pts per a cm.
PTS_PER_CM = 28.3464567

# Number of pts per a mm
PTS_PER_MM = 2.83464567

# Number of pts oer a meter
PTS_PER_METER = 2834.64567


###############################################################################
## Functions
###############################################################################

def is_host(device_name):
    """
    Check whether or not device is a host. Return true if it is a host, false
    otherwise.
    """
    host, port = hostname_port(device_name)
    if host:
        return host_exists(host, port)
    return False

def is_serial_port(filename):
    """
    Given a filename check if the given device is a serial port in the device
    filesystem and that the given device is a character device (requirement for
    serial ports). Return True for success, false otherwise.
    """
    # Create complete serial port name.
    log.debug("Attempting to check existence of serial port at %s." % filename)
    # Check to make sure the serial port is a character device
    try:
        mode = os.stat(filename)[stat.ST_MODE]
        if stat.S_ISCHR(mode):
            # We have a character device, return true.
            return True
        # The device name is not a valid serial port.
        return False
    except OSError:
        # File did not exist so obviously its not a serial port.
        return False

def host_exists(host, port):
    """
    Determine whether or not the given host exists. Return true if hosts
    exists, false otherwise.
    """
    # Try to resolve the hostname
    try:
        socket.getaddrinfo(host, port)
    except socket.gaierror:
        return False
    return True

def hostname_port(device_name):
    """
    Given a device_name return a tuple containing hostname/ip_address and any
    port information. Finding that the device_name matches neither return None.
    """
    # Check for IP_address:port
    pattern = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})"
    match = re.search(pattern, device_name)
    if match:
        # We have an IP address / port pair
        return (match.group(1), match.group(2))

    # Check for IP address
    pattern = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    match = re.search(pattern, device_name)
    if match:
        # We have a solitary IP address
        return (match.group(1), None)

    # Check for hostname:port
    pattern = "([\w\-\.]+):(\d{1,5})"
    match = re.search(pattern, device_name)
    if match:
        # We have hostname:port pair
        return (match.group(1), match.group(2))

    # Check for hostname alone.
    pattern = "([\w\-\.]+)"
    match = re.search(pattern, device_name)
    if match:
        # We have a single hostanme
        return (match.group(1), None)

def units_to_pts(units):
    """
    Given a units string definition of the form 23pts or 23ins; convert that string to pts.
    This function accepts:
    mm
    cm
    in
    pts
    dpi
    """
    try:
        match = re.search("([\d\.]+) *(in|pt|mm|cm|ft|m)s?", units.lower())
        if match:
            if match.group(2) == "in":
                return int(float(match.group(1)) * PTS_PER_INCH)
            elif match.group(2) == 'cm':
                return int(float(match.group(1)) * PTS_PER_CM)
            elif match.group(2) == 'mm':
                return int(float(match.group(1)) * PTS_PER_MM)
            elif match.group(2) == 'm':
                return int(float(match.group(1)) * PTS_PER_METER)
            elif match.group(2) == 'pt':
                return int(match.group(1))
    except AttributeError:
        return units

