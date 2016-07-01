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

"""advlab: Framework for 'Advanced Laboratory' PhD Course
"""

import os

PACKAGE_NAME = 'advlab'

"""Basic folder structure of the package.
"""
ADVLAB_ROOT = os.path.abspath(os.path.dirname(__file__))
ADVLAB_BIN = os.path.join(ADVLAB_ROOT, 'bin')
ADVLAB_CONFIG = os.path.join(ADVLAB_ROOT, 'config')
ADVLAB_UTILS = os.path.join(ADVLAB_ROOT, 'utils')
ADVLAB_DOC = os.path.join(ADVLAB_ROOT, 'doc')
ADVLAB_DOC_FIGURES = os.path.join(ADVLAB_DOC, 'figures')
ADVLAB_DATA = os.path.join(ADVLAB_ROOT, 'data')

""" This is the output directory.
"""
try:
    ADVLAB_OUT = os.environ['ADVLAB_OUT']
except:
    ADVLAB_OUT = os.path.join(ADVLAB_ROOT, 'output')

if __name__ == '__main__':
    print('ADVLAB_ROOT: %s' % ADVLAB_ROOT)
    print ADVLAB_UTILS
