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
Software for handling cups specific command line options and DEVICE_URI
parameters.
"""

###############################################################################
## Imports
###############################################################################

import re


###############################################################################
## Functions
###############################################################################

def command_line_parameters(argv):
    """
    Extract cups command line parameters and return dictionary of values.
    """
    options = {}

    # Read command line arguments which should be of the form:
    # ./backend-name job user title copies options
    # number of the print job
    try:
        options['job_number'] = argv[1]
    except:
        pass
    # user that submitted job
    try:
        options['user'] = argv[2]
    except:
        pass
    # title of job
    try:
        options['title'] = argv[3]
    except:
        pass
    # number of copies for job
    try:
        options['copies'] = argv[4]
    except:
        pass
    # options related to job
    try:
        options['options'] = argv[5]
    except:
        # job options are optional
        pass
    # input file
    try:
        options['in_filename'] = argv[6]
    except:
        pass

    return options

def device_uri(device_uri_variable):
    """
    Extract information about usage of this backend from the cups environment
    variable DEVICE_URI.
    """
    options = {}
    match = re.search('([A-Za-z\-0-9]+)://([A-Za-z\-0-9.]+)/(.*)', device_uri_variable)
    # First parameter is the backend name.
    options['backend'] = match.group(1)
    # Second paramter is the device to use either a hostname or character.
    # device in the /dev/ filesystem.
    options['device'] = match.group(2)

    # Extract the settings for the device.
    settings = match.group(3).split('/')

    # Iterate over the settings extracting the key/value pairs.
    for setting in settings:
        # Make sure setting is not blank.
        if setting:
            (key, value) = setting.split('=')
            options[key] = value

    return options

