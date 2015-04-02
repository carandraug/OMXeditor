import numpy
import OpenGL.GL as GL
import wx
import wx.glcanvas

## An OpenGL canvas for drawing histograms, including mouse manipulation of the
# black and whitepoints.
class HistogramCanvas(wx.glcanvas.GLCanvas):

    ## Drag modes -- left vs. right braces.
    DRAG_BLACKPOINT = 1
    DRAG_WHITEPOINT = 2

    ## \param scaleCallback Function to call when black/whitepoints are changed.
    # \param infoCallback Function to call to inform about current position and
    #        scale.
    # \param image Image array we provide a histogram for.
    # \param numBins How many bins to use when generating the histogram.
    def __init__(self, parent, scaleCallback, infoCallback, image, color, size):
        wx.glcanvas.GLCanvas.__init__(self, parent, size = size)
        self.scaleCallback = scaleCallback
        self.infoCallback = infoCallback
        ## Color tuple for drawing
        self.color = color
        ## Number of bins to use
        self.numBins = size[0]
        ## Width and height of the canvas
        self.width = self.height = None
        ## Black- and whitepoints, for scaling the image
        self.blackPoint, self.whitePoint = 0.0, 1.0
        ## Min and max values of our current image.
        self.minVal, self.maxVal = None, None
        ## Mouse position as of last call to onMouse.
        self.mouseX = self.mouseY = None
        ## What, if any, mouse dragging we're doing.
        self.dragMode = None
        ## Whether or not we've initialized OpenGL
        self.haveInitedOpenGL = False
        ## OpenGL context
        self.context = wx.glcanvas.GLContext(self)

        self.updateImage(image)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouse)
    

    ## Recalculate our bins and min/max values, based on the provided image.
    def updateImage(self, image):
        self.binSizes, self.binEdges = numpy.histogram(image, self.numBins)
        self.minVal = image.min()
        self.maxVal = image.max()


    ## Reset black/whitepoint.
    def autoFit(self):
        self.blackPoint, self.whitePoint = 0.0, 1.0


    ## Adjust our black/whitepoints to the given image, which is a subset
    # of our overall data.
    def autoFitToImage(self, image):
        self.minVal = image.min()
        self.maxVal = image.max()
        self.Refresh()


    ## Get the blackpoint and whitepoint as applied to the current image.
    # That is, the largest pixel value that paints as black, and the smallest
    # that paints as white.
    def getMinMax(self):
        scale = self.maxVal - self.minVal
        minVal = int(self.blackPoint * scale + self.minVal)
        maxVal = int(self.whitePoint * scale + self.minVal)
        return (minVal, maxVal)


    ## Paint the histogram.
    def onPaint(self, event = None):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        
        if not self.haveInitedOpenGL:
            self.width, self.height = self.GetClientSizeTuple()
            GL.glClearColor(0, 0, 0, 0)
            self.haveInitedOpenGL = True

        GL.glViewport(0, 0, self.width, self.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, self.width, 0, self.height, 1, -1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Draw a gradient background
        GL.glBegin(GL.GL_QUADS)
        GL.glColor3fv(self.color)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.width, 0)
        GL.glColor3f(1, 1, 1)
        GL.glVertex2f(self.width, self.height)
        GL.glVertex2f(0, self.height)
        GL.glEnd()

        # Draw a quad for each bin
        GL.glBegin(GL.GL_QUADS)
        GL.glColor3f(0, 0, 0)
        binWidth = self.width / float(self.numBins)
        maxVal = max(self.binSizes)

        xOff = binWidth * numpy.array (range(self.binSizes.size +1))
        heights = self.binSizes / float(maxVal) * self.height
        for i in self.binSizes.nonzero()[0]:
            GL.glVertex2f(xOff[i], 0)
            GL.glVertex2f(xOff[i+1], 0)
            GL.glVertex2f(xOff[i+1], heights[i])
            GL.glVertex2f(xOff[i], heights[i])
        GL.glEnd()

        # Draw marks for the black and white points
        GL.glColor3f(0, 0, 0)

        # The horizontal position of the marks are based on our
        # black and white points, and are positioned independent
        # of the current image data.
        for val, sign in [(self.blackPoint, 1), (self.whitePoint, -1)]:
            # Offset by 1 pixel to ensure we stay in-bounds even with min/max values
            xOff = val * self.width + sign
            GL.glBegin(GL.GL_LINE_STRIP)
            GL.glVertex2f(xOff + sign * 5, 2)
            GL.glVertex2f(xOff, 2)
            GL.glVertex2f(xOff, self.height - 2)
            GL.glVertex2f(xOff + sign * 5, self.height - 2)
            GL.glEnd()

        self.SwapBuffers()


    ## Handle mouse events. Left-click drag to adjust black/whitepoint, 
    # right-click to reset both.
    def onMouse(self, event):
        curX, curY = event.GetPosition()
        shouldUpdate = False

        if event.LeftDown():
            # Started dragging. Set drag mode based on current mouse position.
            self.dragMode = None
            if curX < self.width / 2:
                self.dragMode = self.DRAG_BLACKPOINT
            else:
                self.dragMode = self.DRAG_WHITEPOINT
        elif event.LeftIsDown():
            # Continue dragging.
            delta = float(curX - self.mouseX) / self.width
            if self.dragMode == self.DRAG_BLACKPOINT:
                self.blackPoint += delta
            elif self.dragMode == self.DRAG_WHITEPOINT:
                self.whitePoint += delta
            shouldUpdate = True
        elif event.RightDown():
            # Reset black and whitepoints.
            self.autoFit()
            shouldUpdate = True

        scale = self.maxVal - self.minVal
        minVal = self.blackPoint * scale + self.minVal
        maxVal = self.whitePoint * scale + self.minVal
        curVal = curX * scale / float(self.width) + self.minVal
        self.infoCallback(curVal, minVal, maxVal)
        if shouldUpdate:
            self.scaleCallback(minVal, maxVal)
            self.Refresh(False)

        self.mouseX, self.mouseY = curX, curY


