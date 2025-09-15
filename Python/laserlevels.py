'''The actual level design that imports and calls functions from the laser file.'''
import tkinter
from tkinter import *
from laser import *
from core import *
import random



def levelEnd(inactive = False): #Runs when the level is completed
    if inactive:
        return #If the emitter is not active, dont run
    freeze()
    root.after(2000,nextLevel)

def doorOpen(reverse,y,x):
    if not reverse:
        if (objects[y][x][0] == 'd'):
            setPanel(y,x,'')
        #     print("door opened") 
        # else:
        #     print("already open")
    else:
        if (objects[y][x][0] in ['','l']): #Door overrides lasers
            setPanel(y,x,'d')
        #     print("door closed")
        # else:
        #     print("already closed")
    panels[y][x].tag_raise('frame')


def doorRect(reverse,start,end): 
    '''Open multiple doors'''
    for y in range(start[0],end[0]+1):
        for x in range(start[1],end[1]+1):
            doorOpen(reverse,y,x)

def level0():
    '''Basic laser and box reflection intro.'''
    
    fillRect([3,2],[6,6],"f")
    fillRect([2,8],[6,8],'w')
    fillRect([1,2],[1,8],'w')
    # setPanel(2,5,'w')

    boxes = []
    boxes.append(boxSprite(2,7,flipped=False))

    emitterSprite(6,7,active=False,dir=0)
    recieverSprite(2,2,laser=False,dir=3,colour='red')

    selectedObject = [2,7]
    objectSelect(0, boxes[0])



    laserEvent(
        red = levelEnd
        #Put functions for different colours here
        #Use lambda for single expression functions
    )
        

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes: 
        i.bind("<Button-1>", objectSelect)
levels.append(level0)
level0()

def level1():
    '''Moving boxes intro.'''

    fillRect([5,3],[8,6],"f")
    fillRect([3,1],[8,1],"w")
    fillRect([3,8],[8,8],"w")
    fillRect([3,2],[3,7],"w")

    boxes = []
    boxes.append(boxSprite(4,7,flipped=False))
    boxes.append(boxSprite(5,3,flipped=True))
    # boxes.append(boxSprite(6,5,False))
    # boxes.append(boxSprite(6,6,True))

    emitterSprite(8,7,active=False,dir=0)
    recieverSprite(8,2,laser=False,dir=2,colour='red')


    selectedObject = [5,3]
    objectSelect(0, boxes[0])


    laserEvent(
        red = levelEnd
        #Put functions for different colours here
    )


    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level1)

def level2():
    '''Doors intro'''
    fillRect([5,2],[5,8],"w")
    fillRect([2,5],[3,8],"f")
    fillRect([0,9],[8,9],"w")
    fillRect([0,0],[9,0],"w")
    fillRect([0,1],[0,8],'w')
    fillRect([9,1],[9,9],"w")
    fillRect([6,1],[8,8],'f')

    doors = []
    doors.append(setPanel(5,1,'d'))

    boxes = []
    boxes.append(boxSprite(3,4,flipped=False))
    boxes.append(boxSprite(8,1,flipped=True))

    emitterSprite(4,8,active=False,dir=3)
    recieverSprite(1,8,laser=False,dir=1,colour='red')
    recieverSprite(0,3,laser=False,dir=0,colour='green')

    selectedObject = [3,4]
    objectSelect(0, boxes[0])


    laserEvent(doors,
        green = lambda reverse: doorOpen(reverse,5,1),
        red = levelEnd
        #Put functions for different colours here
    )


    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level2)


def level3():
    '''Glass intro'''
    fillRect([0,0],[9,9],'w')
    fillRect([1,1],[8,9],'')
    fillRect([1,5],[8,5],'g')
    fillRect([1,6],[3,7],'f')
    fillRect([1,8],[8,8],'g')

    doors = []
    doors.append(fillRect([4,1],[4,4],'d'))

    boxes = []
    boxes.append(boxSprite(4,7,flipped=False))
    boxes.append(boxSprite(5,1,flipped=True))
    boxes.append(boxSprite(3,2,flipped=False))
    boxes.append(boxSprite(7,9,flipped=True))

    emitterSprite(8,7,dir=0)
    recieverSprite(8,2,laser=False,dir=2,colour='red')
    recieverSprite(1,9,laser=False,dir=0,colour="green")

    def red(reverse):
        for i in range(5):
            doorOpen(reverse,4,i)

    laserEvent(doors,
       red = lambda reverse: red(reverse),
       green = levelEnd  
    )

    selectedObject = [5,9]
    objectSelect(0, boxes[0])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level3)

