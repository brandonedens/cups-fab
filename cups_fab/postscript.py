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
File holds functionality related to postscript specifically converting
postscript to encapsulated postscript (eps).
"""

###############################################################################
## Imports
###############################################################################

import re
from cStringIO import StringIO


###############################################################################
## Constants
###############################################################################

BOUNDING_BOX_PS = "/==={(        )cvs print}def/stroke{currentrgbcolor 0.0 \
eq exch 0.0 eq and exch 0.0 ne and{(P)=== currentrgbcolor pop pop 100 mul \
round  cvi = flattenpath{transform(M)=== round cvi ===(,)=== round cvi \
=}{transform(L)=== round cvi ===(,)=== round cvi =}{}{(C)=}pathforall \
newpath}{stroke}ifelse}bind def/showpage{(X)= showpage}bind def\n"


###############################################################################
## Functions
###############################################################################

def ps_to_eps(in_file, width, height,
              flip=False, raster_mode=None, screen=-6, resolution=600):
    """
    Convert a postscript file to an EPS file. This function adds additional
    information after the PageBoundingBox entry. It also makes adjustment
    to the postscript if the raster_mode is mono AND (screen mode is a
    value other than 0 OR resolution is higher than 600)

    Arguments for this function are:

    * in_file - the input postscript file
    * width - the width of the printed page for the device (not the input file)
    * height - the height of the printed page for the device (not the input
      file)
    * flip - whether or not to flip the in_file's page along x-axis.
    * raster_mode - the mode that raster data will be converted to:
      one of none, mono, grey, or color
    * screen - the postscript half-toning screen
    * resolution - the resolution for printing in dots per inch.
    """
    out = StringIO()

    for line in in_file.readlines():
        if line.startswith('%%PageBoundingBox:'):
            out.write(line)
            match = re.search("%%PageBoundingBox: (\d+) (\d+) (\d+) (\d+)",
                              line)
            groups = match.groups()
            lower_left_x = int(groups[0])
            lower_left_y = int(groups[1])
            upper_right_x = int(groups[2])
            upper_right_y = int(groups[3])

            xoffset = lower_left_x
            yoffset = lower_left_y
            doc_width = upper_right_x - lower_left_x
            doc_height = upper_right_y - lower_left_y

            out.write('/setpagedevice{pop}def\n')

            # Bugfix for situation where x,y offset is non 0
            if xoffset or yoffset:
                out.write("%d %d translate\n", -xoffset, -yoffset)

            # Adjust for situation where user wants flip.
            if flip:
                out.write("%d 0 translate -1 1 scale\n" % doc_width)
            continue
        elif line.startswith('%!'):
            out.write(BOUNDING_BOX_PS)
            if raster_mode == 'mono':
                if screen == 0:
                    out.write('{0.5 ge{1}{0}ifelse}settransfer\n')
                else:
                    if resolution >= 600:
                        # Adjust for overprint
                        out.write("{dup 0 ne{%d %d div add}if}settransfer\n"
                                  % resolution / 600, screen)
                    # Setup the mono raster screen mode.
                    out.write("%d " % resolution / screen)
                    if screen > 0:
                        out.write("30{pop abs 1 exch sub}")
                    else:
                        out.write(
                            "30{180 mul cos exch 180 mul cos add 2 div}"
                            )
                    out.write("setscreen\n")
        out.write(line)
    out.seek(0)
    return out

