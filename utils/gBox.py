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

"""Utilities to make the Imaging
"""

import os
import math
import numpy as np
import ROOT
from scipy.interpolate import griddata

from advlab import ADVLAB_OUT
from advlab import ADVLAB_DATA
from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.matplotlib_ import overlay_tag, save_current_figure
from advlab.utils.logging_ import logger
from advlab.utils.gAnalysisUtils import check_double_coinc
from advlab.utils.gAnalysisUtils import channel2energy
from advlab.utils.gParsing import process_data
from advlab.utils.gParsing import parse_coinc_data

# Coordinates of the mobile RS in the Lab RS.
MOB_RS_Y = 150 #mm
MOB_RS_X = 0

def get_m_q(line):
    m = (line[1][1]-line[0][1])/(line[1][0]-line[0][0])
    q = line[0][1]-m*line[0][0]
    return m, q

def mkline(ybox, theta):
    line = (-39.5, ybox), (39.5, ybox)
    r_line = rotate_line(line, theta)
    return r_line

def rotate_line(line, theta):
    """Rotate a line around its center 
    """
    if theta == 0:
        return line
    #line_c = ((line[0][0]+line[1][0])/2, (line[0][1]+line[1][1])/2)
    theta = np.radians(theta)
    #linet = ((line[0][0]-line_c[0],line[0][1]-line_c[1]),
    #         (line[1][0]-line_c[0],line[1][1]-line_c[1]))
    new_linet = (np.cos(-theta)*line[0][0]-np.sin(-theta)*line[0][1],\
                np.sin(-theta)*line[0][0]+np.cos(-theta)*line[0][1]),\
        (np.cos(-theta)*line[1][0]-np.sin(-theta)*line[1][1],\
         np.sin(-theta)*line[1][0]+np.cos(-theta)*line[1][1])
    #new_line = ((new_linet[0][0]+line_c[0],new_linet[0][1]+line_c[1]),
    #         (new_linet[1][0]+line_c[0],new_linet[1][1]+line_c[1]))
    return new_linet

def imaging(lines_list, rate_list, x_side, y_side, gran=1, \
            outfile='imaging.root'):
    """perform the imaging of the gamma-ray emission from sources 
       inside the red box
    """
    f = ROOT.TFile(os.path.join(ADVLAB_OUT,outfile), 'RECREATE')
    xh_low, xh_high = -x_side/2, x_side/2
    yh_low, yh_high = -y_side/2, y_side/2
    xh_bins = np.linspace(xh_low, xh_high, (x_side/5)*2*gran)
    yh_bins = np.linspace(yh_low, yh_high, (y_side/5)*2*gran)
    xh_nbins = len(xh_bins)
    yh_nbins = len(yh_bins)
    hh = ROOT.TH2F('pet', 'Sources imaging', xh_nbins, xh_low, xh_high, \
                   yh_nbins, yh_low, yh_high)
    hh.GetXaxis().SetTitle('x [mm]')
    hh.GetYaxis().SetTitle('y [mm]')
    for i in range(-xh_nbins/2, xh_nbins/2):
        for j in range(-yh_nbins/2, yh_nbins/2):
            hh.Fill(i,j,1)
    for i,line in enumerate(lines_list):
        m, q = get_m_q(line)
        _x = xh_bins
        _y = _x*m + q
        _mask = (_y<=yh_high)&(_y>=yh_low)
        _x = _x[_mask]
        _y = _y[_mask]
        w = rate_list[i]
        for i, x in enumerate(_x):
            bx = hh.GetXaxis().FindBin(x)
            by = hh.GetYaxis().FindBin(_y[i])
            new_w = hh.GetBinContent(bx,by)+w
            hh.SetBinContent(bx,by,new_w)
            for zx in range(bx-gran, bx+gran):
                if zx == 0 or zx < 0:
                    continue
                for zy in range(by-gran, by+gran):
                    if zy == 0 or zy < 0:
                        continue
                    new_w = hh.GetBinContent(zx,zy)+w
                    hh.SetBinContent(zx,zy,new_w)
    hh.Draw('COLZ')
    hh.Write()
    f.Close()
    logger.info('Created %s'%os.path.join(ADVLAB_OUT,outfile))
     
