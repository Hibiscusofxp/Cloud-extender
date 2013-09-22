import os,sys
import wx

# class main_window(wxFrame):
# 	def __init__(self, parent, id, title):
# 		wxFrame.__init__(self, parent, -1, title,
# 			size=(200, 100),
# 			style = wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)
# 		self.control = wxTextCtrl(self, -1, style=wxTE_MULTILINE)
# 		self.Show(true)

# class App(wx.App):
# 	def OnInit(self):
# 		frame = wx.Frame(parent = None, title = "wxPython: (A Demonstration)")
# 		#self.SetTopWindow(frame)
# 		frame.Show()
# 		return True

# app = App()
# app.MainLoop()




# import wx
# class ExamplePanel(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         self.quote = wx.StaticText(self, label="Your quote :", pos=(20, 30))
#         self.quote2 = wx.StaticText(self, label="Quote 2 :", pos=(20, 30))
#         self.quote2.Hide()

#         # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
#         self.logger = wx.TextCtrl(self, pos=(300,20), size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

#         # A button
#         self.button =wx.Button(self, label="Save", pos=(200, 325))
#         self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

#         # the edit control - one line version.
#         self.lblname = wx.StaticText(self, label="Your name :", pos=(20,60))
#         self.editname = wx.TextCtrl(self, value="Enter here your name", pos=(150, 60), size=(140,-1))
#         self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
#         self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

#         # the combobox Control
#         self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']
#         self.lblhear = wx.StaticText(self, label="How did you hear from us ?", pos=(20, 90))
#         self.edithear = wx.ComboBox(self, pos=(150, 90), size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
#         self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
#         self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)

#         # Checkbox
#         self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?", pos=(20,180))
#         self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

#         # Radio Boxes
#         radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
#         rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
#                          style=wx.RA_SPECIFY_COLS)
#         self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

#     def EvtRadioBox(self, event):
#         self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
#     def EvtComboBox(self, event):
#         self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
#     def OnClick(self,event):
#         self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
#         self.quote.Hide()
#         self.quote2.Show()
#     def EvtText(self, event):
#         self.logger.AppendText('EvtText: %s\n' % event.GetString())
#     def EvtChar(self, event):
#         self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
#         event.Skip()
#     def EvtCheckBox(self, event):
#         self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())


# app = wx.App(False)
# frame = wx.Frame(None)
# panel = ExamplePanel(frame)
# frame.Show()
# app.MainLoop()


# import wx
# import wx.lib.agw.pygauge as PG

# class MyFrame(wx.Frame):

#     def __init__(self, parent):

#         wx.Frame.__init__(self, parent, -1, "PyGauge Demo")

#         panel = wx.Panel(self)

#         gauge1 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
#         gauge1.SetValue(80)
#         gauge1.SetBackgroundColour(wx.WHITE)
#         gauge1.SetBorderColor(wx.BLACK)

#         gauge2 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
#         gauge2.SetValue([20, 80])
#         gauge2.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255)])
#         gauge2.SetBackgroundColour(wx.WHITE)
#         gauge2.SetBorderColor(wx.BLACK)
#         gauge2.SetBorderPadding(2)
#         gauge2.Update([30, 0], 2000)

#         gauge3 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
#         gauge3.SetValue(50)
#         gauge3.SetBarColor(wx.GREEN)
#         gauge3.SetBackgroundColour(wx.WHITE)
#         gauge3.SetBorderColor(wx.BLACK)

#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(gauge1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
#         sizer.Add(gauge2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)
#         sizer.Add(gauge3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 20)

#         panel.SetSizer(sizer)
#         sizer.Layout()


# # our normal wxApp-derived class, as usual

# app = wx.App(0)

# frame = MyFrame(None)
# app.SetTopWindow(frame)
# frame.Show()

# app.MainLoop()





#!/usr/bin/python
# -*- coding: utf-8 -*-

# import wx

# TASK_RANGE = 50

# class Example(wx.Frame):
           
#     def __init__(self, *args, **kw):
#         super(Example, self).__init__(*args, **kw) 
        
