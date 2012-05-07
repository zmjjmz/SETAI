#!/usr/bin/python

import wx
import os
import random

APP_EXIT = 1
LOAD_FILE = 2
FIND_SET = 3
GET_BOARD = 4




class AI:
    """Class that keeps track of game settings and has methods for solving SET"""
    def __init__(self, _boardsize=12, _setsize=3, _props=4):
        self.Deck = []
        self.Board = []

        self.boardsize = _boardsize
        self.setsize = _setsize
        self.props = _props
        
        

    def LoadFile(self, filePath):
        """Loads a file into Deck, then pops off boardsize cards into Board"""
        fLoad = open(filePath, 'r')
        
        for line in fLoad:
            self.Deck.append(line.split())
        fLoad.close()

        random.shuffle(self.Deck)

        for i in range(self.boardsize):
            self.Board.append(self.Deck.pop())


    def check(self, CardList, Board):
        """Algorithm for checking whether a set is valid. Can be made more efficient (currently in O(pnlogn), should be O(pn) where p = props and n = setsize"""
        if len(CardList) != self.setsize:
            return False
        for i in range(self.props):
            proplist = []
            for j in range(self.setsize):
                proplist.append(Board[CardList[j]][i])
            if not((len(set(proplist)) == 1) or (len(set(proplist)) == self.setsize)):
                return False
        return True
     
    def dfs(self, Board, workingSet, checkSet, index):
        """Recursive call for finding sets."""
        
        if not(index in checkSet):
            workingSet.append(index)
            checkSet.add(index)
        if len(workingSet) < self.setsize:
            for i in range(self.boardsize):
                if not(i in checkSet):
                    Result = self.dfs(Board, workingSet, checkSet, i)
                    if Result[0]:
                        return True, Result[1]
                    else:
                        checkSet.remove(i)
                        workingSet.pop()
                        continue 
            return False,
                       

        if self.check(workingSet, Board): 
            return (True, workingSet)
        else:
            return False,
        

     
    def Find(self):
        """Driver function for dfs"""
        for index in range(self.boardsize):
        
            workingSet = []
            checkSet = set(workingSet)
            Result = self.dfs(self.Board, workingSet, checkSet, index)
            if (len(Result) == 2):
                return Result 
            else:
                workingSet[:] = []


        return False,
         
        
        

class SetDemo(wx.Frame):
    """Class that handles all graphical interactions"""
    def __init__(self, arg):
        super(SetDemo, self).__init__(arg)
        self.arg = arg
        self.FoundResult = []
        self.Solver = AI()
        self.tiles = wx.GridSizer(self.Solver.setsize,self.Solver.props,2,2)
        self.MainPanel = wx.Panel(self, style=wx.SUNKEN_BORDER)

        self.tiles.SetContainingWindow(self.MainPanel)
        self.MainPanel.SetSizer(self.tiles)




        self.InitUI()
    
    def InitUI(self):
        """Initializes the UI"""

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
        """Event that handles closing the application"""
        self.Close()
        self.Destroy()
    def OnLoad(self, e):
        """Event that handles loading the deck file through a dialog"""
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
        """Event that calls the AI.Find() method, then updates the Layout to show the solution"""
        SET = self.Solver.Find()
        if len(SET) == 2:
            
            cards = set(SET[1])
            
            for item in range(self.Solver.boardsize):
                if not(item in cards):
                    Item = self.tiles.GetItem(item)
                    if Item.IsShown():
                        Item.Show(False)

            self.tiles.Layout()

            wx.MessageBox('Press when done viewing solution','', wx.OK)
            
            self.FoundResult = SET[1]
            self.UpdateBoard()

        else:
            wx.MessageBox('No Solution', 'Result', wx.OK)
            for i in range(self.Solver.setsize):
                self.FoundResult.append(random.randint(0,self.Solver.boardsize - 1))
            self.UpdateBoard()
        pass
        
    def OnGet(self, e):
        """Event that calls UpdateBoard()"""        
        self.UpdateBoard()
        pass          
    
    def UpdateBoard(self):
        """Updates the AI's internal representation of the Board, then calls Represent, also handles case where deck is emptied"""
        cards = set(self.FoundResult)
        
        if len(self.Solver.Deck) < self.Solver.setsize:
            choices = ['Yes','Quit']
            contDlg = wx.SingleChoiceDialog(self, "Deck is out of cards. Load new deck?", "Continue", choices, wx.YES_NO)
            contDlg.ShowModal()
            selection = contDlg.GetSelection()
            if selection == 0:
               wx.MessageBox("Select new deck from Load File", "Do this", wx.OK) 
               self.Solver.Board = []
               self.Solver.Deck = []
               self.FoundResult = []
               self.tiles.Clear(True)
               pass
                
            else:
                self.Destroy()

            

        for i in range(self.Solver.setsize):
            card = self.Solver.Deck.pop()  
            self.Solver.Board[self.FoundResult[i]] = card

                
        self.tiles.Clear(True)
        self.tiles.Layout()

        self.Represent(self.Solver.Board)

        self.FoundResult = []


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
        """Updates GUI to represent AI's internal Board representation"""
        for i in range(len(Board)):
            cardBMP = self.GetImage(Board[i])
            card = wx.StaticBitmap(self.MainPanel, wx.ID_ANY, cardBMP)
            
            self.tiles.Add(card)
        self.tiles.Layout()
        


app = wx.App()
SetDemo(None)


app.MainLoop()
