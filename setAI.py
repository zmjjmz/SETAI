#!/usr/bin/python

"""
These properties correspond to the actual SET game
    Properties:
    1 - shape:
        1 oval
        2 squiggle
        3 diamond
    2 - color:
        1 red
        2 green
        3 purple
    3 - shading:
        1 clear
        2 partial
        3 full
    4 - number:
        1 1
        2 2
        3 3

"""
import sys
import random
import math
import pygame

sys.setrecursionlimit(10000)

#Global variables
SET_SIZE = 3
CARD_PROPS = 4
BOARD_SIZE = 12
MAX_COMBO = math.pow(BOARD_SIZE, SET_SIZE)


COUNTER = 0
SET_HASH = set([])

def check(CardList, Board):
    """docstring for check"""
    if len(CardList) != SET_SIZE:
        return False
    for i in range(CARD_PROPS):
        proplist = []
        for j in range(SET_SIZE):
            proplist.append(Board[CardList[j]][i])
        if not((len(set(proplist)) == 1) or (len(set(proplist)) == SET_SIZE)):
            return False
    return True
                
def dfs(Board, workingSet, checkSet, index):
    """docstring for dfs"""
    
    if not(index in checkSet):
        workingSet.append(index)
        checkSet.add(index)
    if len(workingSet) < SET_SIZE:
        print "Adding another card to the set"
        print workingSet
        for i in range(BOARD_SIZE):
            if not(i in checkSet):
                Result = dfs(Board, workingSet, checkSet, i)
                if Result[0]:
                    return True, Result[1]
                else:
                    checkSet.remove(i)
                    workingSet.pop()
                    continue 
        return False,
        """
        if (len(workingSet) == 0):
            if index < len(Board)-1:
                index += 1
                checkSet = set(workingSet)
                return dfs(Board, workingSet, checkSet, index) 

        
        workingSet.pop()
        checkSet = set(workingSet)
        return dfs(Board, workingSet, checkSet, index
        """                        

            
    print "Checking set: " 
    print workingSet
    global COUNTER 
    COUNTER += 1

    if check(workingSet, Board): 
        print "Found a set"
        return (True, workingSet)
    elif COUNTER < MAX_COMBO:
        return False, 
    elif COUNTER == MAX_COMBO:
        print "Found no sets"
        return False,
        
        
def print_set(FinalSet):
    """docstring for printSet"""
    for i in range(SET_SIZE):
        for j in range(CARD_PROPS):
            sys.stdout.write(Board[FinalSet[i]][j])
            sys.stdout.write(" ")
        sys.stdout.write("\n")

if len(sys.argv) == 2:
    inputPath = sys.argv[1]
    inputFile = open(inputPath, 'r')
    Deck = []
    Board = []

    for line in inputFile:
        Deck.append(line.split())

    inputFile.close()
    
    random.shuffle(Deck)


    for i in range(BOARD_SIZE):
        Board.append(Deck.pop())

    workingSet = []
    checkSet = set([])
    foundSet = False
    
    for index in range(BOARD_SIZE):
        
        Result = dfs(Board, workingSet, checkSet, index)
        if (len(Result) == 2):
            foundSet = True
            print_set(Result[1])
            break
        else:
            workingSet[:] = []
            print "Couldn't find set starting with " + str(index)


    if not(foundSet):
        print "Found no sets"
        

else:
    print "No input file provided"



    
    
        







                    

    
        
    
    

