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

import os
import re
import serial
import socket
import sys
from cStringIO import StringIO

import log
import pstoedit
import utils
from config import config


###############################################################################
## Constants
###############################################################################

BOUNDING_BOX_PS="/==={(        )cvs print}def/stroke{currentrgbcolor 0.0 \
eq exch 0.0 eq and exch 0.0 ne and{(P)=== currentrgbcolor pop pop 100 mul \
round  cvi = flattenpath{transform(M)=== round cvi ===(,)=== round cvi \
=}{transform(L)=== round cvi ===(,)=== round cvi =}{}{(C)=}pathforall \
newpath}{stroke}ifelse}bind def/showpage{(X)= showpage}bind def\n"


###############################################################################
## Classes
###############################################################################

class Device(object):

    def __init__(self, device_uri):
        log.info('Parsing device options.')
        match = re.search('([A-Za-z\-0-9]+)://([A-Za-z\-0-9.]+)/(.*)', device_uri)
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
            if self.port == None:
                log.debug("Port information not provided in device name.")
                log.debug("Setting socket port to default %d." % config.socket_port)
                self.port = config.socket_port
        else:
            log.crit("Device named %s is neither serial not host." % self.name)
            sys.exit(1)

        match = re.search('([A-Za-z\-0-9]+)://([A-Za-z\-0-9.]+)/(.*)', device_uri)
        settings = match.group(3).split('/')
        self.options = {}
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

    def get_option(self, keys, default=None):
        """
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
            log.crit("Could not send data to device as it is neither a host or serial.")
            sys.exit(1)

    def send_network(self, data):
        """
        Send data to the printer over the network.
        """
        log.info("Sending data via network to %s." % self.name)
        # Open the socket
        sock = socket.create_connection((self.host, self.port), config.socket_timeout)
        # Send HPGL commands to the socket
        sock.sendall(data)
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

    def run(self, job):
        log.info("Start printing job %s." % job)

        if config.debug:
            # Debug is enabled so output cups input file information
            out_filename = config.tmp_dir+"%s_%s_%s.cups" % (os.getenv('PRINTER'),
                                                             job.number,
                                                             os.getpid())
            out_file = open(out_filename, 'w')
            os.fchmod(out_file.fileno(), 0666)
            log.debug("Debug enabled so dumping input from cups to file %s." % out_file.name)
            job.file.seek(0)
            out_file.write(job.file.read())
            out_file.close()
            job.file.seek(0)

class Vector(Device):

    def __init__(self, device_uri):
        super(Vector, self).__init__(device_uri)

    def run(self, job):
        super(Vector, self).run(job)

        # Generate HPGL text
        log.info('Generating HPGL information from input file.')
        hpgl = pstoedit.execute(job.file)
        if hpgl.strip() == '':
            # No HPGL text generated error and quit.
            log.crit('No vector information found in input file from cups.')
            sys.exit(1)

        if config.debug:
            # Debug is enabled so dump hpgl to filesystem.
            out_filename = config.tmp_dir+"%s_%s_%s.hpgl" % (os.getenv('PRINTER'),
                                                             job.number,
                                                             os.getpid())
            out_file = open(out_filename, 'w')
            os.fchmod(out_file.fileno(), 0666)
            out_file.write(hpgl)
            out_file.close()

        # Close the job's file as its no longer needed.
        job.file.close()

        # Send data to the device.
        self.send(hpgl)

        # Successfully completed printed job.
        log.info("Job %s printed." % job)

class RasterVector(Device):

    def __init__(self, device_uri):
        super(RasterVector, self).__init__(device_uri)

        self.flip = False
        self.raster_mode = 'grey'
        self.raster_power = 40
        self.raster_repeat = 0
        self.raster_speed = 100
        self.resolution = 600
        self.screen = 8
        self.vector_frequency = 500
        self.vector_power = 50
        self.vector_speed = 30

        self.width = 1728
        self.height = 864


    def image_to_pcl(image):
        """
        """
        # Gather width and height information for image.
        width, height = image.size

        if mode in ['gray', 'mono'] and image.mode != 'L':
            # Image must be converted to grayscale.
            image = image.convert('L')

        # Convert PIL image to numpy array.
        pixels = numpy.asarray(image)
        # Find position(s) of non-white portions on the raster.
        xpos, ypos = numpy.where( pixels < 255 )

        # Iterate over rows outputting PCL.
        for y in ypos:
            pass

    def vector_to_hpgl(self, vector):
        """
        """
        hpgl = StringIO()

        # Send the initial HPGL sequence
        hpgl.write('IN;')
        hpgl.write("XR%04d;" % self.vector_frequency)
        hpgl.write("YP%03d;" % self.vector_power)
        hpgl.write("ZS%03d;" % self.vector_speed)

        # Iterate over the ghostscript outputted vector lines
        for line in vector.readlines():
            # The following are ordered in likelihood of their appearing in the
            # file.
            if line[0] == 'L':
                match = re.match("^L(\d+),(\d+)$", line)
                x = match.groups()[0]
                y = match.groups()[1]
                hpgl.write("PD%s,%s;" % (x,y))
            elif line[0] == 'M':
                match = re.match("^M(\d+),(\d+)$", line)
                x = match.groups()[0]
                y = match.groups()[1]
                hpgl.write("PU%s,%s;" % (x,y))
            elif line[0] == 'C':
                #hpgl.write(",%d,%d"
                pass
            elif line[0] == 'P':
                pass
            elif line[0] == 'X':
                pass
        return hpgl

    def raster_to_pcl(self, image):
        """
        """
        pcl = StringIO()

        # Gather width and height information for image.
        width, height = image.size

        if mode in ['gray', 'mono'] and image.mode != 'L':
            # Image must be converted to grayscale.
            image = image.convert('L')

        # Convert PIL image to numpy array.
        pixels = numpy.asarray(image)
        # Find position(s) of non-white portions on the raster.
        xpos, ypos = numpy.where( pixels < 255 )

        # Print the PCL header
        pcl.write(ESCAPE + "*rOF")
        pcl.write(ESCAPE + "&y%dP" % self.raster_power)
        # Raster speed
        pcl.write(ESCAPE + "&z%dS" % self.raster_speed)
        pcl.write(ESCAPE + "*r%dT" % height)
        pcl.write(ESCAPE + "*r%dS" % width)
        # Raster compression which determines how printer decodes binary data
        # in the transfer raster data command.
        # 0 = unencoded
        # 1 = run-length encoded
        # 2 = TIFF revision 4.0
        # 3 = Delta row
        # 5 = Adaptive compression
        # 9 = Replacement delta row
        pcl.write(ESCAPE + "*b0M")
        # Raster direction
        pcl.write(ESCAPE + "&y10")
        # Start at current position
        pcl.write(ESCAPE + "*r1A")

        for repeat in range(0, self.raster_repeat):
            pcl.write(ESCAPE + "*p%dY" % 0)
            pcl.write(ESCAPE + "*p%dX" % 0)
            pass

    def ps_to_eps(self, in_file):
        """
        Convert a postscript file to an EPS file. This function adds additional
        information after the PageBoundingBox entry. It also makes adjustment
        to the postscript if the raster_mode is mono AND (screen mode is a
        value other than 0 OR resolution is higher than 600)
        """
        out = StringIO()
        for line in in_file.readlines():
            out.write(line)
            if line.startswith('%%PageBoundingBox:'):
                match = re.search("%%PageBoundingBox: (\d+) (\d+) (\d+) (\d+)", line)
                groups = match.groups(1)
                lower_left_x = int(groups[0])
                lower_left_y = int(groups[1])
                upper_right_x = int(groups[2])
                upper_right_y = int(groups[3])

                xoffset = lower_left_x
                yoffset = lower_left_y
                width = upper_right_x - lower_left_x
                height = upper_right_y - lower_left_y

                out.write('/setpagedevice{pop}def\n')

                # Bugfix for document sent rotated from say Inkscape/Cairo
                if self.bed_width == height and self.bed_height == width:
                    # We have a rotated document because the incoming
                    # postscript height is set to what we would expect the
                    # bed_width to be..
                    out.write("-90 rotate")
                    tmp = width
                    width = height
                    height = tmp

                # Bugfix for situation where x,y offset is non 0
                if xoffset or yoffset:
                    out.write("%d %d translate\n", -xoffset, -yoffset)

                # Adjust for situation where user wants flip.
                if self.flip:
                    out.write("%d 0 translate -1 1 scale\n" % width)

            elif line.startswith('%!'):
                out.write(BOUNDING_BOX_PS)
                if self.raster_mode == 'mono':
                    if screen == 0:
                        out.write('{0.5 ge{1}{0}ifelse}settransfer\n')
                    else:
                        if self.resolution >= 600:
                            # Adjust for overprint
                            out.write("{dup 0 ne{%d %d div add}if}settransfer\n" % self.resolution / 600, self.screen)
                        # Setup the mono raster screen mode.
                        out.write("%d " % self.resolution / self.screen)
                        if screen > 0:
                            out.write("30{pop abs 1 exch sub}setscreen\n")
                        else:
                            out.write("30{180 mul cos exch 180 mul cos add 2 div}setscreen\n")
        out.seek(0)
        return out

    def run(self, job):
        super(RasterVector, self).run(job)

