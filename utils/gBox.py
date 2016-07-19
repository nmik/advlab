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

"""Utilities to make the Imaging
"""

import os
import math
import numpy as np
import ROOT
from scipy.interpolate import griddata

from advlab import ADVLAB_OUT
from advlab import ADVLAB_DATA
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
from advlab.utils.logging_ import logger
from advlab.utils.gAnalysisUtils import check_double_coinc
from advlab.utils.gAnalysisUtils import channel2energy
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import parse_coinc_data

# Coordinates of the mobile RS in the Lab RS.
MOB_RS_Y = 150 #mm
MOB_RS_X = 0

def get_m_q(line):
    m = (line[1][1]-line[0][1])/(line[1][0]-line[0][0])
    q = line[0][1]-m*line[0][0]
    return m, q

def mkline(ybox, theta):
    line = (-60, ybox), (60, ybox)
    r_line = rotate_line(line, theta)
    return r_line

def rotate_line(line, theta):
    """Rotate a line around its center 
    """
    if theta == 0:
        return line
    theta = np.radians(theta)
    new_line = (np.cos(-theta)*line[0][0]-np.sin(-theta)*line[0][1],\
                np.sin(-theta)*line[0][0]+np.cos(-theta)*line[0][1]),\
        (np.cos(-theta)*line[1][0]-np.sin(-theta)*line[1][1],\
         np.sin(-theta)*line[1][0]+np.cos(-theta)*line[1][1])
    return new_line

def get_combinations(th_list, y_list, num_scan_angles):
    """returns a list with all the possible combinations of y_list[i] 
       elements in class num_scan_angles
    """
    y_lists_list = []
    th_lists_list = []
    num_peaks = len(th_list[0])
    print 'num peaks: ',num_peaks
    N = num_peaks**num_scan_angles
    for n in range(0,N):
        BitN = list(str("{0:b}".format(n)))
        BitN = [0]*(num_scan_angles-len(BitN))+BitN
        list1, list2 = [], []
        for i, l in enumerate(y_list):
            list1.append(l[int(BitN[i])])
            list2.append(th_list[i][int(BitN[i])])
        y_lists_list.append(list1)
        th_lists_list.append(list2)
    return y_lists_list, th_lists_list

def build_states(th_list, y_list, return_lines=False):
    """
    """
    a, b = 10.23, 128.
    state_list, cov_list, lines = [], [], []
    for i, th in enumerate(th_list):
        line = mkline(y_list[i], th)
        m, q = get_m_q(line)
        x = np.arange(-10,10)
        y = x*m + q
        yref = 26.5
        if m != 0:
            uk = 1./m
            xk = uk*(yref - q)
            sig_uu = np.tan(np.pi/2-np.arctan(a/b))
            sig_xx = 1./np.cos(np.radians(th))
        else:
            uk = 1./1e-10
            xk = uk*(yref - q)
            sig_uu = 2*uk#np.tan(np.pi/2-2*np.arctan(a/b))
            sig_xx = 1.*xk#/np.cos(np.radians(th))
        state_list.append((xk, uk))
        cov_list.append(np.array([[sig_xx*sig_xx, 0.], [0., sig_uu*sig_uu]]))
        lines.append(line)
        logger.info('Setting cov matrix: sig(xx)=%.2f, sig(uu)=%.2f'%(sig_xx, \
                                                                      sig_uu))
    if return_lines == True:
        return state_list, cov_list, lines
    #plt.show()
    return state_list, cov_list

