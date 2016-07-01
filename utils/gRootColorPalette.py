


import array
import ROOT


class gRootColorPalette:

    """ Set a color palette from a given RGB list.
    stops, red, green and blue should all be lists of the same length
    from http://ultrahigh.org/2007/08/20/making-pretty-root-color-palettes/
    """
   
    def __init__(self, name, stops, red, green, blue):
        """
        """
        self.Name = name
        self.Stops = array.array('d', stops)
        self.Red = array.array('d', red)
        self.Green = array.array('d', green)
        self.Blue = array.array('d', blue)

    def __len__(self):
        """
        """
        return len(self.Stops)

    def createGradientColorTable(self, rootStyle, contours = 250):
        """
        """
        ROOT.TColor.CreateGradientColorTable(len(self), self.Stops, self.Red,
                                             self.Green, self.Blue, contours)
        rootStyle.SetNumberContours(contours)



DEFAULT_COLOR_PALETTE = gRootColorPalette('Default',
                                          [0.00, 0.34, 0.61, 0.84, 1.00],
                                          [0.00, 0.00, 0.87, 1.00, 0.51],
                                          [0.00, 0.81, 1.00, 0.20, 0.00],
                                          [0.51, 1.00, 0.12, 0.00, 0.00])


if __name__ == '__main__':
    DEFAULT_COLOR_PALETTE.createGradientColorTable(ROOT.gStyle)
