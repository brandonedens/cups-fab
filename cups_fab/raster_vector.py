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
File that houses the RasterVector device which is used to both vector cut and
rasterize an image.
"""

###############################################################################
## Imports
###############################################################################

import re
from cStringIO import StringIO

import numpy
from PIL import Image

from device import Device


###############################################################################
## Constants
###############################################################################


# The escape character.
ESCAPE = "\e"


###############################################################################
## Classes
###############################################################################

class RasterVector(Device):

    def __init__(self):
        super(RasterVector, self).__init__()

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

    def parse_device_uri(self, device_uri):
        super(RasterVector, self).parse_device_uri(device_uri)

    def vector_to_hpgl(self, vector):
        """
        Given vector data produced by ghostscript convert that data to HPGL.
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
                hpgl.write("PD%s,%s;" % (x, y))
            elif line[0] == 'M':
                match = re.match("^M(\d+),(\d+)$", line)
                x = match.groups()[0]
                y = match.groups()[1]
                hpgl.write("PU%s,%s;" % (x, y))
            elif line[0] == 'C':
                #hpgl.write(",%d,%d"
                pass
            elif line[0] == 'P':
                pass
            elif line[0] == 'X':
                pass

        hpgl.seek(0)
        return hpgl

    def raster_to_pcl(self, raster):
        """
        Given raster data (a png file) produced by ghostscript. Convert that
        image to PCL data.
        """
        pcl = StringIO()

        # Open the image.
        image = Image.open(raster)

        # Gather width and height information for image.
        width, height = image.size

        if self.raster_mode in ['gray', 'mono'] and image.mode != 'L':
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

        pcl.seek(0)
        return pcl

    def run(self, job):
        """
        Execute the RasterVector software which really just calls the super run
        method at this point.
        """
        super(RasterVector, self).run(job)


###############################################################################
## Functions
###############################################################################


