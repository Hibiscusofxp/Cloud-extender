import wx, json
import sync, sys, os, urllib
import wx.html2 
import monitor
import wx.lib.agw.pygauge as PG

class MyBrowser(wx.Dialog): 
  def __init__(self, *args, **kwds): 
    wx.Dialog.__init__(self, *args, **kwds) 
    sizer = wx.BoxSizer(wx.VERTICAL) 
    self.browser = wx.html2.WebView.New(self) 
    sizer.Add(self.browser, 1, wx.EXPAND, 10) 
    self.SetSizer(sizer) 
    self.SetSize((700, 700))

class Example(wx.Frame):

    def Auth(self, email, password, apikey):
        fullurl = "https://api.point.io/v2/auth.json"
        paras = {
            'email':email,
            'password':password,
            'apikey':apikey
        }
        paras = urllib.urlencode(paras)
        result = urllib.urlopen(fullurl, paras)
        arr = result.readlines()
        arr = json.loads(arr[0])
        self.sessionkey = arr['RESULT']['SESSIONKEY']
        return arr

    #Function runs on the event of when about menu button is clicked
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " Extends Clouds", "About Cloud Extender", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    ##Function runs when GUI is closed
    def OnExit(self,e):
        self.SaveSettings()
        self.Destroy()  # Close the frame.

    #Function runs on the event of when the browse button is clicked
    def OnOpen(self,e):
        dlg = wx.DirDialog(self, message= "Choose a folder")
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            self.pathBox.SetValue(self.dirname)
        dlg.Destroy()
        
    #Function caches data for another session in data.dat
    def SaveSettings(self):
        f = open('data.dat', 'w')
        j = json.dumps({'path': self.pathBox.GetValue(), 'email': self.emailBox.GetValue(), 'password': self.passwordBox.GetValue(), 'apikey': self.apikeyBox.GetValue()})
        f.write(j)
        f.close()
        
    #Function reads in cached data if it exists
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
        
    #Runs when submit button is clicked
    def OnSubmit(self, e):
        #send j for Authorization
        try:
            Authresp = self.Auth(self.emailBox.GetValue(), self.passwordBox.GetValue(), self.apikeyBox.GetValue())
            if Authresp['ERROR'] == 0:
                self.sizer2.Hide(self.emailLabel)
                self.sizer2.Hide(self.emailBox)
                self.sizer2.Hide(self.passwordLabel)
                self.sizer2.Hide(self.passwordBox)
                self.sizer2.Hide(self.apikeyLabel)
                self.sizer2.Hide(self.apikeyBox)
                self.sizer2.Hide(self.locationLabel)
                self.sizer2.Hide(self.pathBox)
                self.sizer2.Hide(self.emailBox)
                self.sizer2.Hide(self.browseButton)
                self.sizer2.Hide(self.browseButton)
                self.sizer2.Hide(self.submitButton)
                
                self.gauge.Show()
                self.syncstatusLabel.Show()
                self.bigBar.Show()
                self.gauge.Show()
                self.square1.Show()
                self.st4.Show()
                self.square2.Show()
                self.st5.Show()
                self.square3.Show()
                self.st6.Show()
                self.st2.Show()
                
                self.gauge.SetValue(0)
                
                self.monitor = monitor.Monitor(self.sessionkey, self.pathBox.GetValue())
                self.monitor.start()
                self.gauge.SetValue(100)
                dialog.browser.LoadURL("http://www.ADDPREDICTIONAPIOAUTH.com")
                dialog.Show()
                print "awesome"
                self.isLogged = 1
            else:
                wx.MessageBox('Bad Login', 'Error', wx.OK | wx.ICON_INFORMATION)
                self.isLogged = 0
            return
        except:
            wx.MessageBox('Bad Login', 'Error', wx.OK | wx.ICON_INFORMATION)
            self.isLogged = 0
            return
        
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(500, 400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.isLogged = 0
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
        self.emailLabel = wx.StaticText(self, id=-1, label="&Email:", pos=(100, 50), size=(60, 30))
        self.emailBox = wx.TextCtrl(self, id=-1, pos=(145, 45), size=(250, 25))
        self.passwordLabel = wx.StaticText(self, id=-1, label="&Password:", pos=(75, 80), size=(65, 30))
        self.passwordBox = wx.TextCtrl(self, id=-1, style= wx.TE_PASSWORD , pos=(145, 75), size=(250, 25))
        self.apikeyLabel = wx.StaticText(self, id=-1, label="&API Key:", pos=(87, 110), size=(60, 30))
        self.apikeyBox = wx.TextCtrl(self, id=-1, pos=(145, 105), size=(250, 25))
        self.locationLabel = wx.StaticText(self, id=-1, label="&Location:", pos=(50, 255), size=(60, 30))
        self.pathBox = wx.TextCtrl(self, id=-1, pos=(120, 250), size=(250, 30))
        self.browseButton = wx.Button(self, id=-1, label="&...", pos=(375, 250), size=(35, 30))
        self.submitButton = wx.Button(self, id=-1, label="&Login", pos=(225, 135), size=(60, 30))
        self.gauge = wx.Gauge(self, id=-1, pos=(150,150), size=(300, 30))
        self.syncstatusLabel = wx.StaticText(self, id=-1, label="&Sync Status:", pos=(70, 155), size=(85, 20))
        
        self.bigBar = PG.PyGauge(self, -1,pos=(0,25), size=(400, 30), style=wx.GA_HORIZONTAL)
        #self.bigBar.SetValue([100*self.box/self.total, 100*(self.drive+self.box)/self.total, 100*(self.dropbox+self.box+self.drive)/self.total])
        self.bigBar.SetValue(50)
        self.bigBar.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255), wx.Colour(59, 76, 255)])
        self.bigBar.SetBackgroundColour(wx.WHITE)
        self.bigBar.SetBorderColor(wx.BLACK)
        
        #vbox = wx.BoxSizer(wx.VERTICAL)
        #vbox.Add((-1, 20))
        #hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.square1 = PG.PyGauge(self, -1, pos=(50,55), size=(25, 25), style=wx.GA_HORIZONTAL)
        self.square1.SetValue(100)
        self.square1.SetBarColor(wx.Colour(162, 255, 178))
        self.square1.SetBackgroundColour(wx.WHITE)
        self.square1.SetBorderColor(wx.WHITE)
        self.st4 = wx.StaticText(self, pos=(0,55), label=' BOX')
        
        self.square2 = PG.PyGauge(self, -1, pos=(175,55), size=(25, 25), style=wx.GA_HORIZONTAL)
        self.square2.SetValue(100)
        self.square2.SetBarColor(wx.Colour(159, 176, 255))
        self.square2.SetBackgroundColour(wx.WHITE)
        self.square2.SetBorderColor(wx.WHITE)
        self.st5 = wx.StaticText(self, pos=(80,55), label=' Google Drive')
        
        self.square3 = PG.PyGauge(self, -1, pos=(280,55), size=(25, 25), style=wx.GA_HORIZONTAL)
        self.square3.SetValue(100)
        self.square3.SetBarColor(wx.Colour(59, 76, 255))
        self.square3.SetBackgroundColour(wx.WHITE)
        self.square3.SetBorderColor(wx.WHITE)
        self.st6 = wx.StaticText(self, pos=(200,55), label=' Dropbox')

        self.st2 = wx.StaticText(self, pos=(0,95), label='Remaining Storage: ')

        self.gauge.Hide()
        self.syncstatusLabel.Hide()
        self.bigBar.Hide()
        self.square1.Hide()
        self.st4.Hide()
        self.square2.Hide()
        self.st5.Hide()
        self.square3.Hide()
        self.st6.Hide()
        self.st2.Hide()
        
        #Changes background to white
        self.SetBackgroundColour('f0f0f0')
        
        #Adds controls to sizer
        self.sizer2.Add(self.emailLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.emailBox, 1, wx.EXPAND)
        self.sizer2.Add(self.passwordLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.passwordBox, 1, wx.EXPAND)
        self.sizer2.Add(self.apikeyLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.apikeyBox, 1, wx.EXPAND)
        self.sizer2.Add(self.locationLabel, 1, wx.EXPAND)
        self.sizer2.Add(self.pathBox, 1, wx.EXPAND)
        self.sizer2.Add(self.browseButton, 1, wx.EXPAND)
        self.sizer2.Add(self.submitButton, 1, wx.EXPAND)
        
        #Get previous data if any
        self.readSettings()
        
        #Set usage details
        #sizeusedLabel.SetLabel(str( "%.2f" % (sync.loadDirDict(dir, dct)(cloud.authorization,cloud.shareId)/1000000) )+"GB/")
        #sizedleftLabel.SetLabel("GB")
        
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.Show()
        
        # Events.
        #while True:
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.browseButton)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.submitButton)
            #if self.isLogged ==0:
                #break

if __name__ == '__main__':
        sys.path.append(os.path.dirname(__file__))
        
        app = wx.App()
        dialog = MyBrowser(None, -1) 
        Example(None, title='Cloud Extender')
        app.MainLoop()