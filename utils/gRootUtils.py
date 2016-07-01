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


"""root configuration utils
"""

import os
import array
import ROOT

from advlab.utils.__root__ import *
from advlab.utils.logging_ import logger, abort


class gRootObject:

    """ Generic ROOT object wrapper.
    
    This class only defines an init(**kwargs) method that loops over the
    keyword arguments and attempts at calling the appropriate underlying class
    methods.

    The basic idea is that, whenever a ROOT object has a "SetXXX(val)" method
    you can invoke it by passing the keyword argument "XXX = val".
    """

    DEFAULT_OPTIONS = {}

    def __init__(self, **kwargs):
        """ Workhorse class method.
        """
        self.setup(**kwargs)
        for (key, value) in self.DEFAULT_OPTIONS.items():
            if not kwargs.has_key(key):
                kwargs[key] = value
        for (key, value) in kwargs.items():
            try:
                if isinstance(value, str):
                    value = '"%s"' % value
                exec('self.Set%s(%s)' % (key, value))
            except AttributeError, e:
                logger.warn('Cannot process kwarg "%s = %s" (%s).' %\
                                (key, value, e))

    def setup(self, **kwargs):
        """ Generic hook to allow subclasses to perform specific operations
        before the kwargs are actually processed by the init() method.
        """
        pass


class gRootLegend(ROOT.TLegend):

    """ Wrapper around the ROOT.TLegend class.
    """
    
    def __init__(self, entries = [], left = 0.66, top = 0.96, width = 0.3,
                 rowHeight = 0.055):
        """ Constructor.
        """
        x1 = left
        y1 = top
        x2 = left + width
        y2 = top
        ROOT.TLegend.__init__(self, x1, y1, x2, y2)
        #TEXT_FONT, LEGEND_TEXT_SIZE = 42, 0.06
        self.SetTextFont(TEXT_FONT)
        self.SetTextSize(LEGEND_TEXT_SIZE)
        self.SetFillStyle(0)
        self.SetBorderSize(0)
        self.__RowHeight = rowHeight
        for entry in entries:
            self.AddEntry(entry)

    def AddEntry(self, entry, label = None, opts = 'lpf'):
        """ Overloaded AddEntry() class method.
        """
        if label is None:
            label = entry.GetTitle()
        self.SetY1(self.GetY1() - self.__RowHeight)
        ROOT.TLegend.AddEntry(self, entry, label, opts)


class gRootCanvas(ROOT.TCanvas, gRootObject):
    """ Small wrapper around the TCanvas object.
    """

    DEFAULT_OPTIONS = {'Gridx': True,
                       'Gridy': True}

    def __init__(self, name, title = None, **kwargs):
        """ Overloaded constructor.
        """
        ROOT.TCanvas.__init__(self, name, title or name)
        gRootObject.__init__(self, **kwargs)
        if kwargs.get('colz', False):
            if kwargs.get('ztitle', False):
                self.SetRightMargin(0.16)
            else:
                self.SetRightMargin(0.12)

            
    def annotate(self, x, y, text, **kwargs):
        """ Draw some text on the canvas.
        """
        ndc = kwargs.get('ndc', True)
        align = kwargs.get('align', 11)
        size = kwargs.get('size', TEXT_SIZE)
        color = kwargs.get('color', ROOT.kBlack)
        angle = kwargs.get('angle', 0)
        self.cd()
        label = ROOT.TLatex(x, y, text)
        if ndc:
            label.SetNDC(True)
        label.SetTextAlign(align)
        label.SetTextSize(size)
        label.SetTextColor(color)
        label.SetTextAngle(angle)
        label.Draw()
        store(label)
        ROOT.TCanvas.Update(self)

    def save(self, outputFolder = None, formats = ['pdf', 'eps', 'png']):
        """ Save the canvas in different formats using the canvas name to
        define the file name.
        """
        for format in formats:
            filePath = '%s.%s' % (self.GetName(), format)
            if outputFolder is not None:
                filePath = os.path.join(outputFolder, filePath)
            self.SaveAs(filePath)

    def saveformat(self, outputFolder = None, format = 'pdf'):
        """ Save the canvas in different formats using the canvas name to
        define the file name.
        """
        filePath = '%s.%s' % (self.GetName(), format)
        if outputFolder is not None:
            filePath = os.path.join(outputFolder, filePath)
        self.SaveAs(filePath)

    def drawframe(self, xmin, xmax, ymin, ymax):
        """ draws a user supplied frame in the canvas
        """
        frame = ROOT.TH2F(self.GetName(), self.GetName(),
                          1, xmin, xmax, 1, ymin, ymax)
        frame.Draw()
        store(frame)


if __name__ == '__main__':
    print 'ok!'
