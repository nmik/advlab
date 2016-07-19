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


"""Imaging Configuration file
"""

import ROOT
import os
import numpy as np

from advlab import ADVLAB_DATA

SIDEX = 80
SIDEY = 55
GRAN = 10
OUTFILE = 'redbox_imaging.root'
KF_OUTFILE = 'KF_vertexing.png'

INFILES = np.array([os.path.join(ADVLAB_DATA, 'scan_0_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_0_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_120_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_160_125.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_40.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_45.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_50.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_55.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_60.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_65.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_70.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_75.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_80.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_85.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_90.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_95.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_20.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_25.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_30.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_35.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_100.dat'),
                    #os.path.join(ADVLAB_DATA, 'scan_200_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_40_130.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_80_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_240_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_10.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_280_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_40.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_45.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_50.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_55.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_60.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_65.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_70.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_75.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_80.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_85.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_90.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_95.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_15.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_20.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_25.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_30.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_35.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_100.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_105.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_110.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_115.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_120.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_125.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_130.dat'),
                    os.path.join(ADVLAB_DATA, 'scan_320_135.dat'),
                ])
