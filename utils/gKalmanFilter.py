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

class gExtendedKalmanFilter():
    """
    """
    def __init__(self, Y_list, ext_state_point, cov_matrix_list, X0):
        """Constructor
        """
        self.yk = 26.5 #[mm] in our ref sys, the top side of red box
        self.Y_list = Y_list
        self.extend = ext_state_point
        self.X0 = X0
        self.C0 = np.array([[1/1e7, 0],[0, 1/1e7]])
        logger.info('KF Extended in (%.2f, %.2f, %.2f)'%(self.extend[0][0], \
                                                      self.extend[1][0], \
                                                      self.extend[2][0]))
        self.Vk_list = cov_matrix_list
        
    def compute_vertex(self):
        """
        """
        def Hk_(xv, yv, uv):
            yk = self.yk
            return np.array([[xv + uv*(yk - yv)], [uv]])
        def Ak_():
            uke = self.extend[2][0]
            return np.array([[1, -uke], [0, 0]])
        def Bk_():
            yk = self.yk
            return np.array([[yk], [1]])
        def cke_():
            xke, yke, uke = self.extend[0][0], self.extend[1][0], self.extend[2][0]
            Bk = Bk_()
            c = np.subtract(Hk_(xke, yke, uke), np.dot(Bk, uke))
            return c

        exp_state = self.extend
        X0 = self.X0
        C0 = self.C0
        Vk_list = self.Vk_list
        

        InvC0 = np.linalg.inv(self.C0)
        InvCn = InvC0
        Xn_sum = np.array([[0], [0]])
        for i, (xk, uk) in enumerate(self.Y_list):
            Gk = np.linalg.inv(Vk_list[i])
            Hk = Hk_(exp_state[0][0], exp_state[1][0], exp_state[0][0])
            Ak = Ak_()
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            GkB = np.subtract(Gk, np.dot(Gk,np.dot(Bk,np.dot(Wk,np.dot(Bk.T,Gk)))))
            InvCn = np.add(InvCn, np.dot(Ak.T, np.dot(GkB, Ak)))
            Xn_sum = np.add(Xn_sum, np.dot(Ak.T,np.dot(GkB, np.subtract(pk, cke))))
        Cn = np.linalg.inv(InvCn)
        Xn = np.dot(Cn, np.add(np.dot(np.linalg.inv(self.C0), X0), Xn_sum))
        logger.info('Final status (xv, yv): (%.2f, %.2f)'%(Xn[0][0], Xn[1][0]))
        logger.info('Final cov: ((%.5f, %.5f),(%.5f, %.5f))' \
                    %(Cn[0][0], Cn[0][1], Cn[1][0], Cn[1][1]))
        
        Chi2n = np.dot(np.subtract(X0, Xn).T, np.dot(InvC0, np.subtract(X0, Xn)))
        for xk, uk in self.Y_list:
            Hk = Hk_(exp_state[0][0], exp_state[1][0], exp_state[0][0])
            Ak = Ak_()
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            GkB = np.subtract(Gk, np.dot(Gk,np.dot(Bk,np.dot(Wk,np.dot(Bk.T,Gk)))))
            qkn = np.dot(Wk, np.dot(Bk.T, np.dot(Gk, np.subtract(pk, \
                                    np.subtract(cke, np.dot(Ak, Xn))))))
            pkn = np.add(cke, np.add(np.dot(Ak, Xn), np.dot(Bk, qkn)))
            rkn = np.subtract(pk, pkn)
            Chi2n = np.add(Chi2n, np.dot(rkn.T, np.dot(Gk, rkn)))
        logger.info('Chi2 = %e '%Chi2n[0][0])

    def make_(X, P, Y, H): 
        """
        """
        IM = np.dot(H, X)
        IS = np.dot(H, np.dot(P, H.T)) 
        K = np.dot(P, np.dot(H.T, np.linalg.inv(IS))) 
        X = X + np.dot(K, (Y-IM))
        P = P - np.dot(K, np.dot(IS, K.T)) 
        return (X,P)

def main():
    """Simple function test
    """
    Y_list = [(1, 1./1), (20, 1./2), (-10, 1./0.5)]
    Vk_list = [np.array([[1., 0], [0, 4.]]), \
               np.array([[1., 0], [0, 4.]]), \
               np.array([[1., 0], [0, 4.]])]
    exp_point = np.array([[0.0], [0.0], [1.]])
    X0 = np.array([[0.], [0.]])
    KF = gExtendedKalmanFilter(Y_list, exp_point, Vk_list, X0)
    KF.compute_vertex()

    """
    X = np.array([[0.0], [0.0], [0.0]])
    d = 10000.
    P = np.array([[1./d, 0.0, 0.0],
                  [0.0, 1./d, 0.0],
                  [0.0, 0.0, 1./d]])
    A = np.array([[1.0, 0.0, 0.0],
                  [0.0, 1.0, 0.0],
                  [0.0, 0.0, 1.0]])
    #X_pred, P_pred = make_prediction(X, P, A)
    yp = 26.5 #always!!!
    xp = 20. #change
    up = 1. #change, defined as inverse of m
    uv = up
    Y = np.array([[xp], [up]])
    H = np.array([[1, uv, yp],
                  [0, 0, 1]])
    #list = make_update(X_pred, P_pred, Y, H)
    """


if __name__=='__main__':
    main()
