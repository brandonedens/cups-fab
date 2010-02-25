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
"""

###############################################################################
## Imports
###############################################################################

import re

import device
import ghostscript
import log


###############################################################################
## Classes
###############################################################################

class Laser(device.RasterVector):
    """
    Generic laser cutter.
    """

    def __init__(self, device_uri):
        """
        """
        super(Laser, self).__init__(device_uri)

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
        self.raster_mode = self.get_option(['rm', 'raster-mode'], default='grey')

        # Default raster power level (0-100)
        self.raster_power = self.get_option(['rp', 'raster-power'], default=40)
        # Default on whether to repeat the raster stage. This is the
        # number of times to raster the same image.
        self.raster_repeat = self.get_option(['rr', 'raster-repeat'], default=0)
        # Default raster speed (0-100)
        self.raster_speed = self.get_option(['rs', 'raster-speed'], default=100)

        # Default resolution in dots per inch (DPI)
        # 75 - 1200 dpi
        self.resolution = self.get_option(['r', 'resolution'], default=600)

        # Default raster halftone screen (the size of halftone blocks)
        # Another interesting value is -6
        self.raster_halftone_screen = self.get_option(['s', 'screen'], default=8)

        # Default vectory frequency (in Hz) or the number of times
        # that the laser turns on per a second
        # 500 or 5000 are quite common
        self.vector_frequency = self.get_option(['vf', 'vector-frequency'], default=500)
        # Default vector power (0-100)
        self.vector_power = self.get_option(['vp', 'vector-power'], default=50)
        # Default vector speed (0-100)
        self.vector_speed = self.get_option(['vs', 'vector-speed'], default=30)

        # Bed width in pts
        self.bed_width = self.get_option(['w', 'width'], default=1728)
        # Bed height in pts
        self.bed_height = self.get_option(['h', 'height'], default=864)

        # Additional offset for the x-axis
        self.offset_x = 0
        self.offset_y = 0

    def run(self, job):
        """
        """
        super(Laser, self).run(job)

        # Address potential rotation problems in the given postscript by making
        # sure that if passed print job is same size as the defined bed then we
        # rotate document to same coordinates.
        # XXX fixme

        # Convert postscript to eps.
        log.info('Converting input postscript to EPS.')
        eps = self.ps_to_eps(job.file)

        # run ghostscript on eps
        log.info('Running ghostscript on eps file.')
        (raster, vector) = ghostscript.execute(eps, self.resolution,
                                               self.bed_width, self.bed_height,
                                               ghostscript.raster_mode_to_ghostscript(self.raster_mode))

        # convert image data to pcl
        log.info('Converting image data to PCL.')

        # convert vector data to hpgl
        log.info('Converting ghostscript vector data to HPGL')
        hpgl = self.vector_to_hpgl(vector)

        # send to printer
        log.info('Sending data to printer.')