#         self.InitUI()
        
#     def InitUI(self):   
        
#         self.timer = wx.Timer(self, 1)
#         self.count = 0

#         self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

#         pnl = wx.Panel(self)

#         vbox = wx.BoxSizer(wx.VERTICAL)
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)
#         hbox2 = wx.BoxSizer(wx.HORIZONTAL)
#         hbox3 = wx.BoxSizer(wx.HORIZONTAL)

#         self.gauge = wx.Gauge(pnl, range=TASK_RANGE, size=(250, 25))
#         self.btn1 = wx.Button(pnl, wx.ID_OK)
#         self.btn2 = wx.Button(pnl, wx.ID_STOP)
#         self.text = wx.StaticText(pnl, label='Task to be done')

#         self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)
#         self.Bind(wx.EVT_BUTTON, self.OnStop, self.btn2)

#         hbox1.Add(self.gauge, proportion=1, flag=wx.ALIGN_CENTRE)
#         hbox2.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
#         hbox2.Add(self.btn2, proportion=1)
#         hbox3.Add(self.text, proportion=1)
#         vbox.Add((0, 30))
#         vbox.Add(hbox1, flag=wx.ALIGN_CENTRE)
#         vbox.Add((0, 20))
#         vbox.Add(hbox2, proportion=1, flag=wx.ALIGN_CENTRE)
#         vbox.Add(hbox3, proportion=1, flag=wx.ALIGN_CENTRE)

#         pnl.SetSizer(vbox)
        
#         self.SetSize((300, 200))
#         self.SetTitle('wx.Gauge')
#         self.Centre()
#         self.Show(True)     

#     def OnOk(self, e):
        
#         if self.count >= TASK_RANGE:
#             return

#         self.timer.Start(100)
#         self.text.SetLabel('Task in Progress')

#     def OnStop(self, e):
        
#         if self.count == 0 or self.count >= TASK_RANGE or not self.timer.IsRunning():
#             return

#         self.timer.Stop()
#         self.text.SetLabel('Task Interrupted')
        
#     def OnTimer(self, e):
        
#         self.count = self.count + 1
#         self.gauge.SetValue(self.count)
        
#         if self.count == TASK_RANGE:

#             self.timer.Stop()
#             self.text.SetLabel('Task Completed')
                      
# def main():
    
#     ex = wx.App()
#     Example(None)
#     ex.MainLoop()    

# if __name__ == '__main__':
#     main()                 


#!/usr/bin/python
# -*- coding: utf-8 -*-

# newclass.py

# import wx

# class Example(wx.Frame):

#     def __init__(self, parent, title):    
#         super(Example, self).__init__(parent, title=title, 
#             size=(450, 350))

#         self.InitUI()
#         self.Centre()
#         self.Show()     

#     def InitUI(self):
      
#         panel = wx.Panel(self)
        


#         sizer = wx.GridBagSizer(45, 5)

#         text1 = wx.StaticText(panel, label="Java Class")
#         sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, 
#             border=15)

#         icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('ross.jpg'))
#         sizer.Add(icon, pos=(0, 4), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, 
#             border=5)

#         line = wx.StaticLine(panel)
#         sizer.Add(line, pos=(1, 0), span=(1, 5), 
#             flag=wx.EXPAND|wx.BOTTOM, border=10)

#         text2 = wx.StaticText(panel, label="Name")
#         sizer.Add(text2, pos=(2, 0), flag=wx.LEFT, border=10)

#         gauge1 = wx.Gauge(panel, range=50, size=(250, 25))
#         #tc1 = wx.TextCtrl(panel)
#         sizer.Add(gauge1, pos=(2, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND)

#         text3 = wx.StaticText(panel, label="Package")
#         sizer.Add(text3, pos=(3, 0), flag=wx.LEFT|wx.TOP, border=10)

#         tc2 = wx.TextCtrl(panel)
#         sizer.Add(tc2, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, 
#             border=5)

#         button1 = wx.Button(panel, label="Browse...")
#         sizer.Add(button1, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

