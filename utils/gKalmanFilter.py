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

def make_prediction(X, P, A):
    """
    """
    X = np.dot(A, X)
    P = np.dot(A, np.dot(P, A.T))
    return(X,P)

def make_update(X, P, Y, H): 
    """
    """
    IM = dot(H, X)
    IS = dot(H, dot(P, H.T)) 
    K = dot(P, dot(H.T, inv(IS))) 
    X = X + dot(K, (Y-IM))
    P = P - dot(K, dot(IS, K.T)) 
    LH = gauss_pdf(Y, IM, IS) 
    return (X,P,K,IM,IS,LH)
   
    
    
def make_smoothing(self):
    """
    """
    pass


def main():
    """Simple function test
    """
    X = np.array([[0.0], [0.0], [0.0]])
    P = np.array([[0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0],
                  [0.0, 0.0, 0.0]])
    A = np.array([[1.0, 1.0, 1.0],
                  [1.0, 1.0, 1.0],
                  [1.0, 1.0, 1.0]])
    X_pred, P_pred = make_prediction(X, P, A)
    print X_pred 
    print P_pred
    Y = np.array([[10.], [26.5], [1.]])
    H = np.array([[None, None, None],
                  [None, None, None],
                  [None, None, None]])
    R =
    list = make_update(X_pred, P_pred, )


if __name__=='__main__':
    main()
