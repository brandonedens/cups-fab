# Brandon Edens
# 2010-02-15
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
File that defines functionality specific to laser cutters. This file builds off
of the generic device RasterVector().
"""

###############################################################################
## Imports
###############################################################################

import os
import sys
import traceback
from cStringIO import StringIO

import ghostscript
import log

from raster_vector import RasterVector
from job import Job
from postscript import ps_to_eps
from utils import units_to_pts


###############################################################################
## Constants
###############################################################################

# The escape character.
ESCAPE = "\e"


###############################################################################
## Classes
###############################################################################

class Laser(RasterVector):
    """
    Generic laser cutter.
    """

    def __init__(self, device_uri):
        """
        Initialize the laser cutter device.
        """
        super(Laser, self).__init__(device_uri)

        # Setup laser cutter specific cups settings.
        self.device_make_and_model = "Generic Laser Cutter"
        self.device_info = "Laser Cutter (thin red lines vector cut)"

        # Whether or not to auto-focus the laser.
        self.auto_focus = self.get_option(['af', 'auto-focus'], default=True)

        # Whether or not to flip raster output along x-axis
        self.flip = self.get_option(['f', 'flip'], default=False)

        # Default mode for procecssing raster engraving (varying power
        # depending upon image characteristics)
        # Values are one of:
        # color = color determines power level
        # grey = grey-scale levels determine power level
        # mono = mono with half-toning
        # none = no rasterizatino
        self.raster_mode = self.get_option(['rm', 'raster-mode'],
                                           default='grey')

        # Default raster power level (0-100)
        self.raster_power = self.get_option(['rp', 'raster-power'],
                                            default=40)
        # Default on whether to repeat the raster stage. This is the
        # number of times to raster the same image.
        self.raster_repeat = self.get_option(['rr', 'raster-repeat'],
                                             default=0)
        # Default raster speed (0-100)
        self.raster_speed = self.get_option(['rs', 'raster-speed'],
                                            default=100)

        # Default resolution in dots per inch (DPI)
        # 75 - 1200 dpi
        self.resolution = self.get_option(['r', 'resolution'],
                                          default=600)

        # Default raster halftone screen (the size of halftone blocks)
        # Another interesting value is -6
        self.raster_halftone_screen = self.get_option(['s', 'screen'],
                                                      default=8)

        # Default vectory frequency (in Hz) or the number of times
        # that the laser turns on per a second
        # 500 or 5000 are quite common
        self.vector_frequency = self.get_option(['vf', 'vector-frequency'],
                                                default=500)
        # Default vector power (0-100)
        self.vector_power = self.get_option(['vp', 'vector-power'],
                                            default=50)
        # Default vector speed (0-100)
        self.vector_speed = self.get_option(['vs', 'vector-speed'],
                                            default=30)

        # Bed width in pts
        self.width = units_to_pts(self.get_option(['w', 'width'],
                                                  default=1728))
        # Bed height in pts
        self.height = units_to_pts(self.get_option(['h', 'height'],
                                                   default=864))

        # Additional offset for the x-axis
        self.offset_x = 0
        self.offset_y = 0

    def hpgl_pcl_to_pjl(self, job, hpgl, pcl):
        """
        Convert HPGL+PCL data to printer job language (pjl).

        The parameter job is the print job currently being executed.
        hpgl is the hpgl data to send.
        pcl is the pcl data to send.
        """
        pjl = StringIO()

        # Print the printer job language header.
        pjl.write(ESCAPE + "%%-12345X@PJL JOB NAME=%s\r\n" % job.job_title)
        pjl.write(ESCAPE + "E@PJL ENTER LANGUAGE=PCL\r\n")
        # Set autofocus on or off.
        pjl.write(ESCAPE + "&y%dA" % self.auto_focus)
        # Left (long-edge) offset registration. Adjusts the position of the
        # logical page across the width of the page.
        pjl.write(ESCAPE + "&l0U")
        # Top (short-edge) offset registration. Adjusts the position of the
        # logical page across the length of the page.
        pjl.write(ESCAPE + "&l0Z")
        # Resolution of the print.
        pjl.write(ESCAPE + "&u%dD" % self.resolution)
        # X position = 0
        pjl.write(ESCAPE + "*p0X")
        # Y position = 0
        pjl.write(ESCAPE + "*p0Y")
        # PCL resolution
        pjl.write(ESCAPE + "*t%dR" % self.resolution)

        # If raster power is enabled and raster mode is not 'n' then add that
        # information to the print job.
        if self.raster_power and self.raster_mode != 'n':
            # Unknown purposes.
            pjl.write(ESCAPE + "&y0C")
            # Send the pcl information.
            pjl.write(pcl.read())

        # If vector power is > 0 then add vector information to the print job.
        if self.vector_power > 0:
            pjl.write(ESCAPE + "E@PJL ENTER LANGUAGE=PCL\r\n")
            # Page orientation
            pjl.write(ESCAPE + "*r0F")
            # XXX fixme this needs better porting
            #pjl.write(ESCAPE + "*r%dT" % (self.height * y_repeat))
            #pjl.write(ESCAPE + "*r%dS" % (self.width * x_repeat))
            pjl.write(ESCAPE + "*r1A")
            pjl.write(ESCAPE + "*rC")
            pjl.write(ESCAPE + "%%1B")
            # Send the vector information.
            pjl.write(hpgl.read())

        # Footer for print job language.
        pjl.write(ESCAPE + "F")
        pjl.write(ESCAPE + "%%-12345X")
        pjl.write("@PJL EOJ \r\n")

        # Pad out the remainder of the file with 0 characters.
        for i in xrange(0, 4096):
            pjl.write(0)

        pjl.seek(0)
        return pjl

    def run(self, job):
        """
        Execute the process of sending a job to the laser cutter.
        """
        super(Laser, self).run(job)

        # Convert postscript to eps.
        log.info('Converting input postscript to EPS.')
        eps = ps_to_eps(job.file)

        # run ghostscript on eps
        log.info('Running ghostscript on eps file.')
        (raster, vector) = ghostscript.execute(
            eps, self.resolution,
            self.width, self.height,
            ghostscript.raster_mode_to_ghostscript(self.raster_mode))

        # convert image data to pcl
        log.info('Converting image data to PCL.')
        pcl = self.raster_to_pcl(raster)

        # convert vector data to hpgl
        log.info('Converting ghostscript vector data to HPGL')
        hpgl = self.vector_to_hpgl(vector)

        # send to printer
        log.info('Sending data to printer.')
        self.send(self.hpgl_pcl_to_pjl(job, hpgl, pcl))

        # Successfully completed printing job.
        log.info("Job %s printed." % job)


def main():
    """
    Main entry for laser cutter program.
    """
    try:
        job = Job(sys.argv)
        printer = Laser(os.getenv('DEVICE_URI'))

        if len(sys.argv) == 1:
            # Set the device uri to the script name.
            printer.device_uri = os.path.basename(sys.argv[0])
            print printer
            sys.exit(1)

        printer.run(job)
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        log.crit("Unexpected failure %s." % e)
        sys.exit(1)

