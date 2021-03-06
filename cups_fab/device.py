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
File defines the base class for all of the cups fab devices. This device knows
how to send data to either a serial port or network socket along with knowing
how to process cups queue options and the basics of running cups jobs.
"""

###############################################################################
## Imports
###############################################################################

import os
import re
import serial
import socket
import sys

import log
import utils
from config import config


###############################################################################
## Classes
###############################################################################

class Device(object):

    def __init__(self):
        self.device_class = "direct"
        self.device_uri = "device"
        self.device_make_and_model = "Unknown"
        self.device_info = "Generic device that does nothing"

        # Set debugging default to whatever configuration specified.
        self.debug = config.debug

    def parse_device_uri(self, device_uri):
        """
        Parse the device_uri options.
        """
        log.info('Parsing device options.')
        match = re.search('([A-Za-z\-0-9]+)://([A-Za-z\-0-9\.:]+)/(.*?)',
                          device_uri)
        if not match:
            log.crit("Could not parse the device settings specified by cups.")
            sys.exit(1)

        # First parameter is the backend name.
        self.backend = match.group(1)
        # Second parameter is the name of either the serial or network device
        # to use.
        self.name = match.group(2)

        # Setup variables for serial, host, and port.
        self.serial = None
        self.host = None
        self.port = None

        # Check to see if device is a serial port
        filename = config.device_dir + self.name
        if utils.is_serial_port(filename):
            self.serial = filename
        elif utils.is_host(self.name):
            self.host, self.port = utils.hostname_port(self.name)
            if not self.port:
                log.debug("Port information not provided in device name.")
                log.debug("Setting socket port to default %d."
                          % config.socket_port)
                self.port = config.socket_port
        else:
            log.crit("Device named %s is neither serial not host." % self.name)
            sys.exit(1)

        match = re.search('([A-Za-z\-0-9]+)://([A-Za-z\-0-9.]+)/(.*)',
                          device_uri)
        self.options = {}
        try:
            settings = match.group(3).split('/')
            for option in settings:
                if option:
                    (key, value) = option.split('=')
                    value = value.lower()
                    # Handle values that are booleans.
                    if value in ['1', 't', 'true']:
                        self.options[key] = True
                        continue
                    elif value in ['0', 'f', 'false']:
                        self.options[key] = False
                        continue
                    # Handle values that are integers.
                    try:
                        self.options[key] = int(value)
                        continue
                    except ValueError:
                        pass
                    # Handle values all other values.
                    self.options[key] = value
        except AttributeError:
            pass

    def __str__(self):
        return "%s %s \"%s\" \"%s\"" % (self.device_class,
                                        self.device_uri,
                                        self.device_make_and_model,
                                        self.device_info)

    def get_option(self, keys, default=None):
        """
        Given a set of possible keys, return a possible option that corresponds
        to that key. If no option value is found for those keys then return the
        default if provided.
        """
        value = None
        for key in keys:
            try:
                value = self.options[key]
                break
            except KeyError:
                pass
        if value != None:
            return value
        elif default:
            return default
        else:
            return None

    def send(self, data):
        """
        Send data to the printer. This dispatches data over the network or over
        a serial port depending upon the device uri.
        """
        if self.host:
            self.send_network(data)
        elif self.serial:
            self.send_serial(data)
        else:
            log.crit("Failed to send data to device.")
            log.crit("Device specified is attached via network or serial.")
            sys.exit(1)

    def send_network(self, data):
        """
        Send data to the printer over the network.
        """
        log.info("Sending data via network to %s." % self.name)
        # Open the socket
        sock = socket.create_connection((self.host, self.port),
                                        config.socket_timeout)
        # Send data to the socket
        try:
            sock.sendall(data)
        except TypeError:
            # We likely have a StringIO to send to the socket
            sock.sendall(data.read())

        # Close up the socket
        sock.close()

    def send_serial(self, data):
        """
        Send data to the printer over the serial port.
        """
        log.info("Sending data via serial to %s." % self.name)
        # Open the serial port
        # by default:
        #  ser.xonxoff = False
        #  ser.rtscts = False
        ser = serial.Serial(self.serial,
                            config.serial_baud,
                            timeout=config.serial_timeout,
                            rtscts=config.serial_hardware_flow)
        # Flush output (removing any initial contents)
        ser.flushOutput()
        # Write data to the serial port
        ser.write(data)
        # Close the serial port
        ser.close()

    def debug_basename(self, job):
        """
        Return the debug file basename for this printer/job.
        """
        return "%s_%s_%s" % (os.getenv('PRINTER'),
                             job.number,
                             os.getpid())

    def debug_write(self, filename, buffer):
        """
        Write the given buffer contents to the given filename.
        """
        out_filename = config.tmp_dir + filename
        out_file = open(out_filename, 'w+b')
        os.fchmod(out_file.fileno(), 0666)
        log.debug("Debug enabled so writing file %s." % filename)
        buffer.seek(0)
        out_file.write(buffer.read())
        # Close the output file.
        out_file.close()
        # Rewind the buffer for the next person.
        buffer.seek(0)

    def run(self, job):
        log.info("Start printing job %s." % job)

        if self.debug:
            # Debug is enabled so output cups input file information
            out_filename = "%s.cups" % self.debug_basename(job)
            self.debug_write(out_filename, job.file)

