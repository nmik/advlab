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
LIST_YREF = []
LIST_RATES = []


yref_list_th0 = [40., 45., 50., 55., 60., 65., 70., 75., 80., 85., 90., 95.]
infile_list_th0 = [os.path.join(ADVLAB_DATA, 'run_20160706_Na_0deg_40mm.dat'),
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

yref_th0, rate_th0 = build_rate_hist('th0', infile_list_th0, yref_list_th0)
#logger.info('Maximum rate %.5f at yref = %.2f'%(rate_th0, yref_th0))
LIST_YREF.extend(yref_th0)
LIST_RATES.extend(rate_th0)

    
#  this is supposed to be in bin/mkimaging.py, need a function that gives lines having the box (as gBox object), theta and yref #
def rotate_line(line, theta):
    theta = np.radians(theta)
    new_line = (np.cos(theta)*line[0][0]-np.sin(theta)*line[0][1],\
                np.sin(theta)*line[0][0]+np.cos(theta)*line[0][1]),\
        (np.cos(theta)*line[1][0]-np.sin(theta)*line[1][1],\
         np.sin(theta)*line[1][0]+np.cos(theta)*line[1][1])
    return new_line

from advlab.utils.gBox import imaging
line1 = (-39.5, LIST_YREF[0]), (39.5,LIST_YREF[0])
line2 = (-39.5,LIST_YREF[1]), (39.5,LIST_YREF[1])
line3 = (-39.5,LIST_YREF[2]), (39.5,LIST_YREF[2])
line4 = (-39.5,LIST_YREF[3]), (39.5,LIST_YREF[3])
line5 = (-39.5,LIST_YREF[4]), (39.5,LIST_YREF[4])
line6 = (-39.5,LIST_YREF[5]), (39.5,LIST_YREF[5])
line7 = (-39.5,LIST_YREF[6]), (39.5,LIST_YREF[6])
line8 = (-39.5,LIST_YREF[7]), (39.5,LIST_YREF[7])
line9 = (-39.5,LIST_YREF[8]), (39.5,LIST_YREF[8])
line10 = (-39.5,LIST_YREF[9]), (39.5,LIST_YREF[9])
line11 = (-39.5,LIST_YREF[10]), (39.5,LIST_YREF[10])
line12 = (-39.5,LIST_YREF[11]), (39.5,LIST_YREF[11])
line13 = rotate_line(line1, 30)
line14 = rotate_line(line2, 30)
line15 = rotate_line(line3, 30)
line16 = rotate_line(line4, 30)
line17 = rotate_line(line5, 30)
line18 = rotate_line(line6, 30)
line19 = rotate_line(line7, 30)
line20 = rotate_line(line8, 30)
line21 = rotate_line(line9, 30)
line22 = rotate_line(line10, 30)
line23 = rotate_line(line11, 30)
line24 = rotate_line(line12, 30)
line25 = rotate_line(line1, -30)
line26 = rotate_line(line2, -30)
line27 = rotate_line(line3, -30)
line28 = rotate_line(line4, -30)
line29 = rotate_line(line5, -30)
line30 = rotate_line(line6, -30)
line31 = rotate_line(line7, -30)
line32 = rotate_line(line8, -30)
line33 = rotate_line(line9, -30)
line34 = rotate_line(line10,-30)
line35 = rotate_line(line11, -30)
line36 = rotate_line(line12, -30)

lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, \
        line10, line11, line12, line13, line14, line15, line16, line17, \
        line18, line19, line20, line21, line22, line23, line24, line25, \
        line26, line27, line28, line29, line30, line31, line32, line33, \
        line34, line35, line36]
#lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9, \
#        line10, line11, line12]
rates = LIST_RATES*3
imaging(lines, rates, SIDEX, SIDEY, gran=10)
