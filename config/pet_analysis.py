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
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import channel2energy
from advlab.utils.gParsing import check_double_coinc
from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT


TOT_NUM_EN_CH = 15000 #2**(14-1)
DATA_FILE_NAME = {'delay25ns':'run_gr2_20160630_Na.dat',
                  'delay25ns_3h':'run_gr2_20160630_delay25ns_3h.dat'}


def draw_en_calib_curves(list_channel_names, list_channel_arrays, \
                         list_energy_arrays, show=True):
    """Function to draw the channel2energy calibration curves
    """
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('Na Energy Calibration')
    plt.xlabel('Channel')
    plt.ylabel('Energy [MeV]')
    for i, item in enumerate(list_energy_arrays):
        _channel, _index = np.unique(list_channel_arrays[i], return_index=True)
        item = item[_index]
        plt.plot(_channel, item, '.', label=list_channel_names[i])
    plt.xlim(0.,TOT_NUM_EN_CH)
    plt.legend(loc='center left', shadow=False, fontsize='small')
    overlay_tag()
    plt_figure = 'Energy_Calibration_ch0-ch2.png'
    save_current_figure(plt_figure, clear=False)
    if show == True:
        plt.show()


label = 'delay25ns'
outfile_name = DATA_FILE_NAME[label]
outfile = os.path.join(ADVLAB_DATA, outfile_name)
ch, t, e = process_data(outfile, [0,2])
calib_ch0 = [(1917,0.356),(466,0.08),(2721,0.0511),(6594,1.27),(3504,0.662),\
             (6044,1.17),(6843,1.33)]
calib_ch2 = [(2022,0.356),(496,0.08),(2846,0.0511),(6906,1.27),(3674,0.662),\
             (6362,1.17),(7214,1.33)]
_energies_ch0 = channel2energy(e[0], calib_ch0)
_energies_ch2 = channel2energy(e[1], calib_ch2)
print _energies_ch0
print _energies_ch2
# testing draw_en_calib_curves function
draw_en_calib_curves(['Channel 0','Channel 2'], [e[0],e[1]], \
                     [_energies_ch0, _energies_ch2], show=True)

