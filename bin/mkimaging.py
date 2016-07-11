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
import numpy as np
import ROOT
import re
import imp

from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.logging_ import logger, startmsg

YREF = re.compile('\_\d+\.')
THET = re.compile('\_\d+\_')

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

def mkimaging(**kwargs):
    """I have to give a set of 'line', namely lists like [p1, p2, w]
       where p1(x1,y1), p2(x2,y2) determin the line inside the box,
       and w is the wheight resulting from the rate
    """
    assert(kwargs['configfile'].endswith('.py'))
    get_var_from_file(kwargs['configfile'])
    sidex = data.SIDEX
    sidey = data.SIDEY
    yref_list, thet_list = [], []
    infiles = data.INFILES
    for f in infiles:
        my = YREF.search(f).group()
        yref = float(my.replace('_','').replace('.',''))
        mth = THET.search(f).group()
        thet = float(mth.replace('_',''))
        yref_list.append(yref)
        thet_list.append(thet)
    all_th = np.unique(thet_list)
    yref_list = np.array(yref_list)
    lines_list, coinc_list = [], []
    from advlab.utils.gBox import build_rate_hist
    os.system('rm %s'%os.path.join(ADVLAB_OUT,'y_scan.root'))
    from advlab.utils.gBox import mkline
    for th in all_th:
        logger.info('List of angles scanned:')
        _index = np.where(thet_list == th)
        _y, _coinc = build_rate_hist('th%i'%th, infiles[_index], \
                                     yref_list[_index])
        coinc_list.extend(_coinc)
        for y in _y:
            lines_list.append(mkline(y, th))

    from advlab.utils.gBox import imaging 
    outfile_name = data.OUTFILE
    imaging(lines_list, coinc_list, sidex, sidey, gran=5, outfile=outfile_name)
    
if __name__ == '__main__':
    args = PARSER.parse_args()
    startmsg()
    mkimaging(**args.__dict__)