#         text4 = wx.StaticText(panel, label="Extends")
#         sizer.Add(text4, pos=(4, 0), flag=wx.TOP|wx.LEFT, border=10)

#         combo = wx.ComboBox(panel)
#         sizer.Add(combo, pos=(4, 1), span=(1, 3), 
#             flag=wx.TOP|wx.EXPAND, border=5)

#         button2 = wx.Button(panel, label="Browse...")
#         sizer.Add(button2, pos=(4, 4), flag=wx.TOP|wx.RIGHT, border=5)

#         sb = wx.StaticBox(panel, label="Optional Attributes")

#         boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
#         boxsizer.Add(wx.CheckBox(panel, label="Public"), 
#             flag=wx.LEFT|wx.TOP, border=5)
#         boxsizer.Add(wx.CheckBox(panel, label="Generate Default Constructor"),
#             flag=wx.LEFT, border=5)
#         boxsizer.Add(wx.CheckBox(panel, label="Generate Main Method"), 
#             flag=wx.LEFT|wx.BOTTOM, border=5)
#         sizer.Add(boxsizer, pos=(5, 0), span=(1, 5), 
#             flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)

#         button3 = wx.Button(panel, label='Help')
#         sizer.Add(button3, pos=(7, 0), flag=wx.LEFT, border=10)

#         button4 = wx.Button(panel, label="Ok")
#         sizer.Add(button4, pos=(7, 3))

#         button5 = wx.Button(panel, label="Cancel")
#         sizer.Add(button5, pos=(7, 4), span=(1, 1),  
#             flag=wx.BOTTOM|wx.RIGHT, border=5)

#         sizer.AddGrowableCol(2)
        
#         panel.SetSizer(sizer)


# if __name__ == '__main__':
  
#     app = wx.App()
#     Example(None, title="Create Java Class")
#     app.MainLoop()


#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

In this code example, we create a
custom dialog.

