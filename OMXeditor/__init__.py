import sys
import os

import wx

import mainWindow

__version__ = "2.6-dev"


## The requisite WX App instance; this just creates the main window and 
# passes it any files that were specified in the commandline.
class OMXeditorApp(wx.App):
    def OnInit(self):
        self.frame = mainWindow.MainWindow(title = 'OMX Editor v' + __version__)
        wx.CallAfter(self.onRun)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    ## We want to run this only after we are in the MainLoop.  Otherwise,
    # if the first image causes any issue, we will crash rather than having
    # it caught by the MainLoop to be processed.
    def onRun(self):
        haveFilesToOpen = False
        for file in sys.argv[1:]:
            # When invoking this program as a standalone bundled app with 
            # py2app, a bunch of junk we don't care about shows up on the 
            # commandline, so only try to open a file if it actually exists.
            if os.path.exists(file):
                self.frame.openFile(file)
                haveFilesToOpen = True

        if not haveFilesToOpen:
            # Instead of just popping up a blank window, show an open-file
            # dialog.
            self.frame.OnFileOpen()

    def setStatusbarText(self, text, number=0):
        self.frame.SetStatusText(text, number)

def main():
    app = OMXeditorApp(redirect=False)
    app.MainLoop()
