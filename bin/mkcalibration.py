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
import ROOT
import numpy
import imp

from advlab import ADVLAB_OUT, ADVLAB_DATA
from advlab.utils.logging_ import logger, startmsg
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import parse_coinc_data
from advlab.utils.gAnalysisUtils import build_spectrum
from advlab.utils.gAnalysisUtils import build_spectrum_plt
from advlab.utils.gAnalysisUtils import build_coinc_curve
from advlab.utils.gAnalysisUtils import build_coinc_curve_plt
from advlab.utils.gAnalysisUtils import check_double_coinc
from advlab.utils.gRootUtils import gRootCanvas
from advlab.utils.gRootUtils import gRootLegend
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure


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

def mkcalibration(**kwargs):
    """
    """
    assert(kwargs['configfile'].endswith('.py'))
    get_var_from_file(kwargs['configfile'])
    infile = data.DATA_FILE
    assert(infile.endswith('.dat'))
    root_outfile_name = os.path.basename(infile.replace('.dat', \
                                                        '_CALIB.root'))
    root_outfile =  os.path.join(ADVLAB_OUT, root_outfile_name)
    AnalyseSpectra = data.AnalyseSpectra
    AnalyseCoincidence = data.AnalyseCoincidence
    RootAnalyseSpectra = data.RootAnalyseSpectra
    RootAnalyseCoincidence = data.RootAnalyseCoincidence
    label = data.SRC
    num_en_ch = data.TOT_NUM_EN_CH
    nbins = data.NBINS
    time_window = data.COINC_WINDOW
    ch, t, e = process_data(infile, [0,2])
    coinc_file_name = os.path.basename(infile.replace('.dat', \
                                                      '_COINC.dat'))
    coinc_file = os.path.join(ADVLAB_DATA, coinc_file_name)
    logger.info('created %s'%coinc_file)
    check_double_coinc(t[0], t[1], e[0], e[1], time_window, coinc_file)
    t1, e1, t2, e2 = parse_coinc_data(coinc_file)
    #-------------Draw Spectra---------------- 
    if AnalyseSpectra == True:
        logger.info('Analyzing Spectrum for %s source...'%label)
        plt.figure(figsize=(10, 7), dpi=80)
        plt.title('%s Spectrum Ch2'%label)
        plt.xlabel('channel')
        build_spectrum_plt(e[1], bins=nbins, label='chanel 1', color='red', \
                           alpha=1, range=(0,num_en_ch))
        plt.xlim(0,num_en_ch)
        overlay_tag()
        plt_figure = '%s_spectrum_ch2.png'%label
        save_current_figure(plt_figure, clear=False)
        #--------
        plt.figure(figsize=(10, 7), dpi=80)
        plt.title('%s Spectrum Ch0'%label)
        plt.xlabel('channel')
        build_spectrum_plt(e[0], bins=nbins, range=(0,num_en_ch),\
                           label='chanel 2', color='blue', alpha=1.)
        plt.xlim(0, num_en_ch)
        overlay_tag()
        plt_figure = '%s_spectrum_ch0.png'%label
        save_current_figure(plt_figure, clear=False)
        plt.show()
        #--------                      
        from matplotlib.colors import LogNorm
        plt.figure(figsize=(10, 7), dpi=80)
        plt.title('%s Ch0 vs Ch2 (events in coincidence only)'%label)
        plt.xlabel('Ch 0')
        plt.ylabel('Ch 2')
        plt.xlim(0, num_en_ch)
        plt.ylim(0, num_en_ch)
        plt.hist2d(e1, e2, bins=nbins, range=[(0,num_en_ch),(0,num_en_ch)])#, norm=LogNorm())
        plt.colorbar()
        overlay_tag()
        plt_figure = '%s_spectrum_ch0-ch2.png'%label
        save_current_figure(plt_figure, clear=False)

    #---------Draw Coincudence curve----------
    if AnalyseCoincidence == True:
        logger.info('Analyzing coincidence curve...')
        plt.figure(figsize=(10, 8), dpi=80)
        plt.title('Ch0 - Ch2 Coincidence Curve')
        plt.xlabel('time [ns]')
        h, _diff = build_coinc_curve_plt(t[0], t[1], nbins=2000, label='chanel 2', \
                                         color='blue', alpha=1.)
        plt.xlim(-10,10)
        plt.yscale('log')
        overlay_tag()
        plt_figure = '%s_CoincCurve_ch0-ch2.png'%label
        save_current_figure(plt_figure, clear=False)
        logger.info('Created %s '%plt_figure)
        logger.info('done!') 

    plt.show()
    
    #--------------ROOT---------------
    if RootAnalyseSpectra == True or RootAnalyseCoincidence == True:
        f = ROOT.TFile(root_outfile, 'RECREATE')
    if RootAnalyseSpectra == True:
        h1 = build_spectrum('%s_channel_0'%label, e[0], num_en_ch)  
        h2 = build_spectrum('%s_channel_1'%label, e[1], num_en_ch)
        # should there be the check of the coincidence here
        hh = ROOT.TH2F('%s_scatter'%label,'%s'%label, nbins, 0, num_en_ch, \
                       nbins, 0, num_en_ch)
        for i,e0 in enumerate(e1):
            hh.Fill(e1[i], e2[i])
        h1.Write()
        h2.Write()
        hh.Write()

    if RootAnalyseCoincidence == True:
        h = build_coinc_curve(t[0], t[1])
        h.SetTitle('Coincidence Curve')
        h.GetXaxis().SetTitle('Time delay [ns]')
        h.GetYaxis().SetTitle('counts')
        h.Write()
    if RootAnalyseSpectra == True or RootAnalyseCoincidence == True:
        f.Close()
        logger.info('Created %s'%root_outfile)


if __name__=='__main__':
    args = PARSER.parse_args()
    startmsg()
    mkcalibration(**args.__dict__)
