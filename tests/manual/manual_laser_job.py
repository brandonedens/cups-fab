# Brandon Edens
# 2010-03-15
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
Send a manual print job to a laser cutter.
"""

###############################################################################
## Imports
###############################################################################

import socket
import time

from cStringIO import StringIO


###############################################################################
## Constants
###############################################################################

HOSTNAME = "epilog-mini"
PORT = 515

# The escape character.
ESCAPE = chr(0x1b)


###############################################################################
## Classes
###############################################################################


###############################################################################
## Functions
###############################################################################

def main():
    """
    """

    data = StringIO()
    data.write(ESCAPE + "%-12345X@PJL JOB NAME=brandon")
    data.write(chr(0x0d) + chr(0x0a))
    data.write(ESCAPE + "E@PJL ENTER LANGUAGE=PCL ")
    data.write(chr(0x0d) + chr(0x0a))
    data.write(ESCAPE + '&y0A')
    data.write(ESCAPE + '&y0C')
    data.write(ESCAPE + '&y0Z')
    data.write(ESCAPE + '&l0U')
    data.write(ESCAPE + '&l0Z')
    data.write(ESCAPE + '&u300D')
    data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*p0Y')
    data.write(ESCAPE + '*t300R')
    data.write(ESCAPE + '*r0F')
    data.write(ESCAPE + '&y50P')
    data.write(ESCAPE + '&z50S')
    data.write(ESCAPE + '&z2A')
    data.write(ESCAPE + '*r3300T')
    data.write(ESCAPE + '*r2550S')
    # Compression mechanism
    data.write(ESCAPE + '*b2M')
    data.write(ESCAPE + '&y0O')
    data.write(ESCAPE + '*r1A')
    data.write(ESCAPE + '*p1Y')
    data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*b1A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*p500Y')
    data.write(ESCAPE + '*p5000X')
    data.write(ESCAPE + '*b-200A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*p2000Y')
    data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*b500A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*p2001Y')
    #data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*b-500A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*p2001Y')
    #data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*b500A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*p1000Y')
    #data.write(ESCAPE + '*p0X')
    data.write(ESCAPE + '*b800A')
    data.write(ESCAPE + '*b8W')
    data.write(chr(0x01))
    data.write(chr(0x06))
    data.write(chr(0x04))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(chr(0x80))
    data.write(ESCAPE + '*rC')
    data.write(ESCAPE + "%1BPU")
    data.write(ESCAPE + "E")
    data.write(ESCAPE + '%-12345X@PJL EOJ ')
    data.write(chr(0x0d) + chr(0x0a))
    for x in xrange(0, 2048):
        data.write(chr(0x20))
    data.write('Mini;')

    # Open the socket to the laser cutter
    print "opening socket"
    sock = socket.create_connection((HOSTNAME, PORT),
                                    60)

    job_name = "123"
    job_user = "jdoe"
    job_title = "manual"
    localhost = "lucky"

    sock.sendall(chr(002) + "legend\n")
    result = sock.recv(1)
    if ord(result) != 0:
        print "Error communicating."
        sock.close()
        return

    sock.sendall(chr(002) + "legend\n")
    result = sock.recv(1)
    if ord(result) != 0:
        print "Error communicating."
        sock.close()
        return

    header = StringIO()
    header2 = StringIO()
    header.write("H%s\n" % localhost)
    #header.write("P%s\n" % job_user)
    #header.write("J%s\n" % job_title)
    #header.write("ldfA%s%s\n" % (job_name, localhost))
    #header.write("UdfA%s%s\n" % (job_name, localhost))
    #header.write("N%s\n" % job_title)
    header2.write(chr(002) + "7 cfA%s%s\n" % (job_name, localhost))
    header2.seek(0)
    sock.sendall(header2.read())
    if ord(result) != 0:
        print "Error sending start header"
        print "recived result = %d." % ord(result)
        sock.close()
        return
    header.seek(0)
    #sock.sendall(header.read())
    #result = sock.recv(1)
    #if ord(result) != 0:
    #    print "Error sending rest of header"
    #    print "recived result = %d." % ord(result)
    #    sock.close()
    #    return

    print "data size is %s" % data.tell()
    sock.sendall(chr(3) + "%d cfAmanuallocalhost\n" % data.tell())
    data.seek(0)
    print "sending data"
    sock.sendall(data.read())
    result = sock.recv(1)
    if ord(result) != 0:
        print "Error sending data."
        sock.close()
        return

    # Close the socket to the laser cutter
    print "closing socket"
    sock.close()


if __name__ == '__main__':
    main()

