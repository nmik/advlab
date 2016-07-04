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

from advlab import ADVLAB_DATA


AnalyseSpectra = True
AnalyseCoincidence = False
RootAnalyseSpectra = False
RootAnalyseCoincidence = False
SRC = 'Co'
TOT_NUM_EN_CH = 4000
DATA_FILE = os.path.join(ADVLAB_DATA, 'run_gr2_20160704_Co.dat')
COINC_WINDOW = 20

"""
#-------------Draw Spectra---------------- 
if AnalyseSpectra == True:
    logger.info('Analyzing Spectra...')
    (mu21, sigma21) = norm.fit(e[1][2700:3100])
    (mu22, sigma22) = norm.fit(e[1][6600:7200])
    logger.info('Ch2 --> 1st peak: mu=%.2f, sigma=%.2f'%(mu21, sigma21))
    logger.info('Ch2 --> 2nd peak: mu=%.2f, sigma=%.2f'%(mu22, sigma22))
    (mu01, sigma01) = norm.fit(e[0][2600:3000])
    (mu02, sigma02) = norm.fit(e[0][6200:7100])
    logger.info('Ch0 --> 1st peak: mu=%.2f, sigma=%.2f'%(mu01, sigma01))
    logger.info('Ch0 --> 2nd peak: mu=%.2f, sigma=%.2f'%(mu02, sigma02))
    
    bins = TOT_NUM_EN_CH/2
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('%s Spectrum Ch2'%SRC)
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
    plt_figure = '%s_spectrum_ch2.png'%SRC
    save_current_figure(plt_figure, clear=False)
    #--------
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('%s Spectrum Ch0'%SRC)
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
    plt_figure = '%s_spectrum_ch0.png'%SRC
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
    plt_figure = '%s_CoincCurve_ch0-ch2.png'%SRC
    save_current_figure(plt_figure, clear=False)
    plt.show()
    logger.info('Created %s '%plt_figure)
    logger.info('done!') 
    
    
if RootAnalyseSpectra == True:
    out_root = os.path.join(ADVLAB_OUT,'%s_spectra_%s.root'%(SRC,label))
    f = ROOT.TFile(out_root, 'RECREATE')
    #c = gRootCanvas('spec', 'spec')                 
    h1 = build_spectrum('channel_0', e[0], TOT_NUM_EN_CH)  
    h2 = build_spectrum('channel_1', e[1], TOT_NUM_EN_CH)
    hh = ROOT.TH2F('Na','Na spec', 7500, 0, 15000, 7500, 0, 15000)
    for i,e0 in enumerate(e[0]):
            hh.Fill(e[0][i], e[1][i])
    #l_list = [h1, h2]
    #l = gRootLegend(l_list)
    h2.SetLineColor(2)                                                 
    h2.Draw()
    h1.SetLineColor(4)
    h1.Draw('SAME')
    #l.Draw('SAME')
    #c.Write()
    h1.Write()
    h2.Write()
    hh.Write()
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
"""
