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

import os
import numpy as np
import ROOT

from advlab.utils.logging_ import logger
from advlab.utils.gParsing import process_data
from advlab.utils.gAnalysisUtils import channel2energy
from advlab.utils.gAnalysisUtils import check_double_coinc
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT


TOT_NUM_EN_CH = 15000 #2**(14-1)



def draw_en_calib_curves(list_channel_names, list_channel_arrays, \
                         list_energy_arrays, show=True):
    """Function to draw the channel2energy calibration curves
    """
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('Na Energy Calibration')
    plt.xlabel('Channel')
    plt.ylabel('Energy [MeV]')
    calib_ch0_x = [1917,466,2721,6594,3504,6044,6843]
    calib_y = [0.356,0.03,0.511,1.27,0.662,1.17,1.33]
    calib_ch2_x = [2022,496,2846,6906,3674,6362,7214]
    for i, item in enumerate(list_energy_arrays):
        _channel, _index = np.unique(list_channel_arrays[i], return_index=True)
        item = item[_index]
        plt.plot(_channel, item, '-', label=list_channel_names[i])
    plt.plot(calib_ch0_x, calib_y, '.', color='red', label='ch0 benchmarks')
    plt.plot(calib_ch2_x, calib_y, '.', color='orange', label='ch2 benchmarks')
    plt.xlim(0.,TOT_NUM_EN_CH)
    plt.legend(loc='center left', shadow=False, fontsize='small')
    overlay_tag()
    plt_figure = 'Energy_Calibration_ch0-ch2.png'
    save_current_figure(plt_figure, clear=False)
    if show == True:
        plt.show()


infile_name = 'run_gr2_20160630_Na.dat'
infile = os.path.join(ADVLAB_DATA, infile_name)
ch, t, e = process_data(infile, [0,2])
_e0_mev = channel2energy(e[0], 0)
_e2_mev = channel2energy(e[1], 2)

# testing draw_en_calib_curves function
draw_en_calib_curves(['Channel 0','Channel 2'], [e[0],e[1]], \
                     [_e0_mev, _e2_mev], show=True)

