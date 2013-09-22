#!/usr/bin/python
# -*- coding: utf-8 -*-

# gotoclass.py

import wx
import wx.lib.agw.pygauge as PG

class Example(wx.Frame):
    box = 0
    drive = 0
    dropbox = 0
    total = 0
    def __init__(self, parent, title, dropbox, drive, box, total):
        super(Example, self).__init__(parent, title=title, 
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

        bigBar = PG.PyGauge(panel, -1, size=(200, 25), style=wx.GA_HORIZONTAL)
        bigBar.SetValue([100*self.box/self.total, 100*(self.drive+self.box)/self.total, 100*(self.dropbox+self.box+self.drive)/self.total])
        bigBar.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255), wx.Colour(59, 76, 255)])
        bigBar.SetBackgroundColour(wx.WHITE)
        bigBar.SetBorderColor(wx.BLACK)

        hbox3.Add(bigBar, proportion=1, flag=wx.EXPAND)
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


if __name__ == '__main__':
  
    app = wx.App()
    Example(None, 'Information', 20.55, 50, 20, 100)
    app.MainLoop()