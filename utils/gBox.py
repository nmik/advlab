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
import math
import numpy as np

from advlab.utils.matplotlib_ import pyplot as plt
from advlab.utils.logging_ import logger

# Coordinates of the mobile RS in the Lab RS.
MOB_RS_Y = 15
MOB_RS_X = 0


class gBox:
    """Class implementing the position of the box in the lab reference system
       given the position of the center of the box in the mobile reference sys.
    """

    def __init__(self, xc, yc, x_side_lenght, y_side_lenght):
        """Constructor.
        
           Arguments
           --------- 
           xc : float
               The x coordinate of the center of the box in the mobile RS
           yc : float
               The y coordinate of the center of the box in the mobile RS
        """
        self.xc_lab = xc + MOB_RS_X
        self.yc_lab = yc + MOB_RS_Y
        self.lowlx = xc - x_side_lenght/2
        self.lowly = yc - y_side_lenght/2
        self.highlx = xc + x_side_lenght/2
        self.highly = yc + y_side_lenght/2
    
    def point_rotation(self, center, point, theta):
        """Rotates a point around another centerPoint. Angle is in degrees.
           Rotation is counter-clockwise
        """
        temp_point = point[0]-center[0], point[1]-center[1]
        temp_point = (temp_point[0]*np.cos(theta)-temp_point[1]*np.sin(theta),\
                      temp_point[0]*np.sin(theta)+temp_point[1]*np.cos(theta))
        temp_point = temp_point[0]+ center[0] , temp_point[1]+center[1]
        return temp_point

    def rotation(self, polygon, theta, degree=True):
        """Rotates the given polygon which consists of corners 
           represented as (x,y), around the ORIGIN, clock-wise, 
           theta degrees
        """
        logger.info('Rotating the box...')
        if degree == True:
            logger.info('Converting degrees to radians...')
            theta = np.radians(theta)
        #theta = theta + np.pi/2
        rotated_polygon = []
        for corner in polygon :
            center = MOB_RS_X, MOB_RS_X
            new_corner = self.point_rotation(center, corner, theta)
            rotated_polygon.append(new_corner)
        return rotated_polygon

    def y_translation(self, polygon, delta_y):
        """Function which translate along the y axis
        """
        new_polygon = []
        for corn in polygon:
            print corn[1]
            new_corn = corn[0], corn[1]+delta_y
            new_polygon.append(new_corn)
        return new_polygon

    def get_box_corners_coord(self):
        """
        """
        ll = (self.lowlx, self.lowly)
        hl = (self.highlx, self.lowly)
        hh = (self.highlx, self.highly)
        lh = (self.lowlx, self.highly)
        return [ll, hl, hh, lh]

    def print_center_coord(self):
        """
        """
        logger.info('Box center coordinates in the Lab RS: (%.2f,%.2f)' \
                    %(self.xc_lab, self.yc_lab))
        corn = self.get_box_corners_coord()
        logger.info('Corners coordinates: %s, %s, %s, %s'\
                    %(str(corn[0]),str(corn[1]),str(corn[2]),str(corn[3])))
    

    def line_in_box(self, y_ref, polygon):
        """
        """
        
        def line_intersection(line1, line2):
            """Return the intersection point between two lines if any
            """
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
            
            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                logger.info('Lines do not intersect!')
                return None
            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return x, y

        ref_line = [(-20, y_ref), (20, y_ref)]
        box_side1 = [polygon[0], polygon[1]]
        box_side2 = [polygon[1], polygon[2]]
        box_side3 = [polygon[2], polygon[3]]
        box_side4 = [polygon[3], polygon[0]]
        (x1, y1) = line_intersection(ref_line, box_side1)
        (x2, y2) = line_intersection(ref_line, box_side2)
        (x3, y3) = line_intersection(ref_line, box_side3)
        (x4, y4) = line_intersection(ref_line, box_side4)
        print (x1, y1), (x2, y2), (x3, y3), (x4, y4)
    
    def draw_line_inside_box(self, line):
        """
        """
        pass

    def draw_box(self, _corn, show=True):
        """
        """
        plt.xlim(-10.,10.)
        plt.ylim(-10.,10.)
        plt.plot([_corn[0][0],_corn[1][0]], [_corn[0][1],_corn[1][1]], \
                 'k-', lw=2, color='red')
        plt.plot([_corn[1][0],_corn[2][0]], [_corn[1][1],_corn[2][1]], \
                 'k-', lw=2, color='red')
        plt.plot([_corn[3][0],_corn[2][0]], [_corn[3][1],_corn[2][1]], \
                 'k-', lw=2, color='red')
        plt.plot([_corn[0][0],_corn[3][0]], [_corn[0][1],_corn[3][1]], \
                 'k-', lw=2, color='red')
        if show == True:
            plt.show()

def main():
    """Simple test code.
    """
    a = 5.
    b = 3.
    XC = a/2.
    YC = b/2.
    box = gBox(XC, YC, a, b)
    _corn = box.get_box_corners_coord()
    box.print_center_coord()
    _rot_corn = box.rotation(_corn, 20)
    _trans_rot_corn = box.y_translation(_rot_corn, 2.)

    box.line_in_box(1., _trans_rot_corn)
    
    plt.figure(figsize=(6, 6), dpi=80)
    plt.title('Box test')
    box.draw_box(_corn, show=False)
    box.draw_box(_rot_corn, show=False)
    box.draw_box(_trans_rot_corn, show=False)
    plt.show()
    

if __name__ == '__main__':
    main()