## This class handles a histogram of image data, including drawing and
# manipulation of that histogram.
class HistogramPanel(wx.Panel):
    ## \param scaleCallback Function to call when the histogram scaling is 
    #         changed.
    # \param helpCallback Function to call to set help text.
    def __init__(self, parent, scaleCallback, helpCallback, wavelength, image, 
            color, size):
        wx.Panel.__init__(self, parent, size = size, style = wx.BORDER_SUNKEN)
        ## Wavelength we are controlling.
        self.wavelength = wavelength
        # HACK: insert the wavelength into the callback, since it's not there by 
        # default.
        modScaleCallback = lambda minVal, maxVal: scaleCallback(wavelength, minVal, maxVal)
        sizer = wx.BoxSizer(wx.VERTICAL)
        ## Canvas for drawing the histogram
        self.canvas = HistogramCanvas(self, modScaleCallback, self.onInfo, 
                image, color, size)
        self.canvas.SetMinSize(size)
        sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(sizer)

        ## Callback for when the mouse is over the histogram.
        self.helpCallback = helpCallback


    ## Display information about the histogram in the bottom bar of the window.
    def onInfo(self, curVal, minVal, maxVal):
        wx.GetApp().setStatusbarText("I: %6.2f  left/right: %6.2f %6.2f"  %(curVal, minVal, maxVal), self.wavelength)

        self.helpCallback('Histogram',
                "Click and drag to change the white and black points for this wavelength. Right-click to reset to default scale values.")


    def autoFit(self):
        self.canvas.autoFit()


    def autoFitToImage(self, image):
        self.canvas.autoFitToImage(image)


    ## Retrieve the min/max points (below min is 0, above max is 1).
    def getMinMax(self):
        return self.canvas.getMinMax()


