

"""Functions to parse the CAEN output ascii file
"""

import numpy as np
import os
import ROOT
from ROOT import *

from advlab.utils.logging_ import logger
from advlab.utils.matplotlib_ import pyplot as plt


def parse_data(file_path):
    """Parse the ASCII file with events.   
       
       Arguments
       ---------
       file_path : str
           path and name of the file to process
    """
    ch = []
    t = []
    e = []
    f = open(file_path).readlines()
    lim = int(len(f)/3)
    for line in f[0:-1]:
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

def parse_coinc_data(file_path):
    """Parse the ASCII file with coincident pairs of events.

       Arguments     
       ---------                            
       file_path : str 
           path and name of the file of coincidences to process
    """
    t1 = []
    t2 = []
    e1 = []
    e2 = []
    for line in open(file_path):
        try:
            _t1, _e1, _t2, _e2 = [float(item) for item in line.split()]
            t1.append(_t1)
            t2.append(_t2)
            e1.append(_e1)
            e2.append(_e2)
        except:
            pass
    t1 = np.array(t1, dtype=np.int64)
    t2 = np.array(t2, dtype=np.int64)
    e1 = np.array(e1, dtype=np.int32)
    e2 = np.array(e2, dtype=np.int32)
    return t1, e1, t2, e2

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
