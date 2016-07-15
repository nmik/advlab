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


import numpy as np
import os
import ROOT
from ROOT import *

from advlab import ADVLAB_OUT
from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import save_current_figure, overlay_tag

def find_peaks(th, _x, _y, threashold):
    """to be finished
    """
    c = (np.diff(np.sign(np.diff(_y))) < 0).nonzero()[0] + 1 # local max
    bad = []
    for i, index in enumerate(c):
        if _y[index] < threashold:
            bad.append(i)
    c = np.delete(c, bad)
    plt.plot(_x,_y)
    plt.plot(_x[c], _y[c], "o", label="max")
    overlay_tag()
    save_current_figure('th%i_peaks.png'%th, clear=False)
    return _x[c]

def find_peaks_fit(file_name, isfit=True):
    """
    """
    file1 = ROOT.TFile(file_name)
    y_list  = []
    th_list = []
    for key in file1.GetListOfKeys():
        th_list.append((int(key.GetName().replace("th","")), \
                       int(key.GetName().replace("th",""))))
        h = file1.Get(key.GetName())
        peaks = []
        for i in range(1, h.GetNbinsX()):
            if h.GetBinContent(i-1) < h.GetBinContent(i) and  \
               h.GetBinContent(i) > h.GetBinContent(i+1):
                peaks.append((h.GetBinCenter(i), h.GetBinContent(i)))
            if len(peaks) > 2:
                if peaks[0][1] < peaks[1][1] and peaks[0][1] < peaks[2][1]: 
                    peaks.pop(0)
                elif peaks[1][1] < peaks[0][1] and peaks[1][1] < peaks[2][1]: 
                    peaks.pop(1)
                elif peaks[2][1] < peaks[0][1] and peaks[2][1] < peaks[1][1]: 
                    peaks.pop(2)
        if len(peaks) == 1: 
            peaks.append(peaks[0])
        if not isfit:
            y_list.append((peaks[0], peaks[1]))
            continue
        Max = h.GetXaxis().GetXmax()
        Min = h.GetXaxis().GetXmin()
        g1 = ROOT.TF1("g1", "gaus", Min, Max)
        g2 = ROOT.TF1("g2","gaus", Min, Max)
        g1.SetParameter(1, peaks[0][0])
        g1.SetParameter(2, 6)
        g2.SetParameter(1, peaks[1][0])
        g2.SetParameter(2, 6)
        ftot = ROOT.TF1( 'total', 'gaus(0)+gaus(3)', Min, Max )
        par11, par12, par13 = g1.GetParameter(0), g1.GetParameter(1), \
                              g1.GetParameter(2)
        par21, par22, par23 = g2.GetParameter(0),  g2.GetParameter(1),  \
                              g2.GetParameter(2)
        par = np.array([par11, par12, par13, par21, par22, par23])
        ftot.SetParameters(par)
        h.Fit(ftot)
        y_list.append((ftot.GetParameter(1), ftot.GetParameter(4)))
    return th_list, y_list

def build_spectrum(name, _e, tot_num_en_ch):
    """Returns a root THF1 with the energy spectrum of the gamma 
       emission from a ginven src
    """
    nbins = tot_num_en_ch/2
    h = ROOT.TH1F(name, name, nbins, 0, tot_num_en_ch)
    for en in _e:
        h.Fill(en)
    return h

def build_spectrum_plt(_e, **kwargs):
    """Returns a histo (using matplotlib) with the energy spectrum of the gamma 
       emission from a ginven src
    """
    h = plt.hist(_e, bins=kwargs['bins'], label=kwargs['label'], \
                 color=kwargs['color'], alpha=kwargs['alpha'],\
                 range=kwargs['range'] )
    return h
    
def channel2energy(_e, ch_num):
    """Calibrate the measure of energy in the channels

       Arguments
       ---------
       _e : numpy array of floats
           Array where all the energy channels are stored for each event
       tot_num_en_ch : int
           number of storing channels 
       ref_point1, ref_point2 : each one is a couples of numbers 
           e.g. (ch_ref1,e_ref1),(ch_ref2,e_ref2)
           It is assumed that for each couple the first num is the channel
           while the sencond is the corresponding energy [given in MeV].
    """
    ch, en = [], [] 
    calib_ch0 = [(1917,0.356),(466,0.08),(2721,0.511),(6594,1.27),\
                 (3504,0.662),(6044,1.17),(6843,1.33)]
    calib_ch2 = [(2022,0.356),(496,0.08),(2846,0.511),(6906,1.27),\
                 (3674,0.662),(6362,1.17),(7214,1.33)]
    if ch_num == 0:
        ch.append([x[0] for x in calib_ch0][0])
        en.append([x[1] for x in calib_ch0][0])
    if ch_num == 2:
        ch.append([x[0] for x in calib_ch2][0])
        en.append([x[1] for x in calib_ch2][0])
    ch = np.array(ch)
    en = np.array(en)
    p = np.polyfit(ch, en, 1)
    en_array = p[1] + _e*p[0]
    return en_array