def build_rate_hist(th_label, infile_list, yref_list):
    """
    """
    rate_list = []
    ncoinc_list = []
    for f in infile_list:
        ch, t, e = process_data(f, [0,2])
        coinc_file_name = os.path.basename(f.replace('.dat', '_COINC.dat'))
        coinc_file = os.path.join(ADVLAB_DATA, coinc_file_name)
        check_double_coinc(t[0], t[1], e[0], e[1], 10, coinc_file)
        t1, e1, t2, e2 = parse_coinc_data(coinc_file)
        e1_mev = channel2energy(e1, 0)
        e2_mev = channel2energy(e2, 2)
        _mask0 = (e1_mev < 1.) & (e1_mev > 0.1) 
        _mask2 = (e2_mev < 1.) & (e2_mev > 0.1)
        _mask = _mask0 & _mask2
        t1_w, e1_mev_w, t2_w, e2_mev_w = t1[_mask], e1_mev[_mask], t2[_mask],\
                                 e2_mev[_mask]
        logger.info('%i/%i coincidences in the selected energy window' %\
                    (len(t1_w),len(t1)))
        num_coinc = len(t1_w)
        time_interval = (t[0][-1] - t[0][0])/10000000
        logger.info('effective time interval = %i s'%time_interval)
        rate = float(num_coinc)/time_interval
        logger.info('Rate = %.5f s^{-1}'%rate)
        rate_list.append(rate)
        ncoinc_list.append(num_coinc)
    root_file_name = os.path.join(ADVLAB_OUT,'y_scan.root')
    if not os.path.exists(root_file_name):
        root_file = ROOT.TFile(root_file_name,'RECREATE')
    else:
        root_file = ROOT.TFile(root_file_name,'UPDATE')
    nbins = len(yref_list) - 1
    y_min, y_max = 67.5 - yref_list[0], 67.5 - yref_list[-1]
    h = ROOT.TH1F(th_label, th_label, nbins, y_min , y_max)
    ybox_list = []
    for i, c in enumerate(ncoinc_list):
        y = 67.5 - yref_list[i]
        ybox_list.append(y)
        h.Fill(y, c)
    h.GetXaxis().SetTitle('y [mm]')
    h.GetYaxis().SetTitle('Number of Coincidences')
    h.Write()
    root_file.Close()
    logger.info('Created %s'%root_file_name)
    return ybox_list, ncoinc_list

def point_rotation(center, point, theta):
    """Rotates a point around another centerPoint. Angle is in degrees.
       Rotation is counter-clockwise
    """
    temp_point = point[0]-center[0], point[1]-center[1]
    temp_point = (temp_point[0]*np.cos(theta)-temp_point[1]*np.sin(theta),\
                  temp_point[0]*np.sin(theta)+temp_point[1]*np.cos(theta))
    temp_point = temp_point[0]+ center[0] , temp_point[1]+center[1]
    return temp_point

def line_lab2box(_x, _y, box_origin_in_lab, theta):
        """
        """
        points = [x,y in zip(_x, _y)]
        print points
        rot_points = []
        for p in points:
            r_p = point_rotation((MOB_RS_X, MOB_RS_Y), p, -theta)
            rot_points.append(r_p)
        print rot_points
        _rx = [x[0] for x in rot_point if x[0]]
        _ry = [x[1] for x in rot_point if x[1]]
        print _rx, _ry
        

