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


"""Imaging Configuration file
"""

import ROOT
import os
import numpy as np

from advlab import ADVLAB_DATA
from advlab.utils.logging_ import logger
from advlab.utils.gBox import build_rate_hist

SIDEX = 80
SIDEY = 55

OUTFILE = 'test_imaging.root'
INFILES_TH0 = [os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_40mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_45mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_50mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_55mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_60mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_65mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_70mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_75mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_80mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_85mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_90mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_95mm.dat')]

INFILES_TH120 = [os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_40mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_45mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_50mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_55mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_60mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_65mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_70mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_75mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_80mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_85mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_90mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_95mm.dat')]

INFILES_TH240 = [os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_40mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_45mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_50mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_55mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_60mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_65mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_70mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_75mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_80mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_85mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_90mm.dat'),
              os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_95mm.dat')]