def imaging(lines_list, rate_list, x_side, y_side, gran=1, \
            outfile='imaging.root'):
    """perform the imaging of the gamma-ray emission from sources 
       inside the red box
    """
    f = ROOT.TFile(os.path.join(ADVLAB_OUT,outfile), 'RECREATE')
    xh_low, xh_high = -x_side/2., x_side/2.
    yh_low, yh_high = -y_side/2., y_side/2.
    xh_bins = np.linspace(xh_low, xh_high, (x_side/5)*2*gran)
    yh_bins = np.linspace(yh_low, yh_high, (y_side/5)*2*gran)
    xh_nbins = len(xh_bins)
    yh_nbins = len(yh_bins)
    hh = ROOT.TH2F('pet', 'Sources imaging', xh_nbins, xh_low, xh_high, \
                   yh_nbins, yh_low, yh_high)
    hh.GetXaxis().SetTitle('x [mm]')
    hh.GetYaxis().SetTitle('y [mm]')
    for i in range(-xh_nbins/2, xh_nbins/2):
        for j in range(-yh_nbins/2, yh_nbins/2):
            hh.Fill(i,j,1)
    for i,line in enumerate(lines_list):
        m, q = get_m_q(line)
        _x = xh_bins
        _y = _x*m + q
        _mask = (_y<=yh_high)&(_y>=yh_low)
        _x = _x[_mask]
        _y = _y[_mask]
        w = rate_list[i]
        for i, x in enumerate(_x):
            bx = hh.GetXaxis().FindBin(x)
            by = hh.GetYaxis().FindBin(_y[i])
            new_w = hh.GetBinContent(bx,by)+w
            hh.SetBinContent(bx,by,new_w)
            for zx in range(bx-gran, bx+gran):
                if zx == 0 or zx < 0:
                    continue
                for zy in range(by-gran, by+gran):
                    if zy == 0 or zy < 0:
                        continue
                    new_w = hh.GetBinContent(zx,zy)+w
                    hh.SetBinContent(zx,zy,new_w)
    hh.Draw('COLZ')
    hh.Write()
    f.Close()
    logger.info('Created %s'%os.path.join(ADVLAB_OUT,outfile))
     
def build_rate_hist(th_label, infile_list, yref_list):
    """
    """
    rate_list = []
    ncoinc_list = []
    for f in infile_list:
        ch, t, e = process_data(f, [0,2])
        coinc_file_name = os.path.basename(f.replace('.dat', '_COINC.dat'))
        coinc_file = os.path.join(ADVLAB_DATA, coinc_file_name)
        check_double_coinc(t[0], t[1], e[0], e[1], 10, coinc_file)
        t1, e1, t2, e2 = parse_coinc_data(coinc_file)
        e1_mev = channel2energy(e1, 0)
        e2_mev = channel2energy(e2, 2)
        _mask0 = (e1_mev < 1.) & (e1_mev > 0.1) 
        _mask2 = (e2_mev < 1.) & (e2_mev > 0.1)
        _mask = _mask0 & _mask2
        t1_w, e1_mev_w, t2_w, e2_mev_w = t1[_mask], e1_mev[_mask], t2[_mask],\
                                 e2_mev[_mask]
        logger.info('%i/%i coincidences in the selected energy window' %\
                    (len(t1_w),len(t1)))
        num_coinc = len(t1_w)
        time_interval = (t[0][-1] - t[0][0])/10000000
        logger.info('effective time interval = %i s'%time_interval)
        rate = float(num_coinc)/time_interval
        logger.info('Rate = %.5f s^{-1}'%rate)
        rate_list.append(rate)
        ncoinc_list.append(num_coinc)
    root_file_name = os.path.join(ADVLAB_OUT,'y_scan.root')
    if not os.path.exists(root_file_name):
        root_file = ROOT.TFile(root_file_name,'RECREATE')
    else:
        root_file = ROOT.TFile(root_file_name,'UPDATE')
    nbins = len(yref_list) - 1
    y_min, y_max = 70 - yref_list[0], 70 - yref_list[-1]
    h = ROOT.TH1F(th_label, th_label, nbins, y_min , y_max)
    #h.Sumw2()
    ybox_list = []
    for i, c in enumerate(ncoinc_list):
        y = 70 - yref_list[i]
        ybox_list.append(y)
        h.Fill(y, c)
    h.GetXaxis().SetTitle('y [mm]')
    h.GetYaxis().SetTitle('Number of Coincidences')
    h.Write()
    root_file.Close()
    logger.info('Created %s'%root_file_name)
    return ybox_list, ncoinc_list

def main():
    """Simple test code.
    """
    th_list = [(0,0),(40,40),(80,80)]
    y_list = [(15,0),(0,20),(-20,25)]
    num_scan_angles = len(th_list)
    y_lists_list, th_lists_list = get_combinations(th_list, y_list, \
                                                   num_scan_angles)
    for i,y in enumerate(y_lists_list):
        print y
    

if __name__ == '__main__':
    main()
