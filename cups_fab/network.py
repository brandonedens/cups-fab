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
Software for printing over a network socket.
"""

###############################################################################
## Imports
###############################################################################
import re
import socket


###############################################################################
## Constants
###############################################################################

# Default port to connect to
DEFAULT_PORT = 6001

###############################################################################
## Functions
###############################################################################

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
        return (match.group(1), DEFAULT_PORT)

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
        return (match.group(1), DEFAULT_PORT)

def is_host(device_name):
    """
    Check whether or not device is a host. Return true if it is a host, false
    otherwise.
    """
    host, port = hostname_port(device_name)
    if host:
        return True
    return False

def network_send(hpgl_text, host, port):
    """
    Send HPGL commands to the given hostname and port.
    """
    # Open the socket
    sock = socket.create_connection((host, port), SOCKET_TIMEOUT)
    # Send HPGL commands to the socket
    sock.sendall(hpgl_text)
    # Close up the socket
    sock.close()