def level4():
    '''Prism intro'''
    fillRect([0,0],[9,9],'w')
    fillRect([1,1],[8,8],'')
    fillRect([2,1],[2,2],'w')
    fillRect([1,4],[2,4],'w')
    fillRect([2,5],[2,7],'w')
    fillRect([3,1],[8,1],'f')
    fillRect([3,5],[5,5],'w')
    glassSprite(2,8)

    doors = []
    doors.append(setPanel(2,3,'d'))
    doors.append(setPanel(1,8,'d'))
    
    boxes = []
    boxes.append(prismSprite(1,2,dir=0))
    boxes.append(boxSprite(1,1,flipped=False))
    boxes.append(boxSprite(7,3,flipped=True))
    boxes.append(boxSprite(1,6,flipped=False))
    emitterSprite(9,5,active=False,dir=0)
    recieverSprite(0,3,laser=False,dir=0,colour='green')
    recieverSprite(6,9,laser=False,dir=1,colour='red')
    recieverSprite(1,5,laser=False,dir=3,colour='blue')


    laserEvent(doors,
        red = lambda reverse: doorOpen(reverse,2,3),
        green = lambda reverse: doorOpen(reverse,1,8),
        blue = levelEnd
    )


    selectedObject = [7,3]
    objectSelect(0, boxes[2])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level4)

# def level5():
#     possibleTiles = ['','w','f','b','p','e','r','d','l']
#     for a in panels:
#         for b in a:
#             coords = b.grid_info()
#             y = coords['row']
#             x = coords['column']
#             tile = random.choice(possibleTiles)
#             fillRect([y,x],[y,x],tile,dir=0,flipped=False,laser=False,emitter=False,rot='y',active=False,colour='none')
            
def level5():
    '''Advanced prisms'''
    fillRect([0,0],[9,9],'w')
    fillRect([1,1],[8,8],'')
    fillRect([7,5],[8,5],'w')
    fillRect([4,1],[8,1],'f')
    setPanel(3,5,'w')
    setPanel(1,0,'')
    

    

    doors = []
    doors.append(fillRect([1,5],[2,5],'d'))
    doors.append(fillRect([3,6],[3,8],'d'))
    doors.append(fillRect([3,1],[3,4],'d'))
    doors.append(setPanel(2,0,'d'))
    doors.append(fillRect([4,5],[6,5],'d'))


    boxes = []
    boxes.append(prismSprite(6,6,dir=3))
    boxes.append(boxSprite(1,7,flipped=True))
    boxes.append(prismSprite(1,4,dir=0))
    boxes.append(boxSprite(7,4,flipped=False))
    boxes.append(prismSprite(1,0,dir=3))
    emitterSprite(5,9,active=False,dir=3)
    recieverSprite(1,8,laser=False,dir=1,colour='green')
    recieverSprite(9,7,laser=False,dir=2,colour='blue')
    recieverSprite(0,3,laser=False,dir=0,colour='yellow')
    recieverSprite(1,1,laser=False,dir=3,colour='purple')
    recieverSprite(9,3,laser=False,dir=2,colour='orange')
    recieverSprite(7,9,laser=False,dir=1,colour='red')



    laserEvent(doors,
        green = lambda reverse: doorRect(reverse,[1,5],[2,5]),
        blue = lambda reverse: doorRect(reverse,[3,6],[3,8]),
        yellow = lambda reverse: doorRect(reverse,[3,1],[3,4]),
        purple = lambda reverse: doorOpen(reverse,2,0),
        orange = lambda reverse: doorRect(reverse,[4,5],[6,5]),
        red = levelEnd
    )

    #TODO: Split laser doesn't move through door opened on the same frame
    #TODO: Change door functions to allow colour to be set when door created, automatically setting up recievers.

    selectedObject = [6,6]
    objectSelect(0, boxes[0])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level5)

# def level6():
#     setPanel(0,0,'w')
# level6()


root.mainloop() #Ensure all functions are defined before this is run.