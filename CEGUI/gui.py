import wx
import os

class Example(wx.Frame):

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " Extends Clouds", "About Cloud Extender", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a folder", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetDirectory()
            #pathBox.SetValue(self.dirname)
        dlg.Destroy()
  
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(500, 400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.dirname=''    
        self.Centre()
        
        # Setting up the menu.
        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        workingdirectoryLabel = wx.StaticText(self, id=-1, label="&Location:", pos=(50, 255), size=(60, 30))
        pathBox = wx.TextCtrl(self, id=-1, value="path", pos=(120, 250), size=(250, 30))
        browseButton = wx.Button(self, id=-1, label="&...", pos=(375, 250), size=(35, 30))
        self.sizer2.Add(workingdirectoryLabel, 1, wx.EXPAND)
        self.sizer2.Add(pathBox, 1, wx.EXPAND)
        self.sizer2.Add(browseButton, 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show()
        
        # Events.
        self.Bind(wx.EVT_BUTTON, self.OnOpen, browseButton)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

if __name__ == '__main__':
  
        app = wx.App()
        Example(None, title='Cloud Extender')
        app.MainLoop()