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


"""Functions to parse the CAEN output ascii file
"""

import numpy as np
import os
import ROOT
from ROOT import *

from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt


def parse_data(file_path):
    """Parse the ASCII file with the GRB light curve data from Swift.   
       
       Arguments
       ---------
       file_path : str
           path and name of the file to process
    """
    ch = []
    t = []
    e = []
    for line in open(file_path):
        try:
            _ch, _t, _e, _boh1, _boh2 = [float(item) for item in line.split()]
            ch.append(_ch)
            t.append(_t)
            e.append(_e)
        except:
            pass
    ch = np.array(ch)
    t = np.array(t,dtype=np.int64)
    e = np.array(e)
    return ch, t, e

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
    nbins = kwargs['nbins']
    h = plt.hist(_e, nbins, label=kwargs['label'], \
                 color=kwargs['color'], alpha=kwargs['alpha'])
    return h
    
def channel2energy(_e, ref_point1, ref_point2):
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
    m = (ref_point2[1]-ref_point1[1])/(ref_point2[0]-ref_point1[0])
    q = ref_point1[1]-ref_point1[0]*(ref_point2[1]-ref_point1[1])/\
        (ref_point2[0]-ref_point1[0])
    en_array = m*_e + q
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
    logger.info('Scanning the data to find coincidences...')
    switch = False
    if _t1[0] > _t2[0]:
        switch = True
        logger.info('Exchanging time arrays to maintain the sequence...')
        _ttemp =  _t1
        _t1 = _t2
        _t2 = _ttemp
    coinc_events = []
    for j, t_min in enumerate(_t1):
        t_max = t_min + time_window
        _mask = (_t2 >= t_min)*(_t2 <= t_max)
        if np.count_nonzero(_mask) != 0:
            for i, item in enumerate(_t2[_mask]):
                index = np.where(_t2 == _t2[_mask][i])[0]
                if len(index)>1:
                    index = [np.amin(index)]
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
        file_to_write.write('%i %.2f\t%i %.2f\n' %(line[0], line[1], line[2],\
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
    if _t1[0] > _t2[0]:
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
    if _t1[0] > _t2[0]:
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

def process_data(file_path, num_of_channels):
    """Parse the ASCII file with the GRB light curve data from Swift.   
       
       Arguments
       ---------
       file_path : str
           path and name of the file to process
       num_of_channels : list of int
           the number of the channels used in the CAEN module; 
           in our case we must choose among 4 channels (0, 1, 2, or 3)
    """
    logger.info('Parsing data file...')
    _ch, _t, _e = parse_data(file_path)
    _index = np.argsort(_t)
    _ch = _ch[_index] 
    _t = _t[_index]
    _e = _e[_index]
    ch, t, e = [], [], []
    logger.info('splitting the channels...')
    _t = _t*10
    logger.info('Time is returned in ns...')
    for channel in num_of_channels:
        _mask = np.where(_ch == channel)
        ch.append(_ch[_mask])
        t.append(_t[_mask])
        e.append(_e[_mask])
    return ch, t, e


def main():
    """Simple function test
    """
    from advlab import ADVLAB_DATA
    outfile = os.path.join(ADVLAB_DATA, 'test_outfile.dat')
    ch, t, e = process_data(outfile, [0,2])
    for i in range(0,len(ch[0])):
        print 'ch: %i --> time: %i, spectrum ch: %i' %(ch[0][i], t[0][i], \
                                                       e[0][i])
    for i in range(0,len(ch[1])):
        print 'ch: %i --> time: %i, spectrum ch: %i' %(ch[1][i], t[1][i], \
                                                       e[1][i])

if __name__=='__main__':
    main()