def check_double_coinc(_t1, _t2, _e1, _e2, time_window, outfile):
    """Check events happened in coincidence, inside a coincidence window,
       
       Arguments
       ---------
       _t1 : numpy array of int 
           array of a first chanel event arrival times in us
       _t2 : numpy array of int [times in us]
           array of a second chanel event arrival times in us
       time_window : float
           coincidence window in us
       outfile : str
           output file name
    """
    if os.path.exists(outfile):
        logger.info('Already created %s'%outfile)
        return 0
    logger.info('Scanning the data to find coincidences...')
    switch = False
    if len(_t1) > len(_t2):
        switch = True
        logger.info('Exchanging time arrays to maintain the sequence...')
        _ttemp =  _t1
        _t1 = _t2
        _t2 = _ttemp
        _etemp =  _e1
        _e1 = _e2
        _e2 = _etemp
    coinc_events = []
    for j, t_min in enumerate(_t1):
        t_min = t_min - time_window/2
        t_max = t_min + time_window/2
        _mask = (_t2 >= t_min)*(_t2 <= t_max)
        if np.count_nonzero(_mask) != 0:
            for i, item in enumerate(_t2[_mask]):
                index = np.where(_t2 == _t2[_mask][i])[0]
                if len(index)>1:
                    index = [np.amin(abs(index-t1))]
                if switch == False:
                    coinc_events.append((_t1[j], _e1[j], _t2[index], \
                                         _e2[index]))
                else:
                    coinc_events.append((_t2[index], _e2[index], _t1[j], \
                                         _e1[j]))
    logger.info('%i pairs of coincident events found!'%len(coinc_events))
    file_to_write = open(outfile, 'w')
    file_to_write.write('#FIRST CHANNEL\t#SECOND CHANNEL \n\n')
    file_to_write.write('#time - energy\t#time -  energy \n\n')
    for line in coinc_events:
        file_to_write.write('%i %.2f %i %.2f\n' %(line[0], line[1], line[2],\
                                                   line[3]))
    file_to_write.close()
    logger.info('Created output file %s...'%outfile)
    return 0

def build_coinc_curve(_t1, _t2):
    """Returns the histogram to estrapolate the coincidence curve

       Arguments        
       ---------                          
       _t1 : numpy array of int                       
           array of a first chanel event arrival times in us 
       _t2 : numpy array of int [times in us]      
           array of a second chanel event arrival times in us  
    """
    # _t1 and _t2 are ordered arrays
    # Check which array starts first
    if len(_t1) > len(_t2):
        logger.info('Excenging time arrays to maintain the sequence...')
        _ttemp =  _t1
        _t1 = _t2
        _t2 = _ttemp
    diff_eff = abs(len(_t1)-len(_t2))
    tot_evt = max(len(_t1),len(_t2))
    logger.info('Difference of number of events: %i/%i' \
                %(diff_eff,tot_evt))
    logger.info('Building Coincidence Curve...')
    h2 = ROOT.TH1F('delay2', 'delay2', 200, -100.5, 99.5)
    # Loop over the shorter array
    for i,t1 in enumerate(_t1):
        # Loop over the second array but from the (i-3)th element
        # for this reason, skip the first 3 entries
        if i < 3:
            pass
        else:
            min_diff = 100000000000.
            for t2 in _t2[i-3:]:
                # Check when there is the minimum distance and record it
                # exit the inner loop when distance start to increase
                abs_diff = abs(t1-t2)
                if abs_diff > min_diff:
                    break
                else:
                    min_diff = t1-t2
                    continue
            if abs(min_diff) < 1000:
                h2.Fill(min_diff)
    return h2   

   
def build_coinc_curve_plt(_t1,_t2, **kwargs):
    """Returns a histo (using matplotlib) with the energy spectrum of the gamma 
       emission from a ginven src
       
       Arguments        
       ---------                          
       _t1 : numpy array of int                       
           array of a first chanel event arrival times in us 
       _t2 : numpy array of int [times in us]      
           array of a second chanel event arrival times in us  
    """
    # _t1 and _t2 are ordered arrays
    # Check which array starts first
    if len(_t1) > len(_t2):
        logger.info('Excenging time arrays to maintain the sequence...')
        _ttemp =  _t1
        _t1 = _t2
        _t2 = _ttemp
    diff_eff = abs(len(_t1)-len(_t2))
    tot_evt = max(len(_t1),len(_t2))
    logger.info('Difference of number of events: %i/%i' \
                %(diff_eff,tot_evt))
    logger.info('Building Coincidence Curve...')
    _diff = []
    # Loop over the shorter array
    for i,t1 in enumerate(_t1):
        # Loop over the second array but from the ith element
        # for this reason, skip the first 3 entries
        if i < 3:
            pass
        else:
            min_diff = 100000000000.
            for t2 in _t2[i-3:]:
                # Check when there is the minimum distance and record it
                # exit the inner loop when distance start to increase
                abs_diff = abs(t1-t2)
                if abs_diff > min_diff:
                    break
                else:
                    min_diff = t1-t2
                    continue
            if abs(min_diff) < 1000:
                _diff.append(min_diff)
    _diff = np.array(_diff)
    nbins = kwargs['nbins']
    h = plt.hist(_diff, nbins, label=kwargs['label'], color=kwargs['color'],\
                 alpha=kwargs['alpha'], align='mid')
    return h, _diff
