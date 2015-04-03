import threading

import wx
import OpenGL.GL as GL
import matplotlib.backends.backend_agg
import matplotlib.figure

# key codes: 70=F, 76=L, 84=T, 66=B (as in First, Last, Top, Bottom)
KEY_MOTION_MAP = {
        70: (0, -1, 0, 0, 0),
        76: (0, 1, 0, 0, 0),
        66: (0, 0, -1, 0, 0),
        84: (0, 0, 1, 0, 0),
        wx.WXK_DOWN: (0, 0, 0, -1, 0),
        wx.WXK_UP: (0, 0, 0, 1, 0),
        wx.WXK_LEFT: (0, 0, 0, 0, -1),
        wx.WXK_RIGHT: (0, 0, 0, 0, 1),
}


def waveToRGB(wave):
    """Convert wavelength (nm) into (R,G,B) tuple.

    Fortran code http://www.physics.sfasu.edu/astro/color/spectra.html
    """
    if wave < 380:
        rgb = (0, 0, 0)
    if wave >= 380 and wave < 440:
        rgb = ((440 - wave) / 60, 0, 1)
    elif wave < 490:
        rgb = (0, (wave - 440) / 50, 1)
    elif wave < 510:
        rgb = (0, 1, (510 - wave) /20)
    elif wave < 580:
        rgb = ((wave - 510) / 70, 1, 0)
    elif wave < 645:
        rgb = (1, (wave - 645) / 65, 0)
    elif wave < 780:
        rgb = (1, 0, 0)
    else:
        rgb = (0, 0, 0)

    ## Let the intensity SSS fall off near the vision limits
    if wave > 700:
        sss = 0.3 + 0.7 * (780.0 - wave) / (780.0 - 700.0)
    elif wave < 420:
        sss = 0.3 + 0.7 * (wave - 380.0) / (420.0 - 380.0)
    else:
        sss = 1.0
    return [c * sss for c in rgb]


## Copied from the OMX version.
def addLabeledInput(parent, sizer, id = -1, label = '',
                    defaultValue = '', size = (-1, -1), minSize = (-1, -1),
                    shouldRightAlignInput = False, border = 0, labelHeightAdjustment = 0,
                    controlType = None, helperString = '', flags = wx.ALL,
                    style = 0):
    if controlType is None:
        controlType = wx.TextCtrl
    rowSizer = wx.BoxSizer(wx.HORIZONTAL)
    rowSizer.SetMinSize(minSize)
    rowSizer.Add(wx.StaticText(parent, -1, label), 0, wx.TOP, labelHeightAdjustment)
    if helperString != '':
        addHelperString(parent, rowSizer, helperString, labelHeightAdjustment, 
                wx.TOP)
    if shouldRightAlignInput:
        # Add an empty to suck up horizontal space
        rowSizer.Add((10, -1), 1, wx.EXPAND | wx.ALL, 0)
    control = controlType(parent, id, defaultValue, size = size, style = style)
    rowSizer.Add(control)
    sizer.Add(rowSizer, 0, flags, border)
    return control


## Add some explanatory text to the given sizer.
def addHelperString(parent, sizer, text, border = 0, flags = wx.ALL):
    label = wx.StaticText(parent, -1, " (What is this?)")
    label.SetForegroundColour((100, 100, 255))
    label.SetToolTipString(text)
    sizer.Add(label, 0, flags, border)


## Save an array as an image. Copied from 
# http://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image
def imsave(filename, array, vmin=None, vmax=None, cmap=None, format=None, origin=None):
    fig = matplotlib.figure.Figure(figsize=array.shape[::-1], dpi=1, frameon=False)
    canvas = matplotlib.backends.backend_agg.FigureCanvasAgg(fig)
    fig.figimage(array, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin)
    fig.savefig(filename, dpi=1, format=format)

## Save out the current OpenGL view as an image.
def saveGLView(filename):
    view = GL.glGetIntegerv(GL.GL_VIEWPORT)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
    GL.glReadBuffer(GL.GL_BACK_LEFT)
    pixels = GL.glReadPixels(0, 0, view[2], view[3], GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
    image = wx.ImageFromData(int(view[2]), int(view[3]), pixels)
    image.SaveFile(filename, wx.BITMAP_TYPE_PNG)


## Call the passed-in function in a new thread.
def callInNewThread(function):
    def wrappedFunc(*args, **kwargs):
        threading.Thread(target = function, args = args, kwargs = kwargs).start()
    return wrappedFunc


## Decorator function used to ensure that a given function is only called
# in wx's main thread.
def callInMainThread(func):
    def wrappedFunc(*args, **kwargs):
        wx.CallAfter(func, *args, **kwargs)
    return wrappedFunc


printLock = threading.Lock()
## Simple function for debugging when dealing with multiple threads, since
# otherwise Python's "print" builtin isn't threadsafe.
def threadPrint(*args):
    with printLock:
        print " ".join([str(s) for s in args])
