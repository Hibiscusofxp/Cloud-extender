import json, urllib, wx.html2, monitor, wx.lib.agw.pygauge as PG

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

    def OnInfo(self,e):
        InfoDialog = InfoDia(None, 'Info', 20.55, 50, 20, 100)
        InfoDialog.ShowModal()
        InfoDialog.Destroy()

    def OnSet(self,e):
        settingDia = SettingFrame(None, 'Info')
        settingDia.ShowModal()
        settingDia.Destroy()

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
                self.emailLabel.Hide()
                self.emailBox.Hide()
                self.passwordLabel.Hide()
                self.passwordBox.Hide()
                self.apikeyLabel.Hide()
                self.apikeyBox.Hide()
                self.locationLabel.Hide()
                self.pathBox.Hide()
                self.emailBox.Hide()
                self.browseButton.Hide()
                self.browseButton.Hide()
                self.submitButton.Hide()
                
                self.syncstatusLabel.Show()          
                self.gauge.Show()      
                self.gauge.SetValue(0)
                
                self.monitor = monitor.Monitor(self.sessionkey, self.pathBox.GetValue())
                self.monitor.start()
                self.gauge.SetValue(100)
                #dialog.browser.LoadURL("http://www.ADDPREDICTIONAPIOAUTH.com")
                dialog.Show()
                
                print "awesome"
                self.isLogged = 1
            else:
                wx.MessageBox('Bad Login', 'Error', wx.OK | wx.ICON_INFORMATION)
                self.isLogged = 0
            return
        except Exception as ex:
            wx.MessageBox('Bad Login', 'Error', wx.OK | wx.ICON_INFORMATION)
            print ex
            self.isLogged = 0
            return
        
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(500, 400), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.isLogged = 0
        self.CreateStatusBar() # A Statusbar in the bottom of the window   
        self.Centre()
        
        # Setting up the menu.
        filemenu= wx.Menu()
        menuInfo = filemenu.Append(wx.ID_ANY,"I&nfo"," Get the status")
        menuSet = filemenu.Append(wx.ID_ANY,"S&etting"," Set prereferences")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        #self.loginpnl = wx.Panel(self, -1)
        # self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        #Creates controls
        #oliver
        self.emailLabel = wx.StaticText(self, id=-1, label="&Email:", pos=(100, 80), size=(60, 30))
        self.emailBox = wx.TextCtrl(self, id=-1, pos=(145, 75), size=(250, 25))
        self.passwordLabel = wx.StaticText(self, id=-1, label="&Password:", pos=(75, 110), size=(65, 30))
        self.passwordBox = wx.TextCtrl(self, id=-1, style= wx.TE_PASSWORD , pos=(145, 105), size=(250, 25))
        self.apikeyLabel = wx.StaticText(self, id=-1, label="&API Key:", pos=(87, 140), size=(60, 30))
        self.apikeyBox = wx.TextCtrl(self, id=-1, pos=(145, 135), size=(250, 25))
        self.locationLabel = wx.StaticText(self, id=-1, label="&Location:", pos=(50, 285), size=(60, 20))
        self.pathBox = wx.TextCtrl(self, id=-1, pos=(120, 280), size=(250, 30))
        self.browseButton = wx.Button(self, id=-1, label="&...", pos=(375, 280), size=(35, 30))
        self.submitButton = wx.Button(self, id=-1, label="&Login", pos=(225, 165), size=(60, 30))
        self.gauge = wx.Gauge(self, id=-1, pos=(150,150), size=(300, 30))
        self.syncstatusLabel = wx.StaticText(self, id=-1, label="&Sync Status:", pos=(50, 285), size=(60, 30))
        self.gauge.Hide()
        self.syncstatusLabel.Hide()
        
        png = wx.Image('Cloud.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.image = wx.StaticBitmap(self, -1, png, (0,0), (png.GetWidth(), png.GetHeight()))

        #Changes background to white
        self.SetBackgroundColour('#ffffff') #oliver
        
        # #Adds controls to sizer
        # self.sizer2.Add(emailLabel, 1, wx.EXPAND)
        # self.sizer2.Add(self.emailBox, 1, wx.EXPAND)
        # self.sizer2.Add(passwordLabel, 1, wx.EXPAND)
        # self.sizer2.Add(self.passwordBox, 1, wx.EXPAND)
        # self.sizer2.Add(apikeyLabel, 1, wx.EXPAND)
        # self.sizer2.Add(self.apikeyBox, 1, wx.EXPAND)
        # self.sizer2.Add(locationLabel, 1, wx.EXPAND)
        # self.sizer2.Add(self.pathBox, 1, wx.EXPAND)
        # self.sizer2.Add(browseButton, 1, wx.EXPAND)
        # self.sizer2.Add(submitButton, 1, wx.EXPAND)
        # self.sizer2.Add(sizeusedLabel , 1, wx.EXPAND)
        # self.sizer2.Add(sizedleftLabel, 1, wx.EXPAND)
        
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
        self.Bind(wx.EVT_MENU, self.OnInfo, menuInfo)
        self.Bind(wx.EVT_MENU, self.OnSet, menuSet)
            #if self.isLogged ==0:
                #break

class InfoDia(wx.Dialog):
    box = 0
    drive = 0
    dropbox = 0
    total = 0
    def __init__(self, parent, title, dropbox, drive, box, total):
        super(InfoDia, self).__init__(parent, title=title, 
            size=(390, 350))
        self.box = box
        self.drive = drive
        self.dropbox = dropbox
        self.total = total
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self)
        # panel.Hide()
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        font2 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font2.SetPointSize(15)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Total Storage: ')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)


        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        # tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        self.bigBar = PG.PyGauge(panel, -1, size=(200, 25), style=wx.GA_HORIZONTAL)
        self.bigBar.SetValue([100*self.box/self.total, 100*(self.drive+self.box)/self.total, 100*(self.dropbox+self.box+self.drive)/self.total])
        self.bigBar.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255), wx.Colour(59, 76, 255)])
        self.bigBar.SetBackgroundColour(wx.WHITE)
        self.bigBar.SetBorderColor(wx.BLACK)

        hbox3.Add(self.bigBar, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)

        vbox.Add((-1, 20))
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        square1 = PG.PyGauge(panel, -1, size=(25, 25), style=wx.GA_HORIZONTAL)
        square1.SetValue(100)
        square1.SetBarColor(wx.Colour(162, 255, 178))
        square1.SetBackgroundColour(wx.WHITE)
        square1.SetBorderColor(wx.WHITE)
        st4 = wx.StaticText(panel, label=' BOX')
        st4.SetFont(font2)
        square2 = PG.PyGauge(panel, -1, size=(25, 25), style=wx.GA_HORIZONTAL)
        square2.SetValue(100)
        square2.SetBarColor(wx.Colour(159, 176, 255))
        square2.SetBackgroundColour(wx.WHITE)
        square2.SetBorderColor(wx.WHITE)
        st5 = wx.StaticText(panel, label=' Google Drive')
        st5.SetFont(font2)
        square3 = PG.PyGauge(panel, -1, size=(25, 25), style=wx.GA_HORIZONTAL)
        square3.SetValue(100)
        square3.SetBarColor(wx.Colour(59, 76, 255))
        square3.SetBackgroundColour(wx.WHITE)
        square3.SetBorderColor(wx.WHITE)
        st6 = wx.StaticText(panel, label=' Dropbox')
        st6.SetFont(font2)
        hbox4.Add(square1)
        hbox4.Add(st4)
        hbox4.Add(square2, flag=wx.LEFT, border=30)
        hbox4.Add(st5)
        hbox4.Add(square3, flag=wx.LEFT, border=30)
        hbox4.Add(st6)        

        vbox.Add(hbox4, flag=wx.LEFT, border=10)
        
        vbox.Add((-1, 30))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='Remaining Storage: ')
        st2.SetFont(font)
        st3 = wx.StaticText(panel, label=str(self.dropbox+self.box+self.drive) + 'GB / ' + str(self.total) + 'GB')
        st3.SetFont(font)
        hbox2.Add(st2)
        hbox2.Add(st3)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)


        vbox.Add((-1, 145))

        panel.SetSizer(vbox)


