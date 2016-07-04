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


"""Class to define all the Extended Kalman FIlter (EKF) steps
   for a vertex positin estimation.
"""


import os
import numpy as np
from advlab.utils.logging_ import logger


class gTrueState:
    """
    """

    def __init__(self, seed):
        """
        """
        pass
        
    def make_prediction(self):
        """
        """
        pass

    def update(self, prediction, measurement):
        """
        """
        pass

    def make_smoothing(self):
        """
        """
        pass


def main():
    """Simple function test
    """
    seed = x0, y0
    state_var = xk_ref, yk_ref, uk_ref
    state = gTrueState(state_var)
    predict = state.make_prediction()
    update = predict.update()


if __name__=='__main__':
    main()
