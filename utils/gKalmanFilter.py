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
from advlab.utils.matplotlib_ import pyplot as plt

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
        #self.C0 = np.array([[1e7, 0],[0, 1e7]])
        self.C0 = np.array([[1./1e7, 0],[0, 1./1e7]])
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
            return np.array([[1., -uke], [0., 0.]])
        def Bk_():
            yk = self.yk
            return np.array([[yk], [1]])
        def cke_():
            xke, yke, uke = self.extend[0][0], self.extend[1][0], \
                            self.extend[2][0]
            Bk = Bk_()
            c = np.subtract(Hk_(xke, yke, uke), np.dot(Bk, uke))
            return c

        X0 = self.X0
        C0 = self.C0
        Vk_list = self.Vk_list
        

        InvC0 = np.linalg.inv(self.C0)
        print InvC0
        InvCn = InvC0
        Xn_sum = np.array([[0], [0]])
        for i, (xk, uk) in enumerate(self.Y_list):
            Gk = np.linalg.inv(Vk_list[i])
            Ak = Ak_()
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            GkB = np.subtract(Gk, np.dot(Gk,np.dot(Bk,np.dot(Wk, \
                                                             np.dot(Bk.T,Gk)))))
            InvCn = np.add(InvCn, np.dot(Ak.T, np.dot(GkB, Ak)))
            Xn_sum = np.add(Xn_sum, np.dot(Ak.T,np.dot(GkB, \
                                                       np.subtract(pk, cke))))
        Cn = np.linalg.inv(InvCn)
        Xn = np.dot(Cn, np.add(np.dot(np.linalg.inv(self.C0), X0), Xn_sum))
        logger.info('Final status (xv, yv): (%.2f, %.2f)'%(Xn[0][0], Xn[1][0]))
        logger.info('Final cov: ((%.5f, %.5f),(%.5f, %.5f))' \
                    %(Cn[0][0], Cn[0][1], Cn[1][0], Cn[1][1]))
        
        Chi2n = np.dot(np.subtract(X0, Xn).T, np.dot(InvC0, \
                                                     np.subtract(X0, Xn)))
        for xk, uk in self.Y_list:
            Ak = Ak_()
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            GkB = np.subtract(Gk, np.dot(Gk,np.dot(Bk,np.dot(Wk,\
                                                             np.dot(Bk.T,Gk)))))
            qkn = np.dot(Wk, np.dot(Bk.T, np.dot(Gk, np.subtract(pk, \
                                    np.subtract(cke, np.dot(Ak, Xn))))))
            pkn = np.add(cke, np.add(np.dot(Ak, Xn), np.dot(Bk, qkn)))
            rkn = np.subtract(pk, pkn)
            Chi2n = np.add(Chi2n, np.dot(rkn.T, np.dot(Gk, rkn)))
            if Chi2n[0][0] > 30:
                logger.info('Chi2 > 30. Stopping here, return None!')
                return None, None, None
        logger.info('Chi2 = %e '%Chi2n[0][0])
        return Xn[0][0], Xn[1][0], Chi2n[0][0]

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
    Y_list = [(-31.581470203746566, -1.19175359259421), 
              (-19.904064167060497, -0.17632698070846503), 
              (-13.567731325956204, 0.5773502691896254), 
              (14.332063612285729, 2.7474774194546212), 
              (-43.570107613916612, -2.7474774194546225), 
              #(7.7942286340599374, -0.57735026918962651), 
              (-19.981197226489204, -0.57735026918962651),
              #(24.981197226489204, 0.17632698070846453), 
              (-14.981197226489204, 0.17632698070846453),
              (0.46699366653830859, 1.1917535925942091)]
    Vk_list = [np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]]), 
               np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]]),
               np.array([[1., 0], [0, 1.]])]
    exp_point = np.array([[-20.0], [10.0], [0.0]])
    X0 = np.array([[0.], [0.]])
    KF = gExtendedKalmanFilter(Y_list, exp_point, Vk_list, X0)
    xv, yv, chi2 = KF.compute_vertex()


    xk_list1 = np.array([p[0] for p in Y_list])
    m_list = np.array([1./p[1] for p in Y_list])
    yk_list1 = np.array([26.5]*len(xk_list1))
    xk_list2 = np.array([30., -15., -30., -30., 10., 0., -25., -30.])
    yk_list2 = np.add(xk_list2*m_list,(np.subtract(yk_list1, m_list*xk_list1)))
    for i in range(0, len(xk_list1)):
        plt.plot((xk_list1[i], xk_list2[i]), (yk_list1[i], yk_list2[i]))
    plt.plot(xk_list1, yk_list1, 'o')
    plt.plot(xk_list2, yk_list2, 'o')
    vertex = plt.Circle((xv, yv), chi2/2, color='r')
    ax = plt.subplot()
    ax.add_artist(vertex)
    plt.show()
    


if __name__=='__main__':
    main()