class SettingFrame(wx.Dialog):

    def __init__(self, parent, title = 'Setting'):
        super(SettingFrame, self).__init__(parent= parent, title = title, size=(300, 200)) 
            
        self.InitUI()
        #self.SetSize((300, 200))
        #self.SetTitle("Setting")

    def InitUI(self):

        panel = wx.Panel(self, -1)
        self.st = wx.StaticText(panel, -1, 'Sync frequencey', (10, 10))
        self.rb1 = wx.RadioButton(panel, -1, 'Every hour', (10, 35), style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(panel, -1, 'Every day', (100, 35))
        self.rb3 = wx.RadioButton(panel, -1, 'Every week', (190, 35))
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb1.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb2.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb3.GetId())
        # self.statusbar = self.CreateStatusBar(3)
        self.SetVal(True)

        self.cb = wx.CheckBox(panel, -1, 'Check to sync every time a new file is uploaded', (10, 55))
        self.cb.SetValue(True)
        wx.EVT_CHECKBOX(self, self.cb.GetId(), self.ShowTitle)

        # self.tc = wx.TextCtrl(panel, -1, 'Total storage', (10, 100))
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
        hbox1.Add(wx.StaticText(panel, label='Maximum storage capacity', pos=(10,85)))
        self.tc = wx.TextCtrl(panel, -1, 'a', pos=(160,80), size=(50,25))
        hbox1.Add(self.tc, flag=wx.LEFT, border=5)
        hbox1.Add(wx.StaticText(panel, label='GB', pos= (220,85)))

        self.bt = wx.Button(panel, 1, 'OK', (95, 120))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=1)

    def SetVal(self, event):
        state1 = str(self.rb1.GetValue())
        state2 = str(self.rb2.GetValue())
        state3 = str(self.rb3.GetValue())
        #self.statusbar.SetStatusText(state1,0)
        #self.statusbar.SetStatusText(state2,1)
        #self.statusbar.SetStatusText(state3,2)

    def ShowTitle(self, event):
        if self.cb.GetValue():
            self.SetTitle('Checked'+self.tc.GetValue())
        else: self.SetTitle('')

    def OnSubmit(self, event):
        self.Destroy()



if __name__ == '__main__':
        # sys.path.append(os.path.dirname(__file__))
        
        app = wx.App()
        dialog = MyBrowser(None, -1) 
        Example(None, title='Cloud Extender')
        app.MainLoop()