author: Jan Bodnar
website: www.zetcode.com
last modified: July 2012
'''

# import wx

# class ChangeDepthDialog(wx.Dialog):
    
#     def __init__(self, *args, **kw):
#         super(ChangeDepthDialog, self).__init__(*args, **kw) 
            
#         self.InitUI()
#         self.SetSize((250, 200))
#         self.SetTitle("Change Color Depth")
        
        
#     def InitUI(self):

#         pnl = wx.Panel(self)
#         vbox = wx.BoxSizer(wx.VERTICAL)

#         sb = wx.StaticBox(pnl, label='Colors')
#         sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)        
#         sbs.Add(wx.RadioButton(pnl, label='256 Colors', 
#             style=wx.RB_GROUP))
#         sbs.Add(wx.RadioButton(pnl, label='16 Colors'))
#         sbs.Add(wx.RadioButton(pnl, label='2 Colors'))
        
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
#         hbox1.Add(wx.RadioButton(pnl, label='Custom'))
#         hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
#         sbs.Add(hbox1)
        
#         pnl.SetSizer(sbs)
       
#         hbox2 = wx.BoxSizer(wx.HORIZONTAL)
#         okButton = wx.Button(self, label='Ok')
#         closeButton = wx.Button(self, label='Close')
#         hbox2.Add(okButton)
#         hbox2.Add(closeButton, flag=wx.LEFT, border=5)

#         vbox.Add(pnl, proportion=1, 
#             flag=wx.ALL|wx.EXPAND, border=5)
#         vbox.Add(hbox2, 
#             flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

#         self.SetSizer(vbox)
        
#         okButton.Bind(wx.EVT_BUTTON, self.OnClose)
#         closeButton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        
#     def OnClose(self, e):
        
#         self.Destroy()
        
        
# class Example(wx.Frame):
    
#     def __init__(self, *args, **kw):
#         super(Example, self).__init__(*args, **kw) 
            
#         self.InitUI()
        
        
#     def InitUI(self):    
    
#         ID_DEPTH = wx.NewId()

#         tb = self.CreateToolBar()
#         tb.AddLabelTool(id=ID_DEPTH, label='', 
#             bitmap=wx.Bitmap('capture.png'))
        
#         tb.Realize()

#         self.Bind(wx.EVT_TOOL, self.OnChangeDepth, 
#             id=ID_DEPTH)

#         self.SetSize((300, 200))
#         self.SetTitle('Custom dialog')
#         self.Centre()
#         self.Show(True)
        
        
#     def OnChangeDepth(self, e):
        
#         chgdep = ChangeDepthDialog(None, 
#             title='Change Color Depth')
#         chgdep.ShowModal()
#         chgdep.Destroy()        


# def main():
    
#     ex = wx.App()
#     Example(None)
#     ex.MainLoop()    


# if __name__ == '__main__':
#     main()


#!/usr/bin/python

# commondialogs.py

#!/usr/bin/python

# staticbox.py

#!/usr/bin/python

# radiobuttons.py














# import wx

# class MyFrame(wx.Frame):
#     def __init__(self, parent, id, title):
#         wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(300, 220))
#         panel = wx.Panel(self, -1)
#         self.st = wx.StaticText(panel, -1, 'Sync frequencey', (10, 10))
#         self.rb1 = wx.RadioButton(panel, -1, 'Every hour', (10, 35), style=wx.RB_GROUP)
#         self.rb2 = wx.RadioButton(panel, -1, 'Every day', (100, 35))
#         self.rb3 = wx.RadioButton(panel, -1, 'Every week', (190, 35))
#         self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb1.GetId())
#         self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb2.GetId())
#         self.Bind(wx.EVT_RADIOBUTTON, self.SetVal, id=self.rb3.GetId())
#         self.statusbar = self.CreateStatusBar(3)
#         self.SetVal(True)

#         self.cb = wx.CheckBox(panel, -1, 'Check to sync every time a new file is uploaded', (10, 55))
#         self.cb.SetValue(True)
#         wx.EVT_CHECKBOX(self, self.cb.GetId(), self.ShowTitle)

#         # self.tc = wx.TextCtrl(panel, -1, 'Total storage', (10, 100))
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)        
#         hbox1.Add(wx.StaticText(panel, label='Maximum storage capacity', pos=(10,85)))
#         hbox1.Add(wx.TextCtrl(panel, -1, 'a', pos=(160,80), size=(50,25)), flag=wx.LEFT, border=5)
#         hbox1.Add(wx.StaticText(panel, label='GB', pos= (220,85)))

#         self.bt = wx.Button(panel, 1, 'OK', (95, 120))
#         self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=1)

#     def SetVal(self, event):
#         state1 = str(self.rb1.GetValue())
#         state2 = str(self.rb2.GetValue())
#         state3 = str(self.rb3.GetValue())
#         self.statusbar.SetStatusText(state1,0)
#         self.statusbar.SetStatusText(state2,1)
#         self.statusbar.SetStatusText(state3,2)

#     def ShowTitle(self, event):
#         if self.cb.GetValue():
#             self.SetTitle('Checked'+self.tc.GetValue())
#         else: self.SetTitle('')

#     def OnSubmit(self, event):
#     	self.Close(True)

# class MyApp(wx.App):
#     def OnInit(self):
#         frame = MyFrame(None, -1, 'radiobuttons.py')
#         frame.Show(True)
#         frame.Center()
#         return True

# app = MyApp(0)
# app.MainLoop()



#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

This example shows a simple menu.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
'''

import wx

class MainFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs) 
            
        self.InitUI()
        
    def InitUI(self):    

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fites = fileMenu.Append(wx.ID_ANY, 'Setting', 'Set preferences')
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&Option')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_MENU, self.OnSet, fites)

        self.SetSize((300, 200))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, e):
        self.Close()

    def OnSet(self, e):
        #self.Close()
        settingDia = SettingFrame(None, title = 'Setting')
        settingDia.ShowModal()
        settingDia.Destroy()

class SettingFrame(wx.Dialog):

    def __init__(self, *args, **kw):
        super(SettingFrame, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle("Setting")

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


def main():
    
    ex = wx.App()
    MainFrame(None)
    ex.MainLoop()    


if __name__ == '__main__':
    main()