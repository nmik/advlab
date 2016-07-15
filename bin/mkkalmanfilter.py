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
from scipy import signal

from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.logging_ import logger, startmsg

YREF = re.compile('\_\d+\.')
THET = re.compile('\_\d+\_')

__description__ = 'Run the Vertexing'


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

def mkkalmanfilter(**kwargs):
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
    th_list, y_list = [], []
    from advlab.utils.gBox import build_rate_hist
    os.system('rm %s'%os.path.join(ADVLAB_OUT,'y_scan.root'))
    from advlab.utils.gAnalysisUtils import find_peaks
    for th in all_th:
        logger.info('List of angles scanned:')
        _index = np.where(thet_list == th)
        _y, _coinc = build_rate_hist('th%i'%th, infiles[_index], \
                                     yref_list[_index])
        _y_arr, _ind = np.unique(np.array(_y), return_index=True)
        _coinc_arr = np.array(_coinc)[_ind]
        _ypeaks = find_peaks(th, _y_arr, _coinc_arr, 250)
        logger.info('%i peaks found!'%len(_ypeaks))
        if len(_ypeaks)<2:
            y_list.append((_ypeaks[0], _ypeaks[0]))
            th_list.append((th, th))
        else:
            y_list.append((_ypeaks[0], _ypeaks[1]))
            th_list.append((th, th))
    print y_list
    print th_list
    
    """
    from advlab.utils.gAnalysisUtils import find_peaks_fit
    th_list, y_list = find_peaks_fit(os.path.join(ADVLAB_OUT,'y_scan.root'))
    """
    from advlab.utils.gBox import get_combinations
    y_comb_list, th_comb_list = get_combinations(th_list, y_list, len(all_th))
    from advlab.utils.gBox import build_states
    from advlab.utils.gKalmanFilter import gExtendedKalmanFilter
    vertex_list, chi2_list = [], []

    for i, yl in enumerate(y_comb_list[:3]):
        measure_list, cov_list = build_states(th_comb_list[i], yl)
        exp_point = np.array([[0.0], [0.0], [1.]])
        X0 = np.array([[0.], [0.]])
        KF = gExtendedKalmanFilter(measure_list, exp_point, cov_list, X0)
        xv, yv, chi2 = KF.compute_vertex()
        if xv is not None:
            vertex_list.append((xv, yv))
            chi2_list.append(chi2)
        else:
            continue
    print 'min chi2 =', min(chi2_list)
    _index = np.where(np.array(chi2_list) == min(chi2_list))[0]
    for ind in _index:
        print '(xv, yv) =', vertex_list[ind]

    """
        _y_arr, _ind = np.unique(np.array(_y), return_index=True)
        _coinc_arr = np.array(_coinc)[_ind]
        from advlab.utils.gAnalysisUtils import find_peaks
        _ypeaks, _coincpeaks = find_peaks(_y_arr, _coinc_arr, 250)
        logger.info('%i peaks found!'%len(_ypeaks))
        for i,y in enumerate(_ypeaks):
            lines_list.append(mkline(y, th))
            coinc_list.append(_coincpeaks[i])
    from advlab.utils.gBox import imaging 
    """
    outfile_name = data.KF_OUTFILE
    #imaging(lines_list, coinc_list, sidex, sidey, gran=5, \
    #          outfile=outfile_name)

if __name__ == '__main__':
    args = PARSER.parse_args()
    startmsg()
    mkkalmanfilter(**args.__dict__)