class gBox:
    """Class implementing the position of the box in the lab reference system
       given the position of the center of the box in the mobile reference sys.
    """

    def __init__(self, xc, yc, x_side_lenght, y_side_lenght, theta):
        """Constructor.
        
           Arguments
           --------- 
           xc : float
               The x coordinate of the center of the box in the mobile RS
           yc : float
               The y coordinate of the center of the box in the mobile RS
        """
        self.theta = theta
        self.xc = xc
        self.yc = yc
        self.xc_boxrs = x_side_lenght/2
        self.xc_boxrs = y_side_lenght/2
        self.x_side_lenght = x_side_lenght
        self.y_side_lenght = y_side_lenght
        self.xc_lab = xc + MOB_RS_X
        self.yc_lab = yc + MOB_RS_Y
        self.ll = point_rotation((MOB_RS_X, MOB_RS_X), \
                                      (self.xc_lab - x_side_lenght/2, \
                                       self.yc_lab - y_side_lenght/2), theta)
        self.hl = point_rotation((MOB_RS_X, MOB_RS_X), \
                                      (self.xc_lab + x_side_lenght/2, \
                                       self.yc_lab - y_side_lenght/2), theta)
        self.hh = point_rotation((MOB_RS_X, MOB_RS_X), \
                                      (self.xc_lab + x_side_lenght/2, \
                                       self.yc_lab +  y_side_lenght/2), theta)
        self.lh = point_rotation((MOB_RS_X, MOB_RS_X), \
                                      (self.xc_lab - x_side_lenght/2, \
                                       self.yc_lab + y_side_lenght/2), theta)
        

    def rotation(self, new_theta, degree=True):
        """Rotates the given polygon which consists of corners 
           represented as (x,y), around the ORIGIN, clock-wise, 
           theta degrees
        """
        logger.info('Rotating the box of %.2f degree...'%new_theta)
        if degree == True:
            logger.info('Converting degrees to radians...')
            new_theta = np.radians(new_theta)
        new_box = gBox(self.xc, self.yc, self.x_side_lenght, \
                       self.y_side_lenght, new_theta)
        new_box.print_center_coord()
        return new_box

    def y_translation(self, delta_y):
        """Function which translate along the y axis
        """
        logger.info('Translating the box along the y axis of %.2f units' \
                    %delta_y)
        new_yc = self.yc + delta_y
        new_box = gBox(self.xc, new_yc, self.x_side_lenght, \
                       self.y_side_lenght, self.theta)
        new_box.print_center_coord()
        return new_box

    def get_box_corners_coord(self):
        """
        """
        ll = self.ll
        hl = self.hl
        hh = self.hh
        lh = self.lh
        return [ll, hl, hh, lh]

    def print_center_coord(self):
        """
        """
        logger.info('Box center coordinates in the Lab RS: (%.2f,%.2f)' \
                    %(self.xc_lab, self.yc_lab))
        corn = self.get_box_corners_coord()
        logger.info('Corners coordinates:')
        logger.info('(%.2f,%.2f), (%.2f,%.2f), (%.2f,%.2f), (%.2f,%.2f)'\
                    %(self.ll[0], self.ll[1], self.hl[0], self.hl[1], \
                      self.hh[0], self.hh[1], self.lh[0], self.lh[1]))
    

    def line_in_box(self, y_ref):
        """
        """
        
        def line_intersection(line, box_side):
            """Return the intersection point between two lines if any
            """
            xdiff = (box_side[0][0] - box_side[1][0], line[0][0] - line[1][0])
            ydiff = (box_side[0][1] - box_side[1][1], line[0][1] - line[1][1])
            
            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                logger.info('Lines do not intersect!')
                return None, None
            d = (det(*box_side), det(*line))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return x, y

        ref_line = [(-20, y_ref), (20, y_ref)]
        box_side1 = [self.ll, self.hl]
        box_side2 = [self.hl, self.hh]
        box_side3 = [self.hh, self.lh]
        box_side4 = [self.lh, self.ll]
        print 'side 1'
        x1, y1 = line_intersection(ref_line, box_side1)
        print 'side 2'
        x2, y2 = line_intersection(ref_line, box_side2)
        print 'side 3'
        x3, y3 = line_intersection(ref_line, box_side3)
        print 'side 4'
        x4, y4 = line_intersection(ref_line, box_side4)
        intersec = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        _x = [x[0] for x in intersec if x[0] is not None]
        _y = [x[1] for x in intersec if x[1] is not None]
        return _x, _y
        

    def draw_box(self, show=True):
        """
        """
        plt.xlim(-15.,15.)
        plt.ylim(0., 30.)
        plt.plot((self.ll[0], self.hl[0]), (self.ll[1], self.hl[1]), \
                 'k-', lw=2, color='red')
        plt.plot((self.hl[0], self.hh[0]), (self.hl[1], self.hh[1]), \
                 'k-', lw=2, color='red')
        plt.plot((self.hh[0], self.lh[0]), (self.hh[1], self.lh[1]), \
                 'k-', lw=2, color='red')
        plt.plot((self.lh[0], self.ll[0]), (self.lh[1], self.ll[1]), \
                 'k-', lw=2, color='red')
        if show == True:
            plt.show()

def main():
    """Simple test code.
    """
    a = 5.
    b = 3.
    XC = 0.
    YC = 0.
    box = gBox(XC, YC, a, b, 0.)
    _corn = box.get_box_corners_coord()
    box.print_center_coord()
    plt.figure(figsize=(6, 6), dpi=80)
    box.draw_box(show=False)
    box_r = box.rotation(20.)
    box_t = box_r.y_translation(5.)
    box_r.draw_box(show=False)
    box_t.draw_box(show=False)
    _x, _y = box.line_in_box(150)
    line_lab2box(_x, _y, (-a/2, MOB_RS_Y-b/2), 0.)
    plt.plot(_x, _y)
    plt.title('Box test')
    plt.show()

if __name__ == '__main__':
    main()
