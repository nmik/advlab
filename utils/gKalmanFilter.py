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
        self.xk = 0.
        self.Y_list = Y_list
        self.extend = ext_state_point
        self.X0 = X0
        self.InvC0 = np.array([[1e-10, 0.],[0., 1e-10]])
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
        def Ak_(uk):
            #uke = self.extend[2][0]
            return np.array([[1., -uk], [0., 0.]])
        def Bk_():
            yk = self.yk
            return np.array([[yk],[1]])
        def cke_():
            xke, yke, mke = self.extend[0][0], self.extend[1][0], \
                            self.extend[2][0]
            Bk = Bk_()
            c = np.subtract(Hk_(xke, yke, mke), np.dot(Bk, mke))
            return c

        X0 = self.X0
        Vk_list = self.Vk_list        
        InvC0 = self.InvC0
        InvCn_sum = np.array([[0., 0.], [0., 0.]])
        Xn_sum = np.array([[0.], [0.]])
        logger.info('Computing vertex position...')
        for i, (xk, uk) in enumerate(self.Y_list):
            Gk = np.linalg.inv(Vk_list[i])
            Ak = Ak_(uk)
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            GkB = np.subtract(Gk, np.dot(Gk,np.dot(Bk,np.dot(Wk, \
                                                             np.dot(Bk.T,Gk)))))
            InvCn_sum = np.add(InvCn_sum, np.dot(Ak.T, np.dot(GkB, Ak)))
            Xn_sum = np.add(Xn_sum, np.dot(Ak.T,np.dot(GkB, \
                                                       np.subtract(pk, cke))))
        Cn = np.linalg.inv(np.add(InvC0, InvCn_sum))
        Xn = np.dot(Cn, np.add(np.dot(InvC0, X0), Xn_sum))
        logger.info('Final status (xv, yv): (%.2f, %.2f)'%(Xn[0][0], Xn[1][0]))
        logger.info('computing Chi2...')
        Chi2n = np.dot(np.subtract(X0, Xn).T, np.dot(InvC0, \
                                                     np.subtract(X0, Xn)))
        for i, (xk, uk) in enumerate(self.Y_list):
            Gk = np.linalg.inv(Vk_list[i])
            Ak = Ak_(uk)
            Bk = Bk_()
            cke = cke_()
            pk = np.array([[xk],[uk]])
            Wk = np.linalg.inv(np.dot(Bk.T, np.dot(Gk, Bk)))
            qkn = np.dot(Wk, np.dot(Bk.T, np.dot(Gk, np.subtract(np.subtract(pk, \
                                                          cke), np.dot(Ak, Xn)))))
            pkn = np.add(cke, np.add(np.dot(Ak, Xn), np.dot(Bk, qkn)))
            rkn = np.subtract(pk, pkn)
            Chi2n = np.add(Chi2n, np.dot(rkn.T, np.dot(Gk, rkn)))
            if Chi2n[0][0] > 30:
                logger.info('Chi2 > 30. Stopping here, return None!')
                return None, None, None
        logger.info('Chi2 = %e '%Chi2n[0][0])
        return Xn[0][0], Xn[1][0], Chi2n[0][0]


def main():
    """Simple function test
    """
    Y_list = [(-23.232415497817247, -1.19175359259421), 
              (-21.987611888311637, -0.17632698070846506), 
              (-13.604120186609292, 0.57735026918962551), 
              (9.2574382249278635, 2.7474774194546212), 
              (-45.783313809834844, -2.747477419454623), 
              (-26.871755786442005, -0.57735026918962651), 
              (-19.576575935508423, 0.17632698070846456),
              (4.9874225727354045, 1.1917535925942091)]
    Vk_list = [np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]]), 
               np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]]),
               np.array([[2, 0], [0, 6.22**2]])]
    exp_point = np.array([[10.0], [01.0], [1.0]])
    X0 = np.array([[0.], [0.]])
    KF = gExtendedKalmanFilter(Y_list, exp_point, Vk_list, X0)
    xv, yv, chi2 = KF.compute_vertex()

    xk_list1 = np.array([p[0] for p in Y_list])
    u_list = np.array([p[1] for p in Y_list])
    yk_list1 = np.array([26.5]*len(xk_list1))
    yk_list2 = np.array([-26.5]*len(xk_list1))
    xk_list2 = np.subtract(yk_list2, np.add(yk_list1,u_list*xk_list1))*u_list
    for i in range(0, len(xk_list1)):
        plt.plot((xk_list1[i], xk_list2[i]), (yk_list1[i], yk_list2[i]))
    plt.plot(xk_list1, yk_list1, 'o')
    plt.plot(xk_list2, yk_list2, 'o')
    print '(xv,yv):', xv, yv
    vertex = plt.Circle((xv, yv), 1., color='r')
    ax = plt.subplot()
    ax.add_artist(vertex)
    plt.xlim(-40,40)
    plt.ylim(-26.5, 26.5)
    plt.show()
    


if __name__=='__main__':
    main()
