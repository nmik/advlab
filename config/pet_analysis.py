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

from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import calibrate_energy
from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
from advlab import ADVLAB_DATA
from advlab import ADVLAB_OUT


TOT_NUM_EN_CH = 15000 #2**(14-1)
DATA_FILE_NAME = {'delay25ns':'run_gr2_20160630_delay25ns.dat',
                  'delay25ns_3h':'run_gr2_20160630_delay25ns_3h.dat',
                  'delay30ns':'run_gr2_20160630_delay30ns.dat',
                  'first_att':'run_gr2_20160630_coinc_0.dat'}


def draw_en_calib_curves(list_channel_arrays, list_energy_arrays, show=True):
    plt.figure(figsize=(10, 7), dpi=80)
    plt.title('Na Energy Calibration')
    plt.xlabel('Channel')
    plt.ylabel('Energy [MeV]')
    for i, item in enumerate(list_energy_arrays):
        _channel, _index = np.unique(list_channel_arrays[i], return_index=True)
        item = item[_index]
        plt.plot(_channel, item)
    plt.xlim(0., TOT_NUM_EN_CH)
    overlay_tag()
    plt_figure = 'Energy_Calibration_ch0-ch2.png'
    save_current_figure(plt_figure, clear=False)
    if show == True:
        plt.show()


label = 'delay25ns_3h'
outfile_name = DATA_FILE_NAME[label]
outfile = os.path.join(ADVLAB_DATA, outfile_name)
ch, t, e = process_data(outfile, [0,2])
_energies_ch0 = calibrate_energy(e[0], (2900,0.511), (6900,1.27))
_energies_ch2 = calibrate_energy(e[1], (2800,0.511), (6700,1.27))

draw_en_calib_curves([e[0],e[1]], [_energies_ch0, _energies_ch2])
