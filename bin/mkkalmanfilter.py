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
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
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
    from advlab.utils.gAnalysisUtils import find_peaks_fit
    th_list, y_list = find_peaks_fit(os.path.join(ADVLAB_OUT,'y_scan.root'))
    from advlab.utils.gBox import get_combinations
    y_comb_list, th_comb_list = get_combinations(th_list, y_list, len(all_th))
    logger.info('Number of Combinations: %i'%len(y_comb_list))
    from advlab.utils.gBox import build_states
    from advlab.utils.gKalmanFilter import gExtendedKalmanFilter
    vertex_list, chi2_list, lines_list = [], [], []
    plt.figure()
    plt.title('Distribution of vertexes')
    plt.xlim(-39.5, 39.5)
    plt.ylim(-26.5, 26.5)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    for i, yl in enumerate(y_comb_list):
        measure_list, cov_list, lines = build_states(th_comb_list[i], yl, return_lines=True)
        exp_point = np.array([[0.0], [0.0], [0.]])
        X0 = np.array([[0.], [0.]])
        KF = gExtendedKalmanFilter(measure_list, exp_point, cov_list, X0)
        xv, yv, chi2 = KF.compute_vertex()
        if xv is not None:
            plt.plot(xv,yv, 'o')
            vertex_list.append((xv, yv))
            chi2_list.append(chi2)
            lines_list.append(lines)
        else:
            continue
    overlay_tag()
    outfile_name = data.KF_OUTFILE
    save_current_figure(outfile_name.replace('.png','_DISTRIB.png'), clear=False)
    _index = np.where(np.array(chi2_list) == min(chi2_list))[0]
    plt.figure()
    ax = plt.subplot()
    for ind in _index:
        logger.info('1st vertex: (%.2f, %.2f)'%(vertex_list[ind][0],vertex_list[ind][1]))
        logger.info('Chi2 = %f'%chi2_list[ind])
        plt.plot(vertex_list[ind][0],vertex_list[ind][1],'o',color='red')
        for l in lines_list[ind]:
            plt.plot([l[0][0],l[1][0]],[l[0][1],l[1][1]], '--', color='darkgray')
        v_label = '(%.2f, %.2f)'%(vertex_list[ind][0],vertex_list[ind][1])
        chi2_label = '%.5f'%chi2_list[ind]
        ax.annotate(v_label, xy=(vertex_list[ind][0]-6, vertex_list[ind][1]-2), \
                    xytext=(vertex_list[ind][0]-6, vertex_list[ind][1]-2))
        ax.annotate('$\chi^{2}=$'+chi2_label,xy=(vertex_list[ind][0]-4, vertex_list[ind][1]-4),\
                    xytext=(vertex_list[ind][0]-6,vertex_list[ind][1]-4))
        vertex_list.pop(ind)
        chi2_list.pop(ind)
    _index = np.where(np.array(chi2_list) == min(chi2_list))[0]
    for ind in _index:
        logger.info('2nd vertex: (%.2f, %.2f)'%(vertex_list[ind][0],vertex_list[ind][1]))
        logger.info('Chi2 = %f'%chi2_list[ind])
        plt.plot(vertex_list[ind][0],vertex_list[ind][1],'o',color='blue')
        for l in lines_list[ind]:
            plt.plot([l[0][0],l[1][0]],[l[0][1],l[1][1]], '--', color='silver')
        v_label = '(%.2f, %.2f)'%(vertex_list[ind][0],vertex_list[ind][1])
        chi2_label = '%.5f'%chi2_list[ind]
        ax.annotate(v_label, xy=(vertex_list[ind][0]-6, vertex_list[ind][1]-2), \
                    xytext=(vertex_list[ind][0]-6, vertex_list[ind][1]-2))
        ax.annotate('$\chi^{2}=$'+chi2_label,xy=(vertex_list[ind][0]-6, vertex_list[ind][1]-4),\
                    xytext=(vertex_list[ind][0]-6,vertex_list[ind][1]-4))
    plt.xlim(-39.5, 39.5)
    plt.ylim(-26.5, 26.5)
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.title('Vertexing of Na$^{22}$ sources')
    overlay_tag()
    outfile_name = data.KF_OUTFILE
    save_current_figure(outfile_name, clear=False)
    plt.show()

if __name__ == '__main__':
    args = PARSER.parse_args()
    startmsg()
    mkkalmanfilter(**args.__dict__)
