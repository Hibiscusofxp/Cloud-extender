import wx
import json

class Example(wx.Frame):

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " Extends Clouds", "About Cloud Extender", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.SaveSettings()
        self.Destroy()  # Close the frame.

    def OnOpen(self,e):
        dlg = wx.DirDialog(self, message= "Choose a folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            self.pathBox.SetValue(self.dirname)
        dlg.Destroy()
        
    def SaveSettings(self):
        f = open('data.dat', 'w')
        j = json.dumps({'path': self.pathBox.GetValue(), 'email': self.emailBox.GetValue(), 'password': self.passwordBox.GetValue(), 'apikey': self.apikeyBox.GetValue()})
        f.write(j)
        f.close()
        
    def readSettings(self):
        try:
            f = open('data.dat', 'r')
            j = json.loads(f.read())
            self.pathBox.SetValue(j["path"])
            self.emailBox.SetValue(j["email"])
            self.passwordBox.SetValue(j["password"])
            self.apikeyBox.SetValue(j["apikey"])
            
            f.close()
        except:
            return
        
    def OnSubmit(self):
        j = json.dumps({'path': self.pathBox.GetValue(), 'email': self.emailBox.GetValue(), 'password': self.passwordBox.GetValue(), 'apikey': self.apikeyBox.GetValue()})
        #send j
        #if isSuccessful:
            #runsynccode
        #else:
            #wx.MessageBox('Bad Login', 'Error', wx.OK | wx.ICON_INFORMATION)
        return
        
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(500, 400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        
        self.CreateStatusBar() # A Statusbar in the bottom of the window   
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
        
        #Creates controls
        emailLabel = wx.StaticText(self, id=-1, label="&Email:", pos=(100, 50), size=(60, 30))
        self.emailBox = wx.TextCtrl(self, id=-1, pos=(145, 45), size=(250, 25))
        passwordLabel = wx.StaticText(self, id=-1, label="&Password:", pos=(75, 80), size=(65, 30))
        self.passwordBox = wx.TextCtrl(self, id=-1, style= wx.TE_PASSWORD , pos=(145, 75), size=(250, 25))
        apikeyLabel = wx.StaticText(self, id=-1, label="&API Key:", pos=(87, 110), size=(60, 30))
        self.apikeyBox = wx.TextCtrl(self, id=-1, pos=(145, 105), size=(250, 25))
        locationLabel = wx.StaticText(self, id=-1, label="&Location:", pos=(50, 255), size=(60, 30))
        self.pathBox = wx.TextCtrl(self, id=-1, pos=(120, 250), size=(250, 30))
        browseButton = wx.Button(self, id=-1, label="&...", pos=(375, 250), size=(35, 30))
        submitButton = wx.Button(self, id=-1, label="&Login", pos=(225, 135), size=(60, 30))
        
        #Adds controls to sizer
        self.sizer2.Add(emailLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.emailBox, 1, wx.EXPAND)
        self.sizer2.Add(passwordLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.passwordBox, 1, wx.EXPAND)
        self.sizer2.Add(apikeyLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.apikeyBox, 1, wx.EXPAND)
        self.sizer2.Add(locationLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.pathBox, 1, wx.EXPAND)
        self.sizer2.Add(browseButton, 1, wx.EXPAND)
        self.sizer2.Add(submitButton, 1, wx.EXPAND)

        self.readSettings()

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show()
        
        # Events.
        self.Bind(wx.EVT_BUTTON, self.OnOpen, browseButton)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, submitButton)

if __name__ == '__main__':
  
        app = wx.App()
        Example(None, title='Cloud Extender')
        app.MainLoop()