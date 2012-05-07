#!/usr/bin/python

import wx
import os
import random

APP_EXIT = 1
LOAD_FILE = 2
FIND_SET = 3
GET_BOARD = 4




class AI:
    """docstring for AI"""
    def __init__(self, _boardsize=12, _setsize=3, _props=4):
        self.Deck = []
        self.Board = []

        self.boardsize = _boardsize
        self.setsize = _setsize
        self.props = _props
        
        

    def LoadFile(self, filePath):
        """docstring for LoadFile"""
        fLoad = open(filePath, 'r')
        
        for line in fLoad:
            self.Deck.append(line.split())
        fLoad.close()

        random.shuffle(self.Deck)

        for i in range(self.boardsize):
            self.Board.append(self.Deck.pop())

 
    def dfs(Board, workingSet, checkSet, index):
        """docstring for dfs"""
        
        if not(index in checkSet):
            workingSet.append(index)
            checkSet.add(index)
        if len(workingSet) < self.setsize:
            print "Adding another card to the set"
            print workingSet
            for i in range(self.boardsize):
                if not(i in checkSet):
                    Result = dfs(Board, workingSet, checkSet, i)
                    if Result[0]:
                        return True, Result[1]
                    else:
                        checkSet.remove(i)
                        workingSet.pop()
                        continue 
            return False,
                       

        if check(workingSet, Board): 
            return (True, workingSet)
     
    def Find(self):
        """docstring for Find"""

        for index in range(self.boardsize):
        
            workingSet = []
            checkSet = set(workingSet)
            index = 0
            Result = dfs(Board, workingSet, checkSet, index)
            if (len(Result) == 2):
                foundSet = True
                print_set(Result[1])
                break
            else:
                workingSet[:] = []


        if not(foundSet):
            return False,
         
        
        

class SetDemo(wx.Frame):
    """docstring for """
    def __init__(self, arg):
        super(SetDemo, self).__init__(arg)
        self.arg = arg
        self.Solver = AI()
        self.tiles = wx.GridSizer(self.Solver.setsize,self.Solver.props)
        self.MainPanel = wx.Panel(self, style=wx.SUNKEN_BORDER)

        self.tiles.SetContainingWindow(self.MainPanel)
        self.MainPanel.SetSizer(self.tiles)



        self.InitUI()
    
    def InitUI(self):
        """docstring for InitUI"""

        ID_DEPTH = wx.NewId()
        
        menubar = wx.MenuBar()
        menu = wx.Menu()
        mquit = wx.MenuItem(menu, APP_EXIT, '&Quit\tCtrl+Q')
        mload = wx.MenuItem(menu, LOAD_FILE, '&Load File\tCtrl+L')
        mfind = wx.MenuItem(menu, FIND_SET, '&Find Set\tCtrl+F')
        mrefresh = wx.MenuItem(menu, GET_BOARD, '&Get Board\tCtrl+B') 

        menu.AppendItem(mload)
        menu.AppendItem(mfind)
        menu.AppendItem(mrefresh)
        menu.AppendItem(mquit)

        menubar.Append(menu, '&File')

        self.SetMenuBar(menubar)
        

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.OnLoad, id=LOAD_FILE)
        self.Bind(wx.EVT_MENU, self.OnFind, id=FIND_SET)
        self.Bind(wx.EVT_MENU, self.OnGet, id=GET_BOARD)
        
        
        
        self.Show(True)

    def OnQuit(self, e):
        """docstring for OnQuit"""
        self.Close()
        self.Destroy()
    def OnLoad(self, e):
        """docstring for OnLoad"""
        filePath = ""
        dialog = wx.FileDialog(self, message="Choose a deck", defaultDir = os.getcwd(), style = wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filePath = dialog.GetPath()
        
        
        dialog.Destroy()

         
        if not(filePath == ""):
            self.Solver.LoadFile(filePath)
        
            self.Represent(self.Solver.Board)



        pass


    def OnFind(self, e):
        """docstring for OnFind"""
        SET = Solver.Find()
        if len(SET) = 0:
            # Whatever Dialog says No Solution
        else:
            # Dialog that has the three cards
        pass
    def OnGet(self, e):
        """docstring for OnGet"""
        pass          

    def GetImage(self, Card):
        """Returns a BitMap object that matches the card"""
       
        fileString = "".join(Card)
        fileString += ".png"

        fileString = "cards/" + fileString

        BMP = wx.EmptyBitmap(1,1)
        BMP.LoadFile(fileString, wx.BITMAP_TYPE_ANY)

        return BMP
    def Represent(self, Board):
        """docstring for Represent"""
        for i in range(len(Board)):
            cardBMP = self.GetImage(Board[i])
            card = wx.StaticBitmap(self.MainPanel, wx.ID_ANY, cardBMP)
            
            self.tiles.Add(card)
        self.tiles.Layout()
        


app = wx.App()
SetDemo(None)


app.MainLoop()
