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
    IM = np.dot(H, X)
    print H
    print H.T
    print np.dot(P, H.T)
    IS = np.dot(H, np.dot(P, H.T)) 
    print IS
    print np.linalg.inv(IS)
    K = np.dot(P, np.dot(H.T, np.linalg.inv(IS))) 
    X = X + np.dot(K, (Y-IM))
    P = P - np.dot(K, np.dot(IS, K.T)) 
    return (X,P)
   
    
    
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
    yp = 26.5 #always!!!
    xp = 20. #change
    up = 1. #change, defined as inverse of m
    uv = up
    Y = np.array([[xp], [up]])
    H = np.array([[1, uv, yp],
                  [0, 0, 1]])
    list = make_update(X_pred, P_pred, Y, H)
    for item in list:
        print item


if __name__=='__main__':
    main()
