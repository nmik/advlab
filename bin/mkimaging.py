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


"""Imaging app
"""

import os
import numpy
import ROOT
import re
import imp

from advlab import ADVLAB_DATA
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.logging_ import logger, startmsg

YREF = re.compile('\_\d\d[mm]')

__description__ = 'Run the calibration module'


"""Command-line switches.
"""
import argparse

formatter = argparse.ArgumentDefaultsHelpFormatter
PARSER = argparse.ArgumentParser(description=__description__,
                                 formatter_class=formatter)
PARSER.add_argument('--configfile', type=str, required=True,
                    help='the input configuration file')

def get_var_from_file(filename):
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()

def mkline(ybox, theta):
    from advlab.utils.gBox import rotate_line
    line = (-39.5, ybox), (39.5, ybox)
    r_line = rotate_line(line, theta)
    return r_line

def mkimaging(**kwargs):
    """I have to give a set of 'line', namely lists like [p1, p2, w]
       where p1(x1,y1), p2(x2,y2) determin the line inside the box,
       and w is the wheight resulting from the rate
    """
    assert(kwargs['configfile'].endswith('.py'))
    get_var_from_file(kwargs['configfile'])
    sidex = data.SIDEX
    sidey = data.SIDEY
    yref_list = []
    # th0
    infiles_th0 = data.INFILES_TH0
    for f in infiles_th0:
        m = YREF.search(f).group()
        yref = float(m.replace('_','').replace('m',''))
        yref_list.append(yref)
    # th120
    infiles_th120 = data.INFILES_TH120
    for f in infiles_th120:
        m = YREF.search(f).group()
        yref = float(m.replace('_','').replace('m',''))
        yref_list.append(yref)
    # th240
    infiles_th240 = data.INFILES_TH240
    for f in infiles_th240:
        m = YREF.search(f).group()
        yref = float(m.replace('_','').replace('m',''))
        yref_list.append(yref)
    lines, coinc = [], []
    from advlab.utils.gBox import build_rate_hist
    y_th0, coinc_th0 = build_rate_hist('th0', infiles_th0, yref_list[:len(infiles_th0)])
    coinc.extend(coinc_th0)
    for i, y in enumerate(y_th0):
        lines.append(mkline(y,0))
    y_th120, coinc_th120 = build_rate_hist('th120', infiles_th120, \
                           yref_list[len(infiles_th0):len(infiles_th0)+len(infiles_th120)])
    coinc.extend(coinc_th120)
    for i, y in enumerate(y_th120):
        lines.append(mkline(y, 120))
    y_th240, coinc_th240 = build_rate_hist('th240', infiles_th240, 
                           yref_list[len(infiles_th120):len(infiles_th120)+len(infiles_th240)])
    coinc.extend(coinc_th240)
    for i, y in enumerate(y_th240):
        lines.append(mkline(y, 240))
    from advlab.utils.gBox import imaging 
    outfile_name = data.OUTFILE
    imaging(lines, coinc, sidex, sidey, gran=5, outfile=outfile_name)
    
if __name__ == '__main__':
    args = PARSER.parse_args()
    startmsg()
    mkimaging(**args.__dict__)
