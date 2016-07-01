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
from scipy.stats import norm
import matplotlib.mlab as mlab

from advlab.utils.logging_ import logger
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import build_spectrum
from advlab.utils.gParsing import build_spectrum_plt
from advlab.utils.gParsing import build_coinc_curve
from advlab.utils.gParsing import build_coinc_curve_plt
from advlab.utils.gRootUtils import gRootCanvas
from advlab.utils.gRootUtils import gRootLegend
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure

AnalyseSpectra = False
AnalyseCoincidence = False
RootAnalyseSpectra = True
RootAnalyseCoincidence = True
SRC = 'Na'
TOT_NUM_EN_CH = 15000 #2**(14-1)
DATA_FILE_NAME = {'delay25ns':'run_gr2_20160630_delay25ns.dat',
                  'delay25ns_3h':'run_gr2_20160630_delay25ns_3h.dat',
                  'delay30ns':'run_gr2_20160630_delay30ns.dat',
                  'first_att':'run_gr2_20160630_coinc_0.dat',

}


from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT

label = 'delay25ns_3h'
outfile_name = DATA_FILE_NAME[label]
outfile = os.path.join(ADVLAB_DATA, outfile_name)
ch, t, e = process_data(outfile, [0,2])

#-------------Draw Spectra---------------- 
if AnalyseSpectra == True:
    logger.info('Analyzing Spectra...')
    (mu21, sigma21) = norm.fit(e[1][2700:3100])
    (mu22, sigma22) = norm.fit(e[1][6600:7200])
    logger.info('Ch2 --> first peak: mu=%.2f, sigma=%.2f'%(mu21, sigma21))
    logger.info('Ch2 --> first peak: mu=%.2f, sigma=%.2f'%(mu21, sigma21))
    (mu01, sigma01) = norm.fit(e[0][2600:3000])
    (mu02, sigma02) = norm.fit(e[0][6200:7100])
    logger.info('Ch0 --> first peak: mu=%.2f, sigma=%.2f'%(mu01, sigma01))
    logger.info('Ch0 --> first peak: mu=%.2f, sigma=%.2f'%(mu01, sigma01))
    
    bins = TOT_NUM_EN_CH/2
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('Na Spectrum Ch2')
    plt.xlabel('channel')
    build_spectrum_plt(e[1], nbins=bins, label='chanel 1', color='red', \
                       alpha=1)
    plt.xlim(0,15000)
    #plt.yscale('log')
    fit21 = mlab.normpdf(bins, mu21, sigma21)
    fit22 = mlab.normpdf(bins, mu22, sigma22)
    plt.plot(bins, fit21, 'r--', linewidth=1)
    plt.plot(bins, fit22, 'r--', linewidth=1)
    overlay_tag()
    plt_figure = 'Na_spectum_ch2.png'
    save_current_figure(plt_figure, clear=False)
    #--------
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('Na Spectrum Ch0')
    plt.xlabel('channel')
    build_spectrum_plt(e[0], nbins=bins, label='chanel 2', color='blue', \
                       alpha=1.)
    plt.xlim(0,15000)
    #plt.yscale('log')
    fit01 = mlab.normpdf(bins, mu01, sigma01)
    fit02 = mlab.normpdf(bins, mu02, sigma02)
    plt.plot(bins, fit21, 'r--', linewidth=1)
    plt.plot(bins, fit22, 'r--', linewidth=1)
    overlay_tag()
    plt_figure = 'Na_spectum_ch2.png'
    save_current_figure(plt_figure, clear=False)
    plt.show()

#---------Draw Coincudence curve----------
if AnalyseCoincidence == True:
    logger.info('Analyzing coincidence curve...')
    plt.figure(figsize=(10, 8), dpi=80)
    plt.title('Ch0 - Ch2 Coincidence Curve')
    plt.xlabel('time [ns]')
    h, _diff = build_coinc_curve_plt(t[0], t[1], nbins=2000, label='chanel 2', \
                              color='blue', alpha=1.)
    (mu, sigma) = norm.fit(_diff)
    logger.info('Coincidence Curve  --> mu=%.2f, sigma=%.2f'%(mu, sigma))
    plt.xlim(-10,10)
    plt.yscale('log')
    overlay_tag()
    plt_figure = 'Na_CoincCurve_ch0-ch2.png'
    save_current_figure(plt_figure, clear=False)
    plt.show()
    logger.info('Created %s '%plt_figure)
    logger.info('done!') 
    
    
if RootAnalyseSpectra == True:
    out_root = os.path.join(ADVLAB_OUT,'%s_spectra_%s.root'%(SRC,label))
    f = ROOT.TFile(out_root, 'RECREATE')
    c = gRootCanvas('spec', 'spec')                 
    h1 = build_spectrum('channel_0', e[0])  
    h2 = build_spectrum('channel_1', e[1]) 
    l_list = [h1, h2]
    l = gRootLegend(l_list)
    h2.SetLineColor(2)                                                 
    h2.Draw()
    h1.SetLineColor(4)
    h1.Draw('SAME')
    l.Draw('SAME')
    c.Write()
    f.Close()
    logger.info('Created %s'%out_root)

if RootAnalyseCoincidence == True: 
    out_root = os.path.join(ADVLAB_OUT,'%s_calibration_%s.root'%(SRC,label))
    f = ROOT.TFile(out_root, 'RECREATE')
    c2 = gRootCanvas('delay','delay')
    h = build_coinc_curve(t[0], t[1])
    h.SetTitle('Coincidence Curve')
    h.GetXaxis().SetTitle('Time delay [ns]')
    h.GetYaxis().SetTitle('counts')
    h.Draw()
    c2.Write()
    
    f.Close()
    logger.info('Created %s'%out_root)
