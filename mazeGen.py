# Written by Jacob Knutson
from pymel.core import *
import random
import time

if window("m_gen", exists=True):
    deleteUI("m_gen")

# create window and elements on window
win = window("m_gen", title="Maze Generator", height=200, width=300, sizeable=False)

rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(1, 150), (2,100)]) 
text(label="Enter Maze")
text(label=" Attributes", al="left")
separator(h=10)
separator(h=10)

text(label="Number of Cells Long:", align='left')
inputLen = floatField("length", minValue=1, precision=0, value=5)
separator(h=5)
separator(h=5)
text(label="Number of Cells Wide:", al='left')
inputWid = floatField("width", minValue=1, precision=0, value=5)
separator(h=5)
separator(h=5)
text(label="Height of Walls:", al='left')
inputHeight = floatField("height", minValue=0.1, precision=2, value=1)
separator(h=5)
separator(h=5)
text(label="Length of Walls:", al='left')
inputl = floatField("l", minValue=0.1, precision=2, value=5)
separator(h=5)
separator(h=5)

def buttonPressed(*args):
    length = int(inputLen.getValue())
    width = int(inputWid.getValue())
    
    global mGrid
    mGrid = [[Cell() for i in range(length)] for j in range(width)]
    clearMaze()
    mazeGen(length, width, inputHeight.getValue(), inputl.getValue())
    
# deletes any current mazes
def clearMaze(*args):
    if objExists('GeneratedMaze'):
        select('GeneratedMaze')
        delete()
        
random.seed(time.time())

btn = button(label="Generate", command=buttonPressed, w=50, h=25)
separator(5)
btn = button(label="Delete", command=clearMaze, w=50, h=25)
win.show()

# these hold the changes in x and y based on direction moving
xr = {'N':0, 'S':0, 'E':1, 'W':-1}
yr = {'N':1, 'S':-1, 'E':0, 'W':0}
flip = {'N':'S', 'S':'N','W':'E','E':'W'}

# represents if side has wall (1=yes, 0=no)
class Cell:
    def __init__(self):
        self.N = 1
        self.S = 1
        self.E = 1
        self.W = 1
        self.visited = False
     
def mazeGen(length, width, height, lenOfWall):
    createPathFrom(0, 0)
    spawnMaze(length, width, height, lenOfWall)
    
# recursively creates path
def createPathFrom(curX, curY):
    dir = ['N', 'S', 'E', 'W']    # holds possible directions to travel in
    random.shuffle(dir)
    
    # go through each direction and determine if valid movement
    for d in dir:
        newX = curX + xr[d]
        newY = curY + yr[d]
        
        if isValidCell(newX, newY):
            # if it is valid, then continue making path
            mGrid[curX][curY].visited = True
            markDirection(curX, curY, d)
            markDirection(newX, newY, flip[d])
            createPathFrom(newX, newY)
        mGrid[curX][curY].visited = True
   
# returns if valid spot on grid    
def isValidCell(x, y):
    width = len(mGrid)
    height = len(mGrid[0])
    
    if y < 0  or y >= height:
        return False
    elif x < 0 or x >= width:
        return False
    elif mGrid[x][y].visited == True: #has already been visited
        return False
        
    return True
    
   
# marks the given direction as being open
def markDirection(x, y, d):
    if d == 'N':
        mGrid[x][y].N = 0
    elif d == 'S':
        mGrid[x][y].S = 0
    elif d == 'E':
        mGrid[x][y].E = 0
    elif d == 'W':
        mGrid[x][y].W = 0
    
# creates maze in maya
def spawnMaze(length, width, height, lenWall):
    startLength = (length*lenWall/2.)-.25
    startWidth = (width*lenWall/2.)-.25
    group(n='GeneratedMaze')
    
    # create sides of maze
    polyCube(n='leftEdge', h=height, d=width*lenWall, w=.5,)
    move(startLength, height/2, 0)
    parent('leftEdge', 'GeneratedMaze')
    polyCube(n='rightEdge', h=height, d=width*lenWall, w=.5,)
    move((-length*lenWall/2.)+.25, height/2, 0)
    parent('rightEdge', 'GeneratedMaze')
    polyCube(n='topEdge', h=height, d=length*lenWall, w=.5,)
    move(0, height/2, startWidth)
    rotate(0, 0, 90)
    parent('topEdge', 'GeneratedMaze')
    polyCube(n='bottomEdge', h=height, d=length*lenWall, w=.5,)
    move(0, height/2, (-width*lenWall/2.)+.25)
    rotate(0, 0, 90)
    parent('bottomEdge', 'GeneratedMaze')
    
    select(clear=True)
    group(n='interior')
    
    # fill the maze according to created maze
    curW = startWidth-lenWall+.25
    for x, t in enumerate(mGrid):
        curL = startLength-(lenWall/2)+.25
        for y, z in enumerate(t):
            if z.E == 1:
                name = '_' + str(x)+'_'+str(y)+'_East'
                polyCube(n=name, h=height, d=lenWall, w=.5)
                move(curL, height/2, curW)
                rotate(0, 0, 90)
                parent(name, 'interior')
            if z.N == 1:
                name = '_' + str(x)+'_'+str(y)+'_North'
                polyCube(n=name, h=height, d=lenWall, w=.5)
                move(curL-(lenWall/2), height/2, curW+(lenWall/2))
                parent(name, 'interior')
            
            curL = curL - lenWall
        curW = curW - lenWall
    parent('interior', 'GeneratedMaze')
    select('GeneratedMaze')
    
