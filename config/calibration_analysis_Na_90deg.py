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


"""Analysis configuration file
"""

import os

from advlab import ADVLAB_DATA


AnalyseSpectra = True
AnalyseCoincidence = False
RootAnalyseSpectra = False
RootAnalyseCoincidence = False
SRC = 'Na_90deg'
TOT_NUM_EN_CH = 6000
NBINS = 50
DATA_FILE = os.path.join(ADVLAB_DATA, 'run_gr2_20160705_Na_90deg.dat')
COINC_WINDOW = 20
