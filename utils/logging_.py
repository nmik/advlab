#!/usr/bin/env python                                                          #
#                                                                              #
# Autor: Michela Negro, University of Torino.                                  #
#                                                                              #
# This program is free software; you can redistribute it and/or modify         #
# it under the terms of the GNU GengReral Public License as published by       #
# the Free Software Foundation; either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
#------------------------------------------------------------------------------#


"""Logging utilities, building on top of the python logging module.
"""

import logging
import sys
import time


logger = logging.getLogger('advlab')
logger.setLevel(logging.DEBUG)


""" Configure the main terminal logger.
"""
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
consoleFormatter = logging.Formatter(">>> %(message)s")
consoleHandler.setFormatter(consoleFormatter)
logger.addHandler(consoleHandler)


def abort(message = ''):
    """Abort the execution (via a sys.exit) with a message.
    Use this with care, and opt for custom exceptions whenever possible.
    """
    if message != '':
        message = '%s. Abort.' % message
    else:
        message = 'Abort.'
    sys.exit(message)

def startmsg():
    """Print the start message.
    """
    BUILD_DATE = '29 Jun 2016'
    print('\n    Welcome to advlab (built on %s).\n' %BUILD_DATE)
    print('    Autor: Michela Negro, University of Torino.\n')
    print('    This is a framework created to process data')
    print('    taken during the PET experience of the "Avanced')
    print('    Laboratory" Phd Course (Profs N. Amapane & R. Bellan).\n\n')

if __name__ == '__main__':
    startmsg()
