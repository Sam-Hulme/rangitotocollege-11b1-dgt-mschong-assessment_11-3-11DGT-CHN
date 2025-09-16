'''The actual level design that imports and calls functions from the laser file.'''
import tkinter
from tkinter import *
from laser import *
from core import *
import random



def levelEnd(inactive = False, colour = False): #colour is not used but is passed when the reciever is activated so must be declared
    '''Runs when the level is completed.'''
    if inactive:
        return #If the emitter is not active, dont run
    freeze()
    root.after(2000,nextLevel)

def doorOpen(reverse,colour):
    from laser import doors #Ensure that the doors dictionary is updated
    for i in doors[colour]:
        y = i[0]
        x = i[1]
        if reverse and objects[y][x][0] in ['','l']: #Door overrides lasers
            doorSprite(y,x,colour=colour)
        elif not reverse and objects[y][x][0] == 'd':
            setPanel(y,x,'')
    panels[y][x].tag_raise('frame')

def selectInit(selectedObject,boxes):
    '''Automatically select a box and bind movement keys and mouse clicking to boxes'''
    objectSelect(0, boxes[0])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)


    

# def doorRect(reverse,start,end): 
#     '''Open multiple doors'''
#     for y in range(start[0],end[0]+1):
#         for x in range(start[1],end[1]+1):
#             doorOpen(reverse,y,x)

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


    laserEvent(
        red = levelEnd
        #Put functions for different colours here
        #Use lambda for single expression functions
    )
    
    selectInit((2,7),boxes)


levels.append(level0)
# level0()

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

    laserEvent(
        red = levelEnd
        #Put functions for different colours here
    )
    selectInit((5,3),boxes)

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


    setPanel(5,1,'d',colour='green')

    boxes = []
    boxes.append(boxSprite(3,4,flipped=False))
    boxes.append(boxSprite(8,1,flipped=True))

    emitterSprite(4,8,active=False,dir=3)
    recieverSprite(1,8,laser=False,dir=1,colour='red')
    recieverSprite(0,3,laser=False,dir=0,colour='green')

    selectedObject = [3,4]
    objectSelect(0, boxes[0])


    laserEvent(
        green = lambda reverse: doorOpen(reverse,'green'),
        red = levelEnd #TODO: Make red reciever always the reciever for winning
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


    fillRect([4,1],[4,4],'d',colour='red')

    boxes = []
    boxes.append(boxSprite(4,7,flipped=False))
    boxes.append(boxSprite(5,1,flipped=True))
    boxes.append(boxSprite(3,2,flipped=False))
    boxes.append(boxSprite(7,9,flipped=True))

    emitterSprite(8,7,dir=0)
    recieverSprite(8,2,laser=False,dir=2,colour='red')
    recieverSprite(1,9,laser=False,dir=0,colour="green")

    laserEvent(
       red = doorOpen,
       green = levelEnd  
    )

    selectInit((5,9),boxes)

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


    setPanel(2,3,'d',colour='red')
    setPanel(1,8,'d',colour='green')
    
    boxes = []
    boxes.append(prismSprite(1,2,dir=0))
    boxes.append(boxSprite(1,1,flipped=False))
    boxes.append(boxSprite(7,3,flipped=True))
    boxes.append(boxSprite(1,6,flipped=False)) #TODO: make it more clear that boxes keep doors open
    emitterSprite(9,5,active=False,dir=0)
    recieverSprite(0,3,laser=False,dir=0,colour='green')
    recieverSprite(6,9,laser=False,dir=1,colour='red')
    recieverSprite(1,5,laser=False,dir=3,colour='blue')

    doorOpeners = dict.fromkeys(('red','green'), doorOpen)
    laserEvent(
        **doorOpeners,
        blue = levelEnd
    )


    selectInit((7,3),boxes)
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
    

    


    fillRect([1,5],[2,5],'d',colour='green')
    fillRect([3,6],[3,8],'d',colour='blue')
    fillRect([3,1],[3,4],'d',colour='yellow')
    setPanel(2,0,'d',colour='purple')
    fillRect([4,5],[6,5],'d',colour='orange')


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

    doorOpeners = dict.fromkeys(('green','blue','yellow','putple','orange'), doorOpen)
    laserEvent(
        **doorOpeners,
        red = levelEnd
    )

    #TODO: Split laser doesn't move through door opened on the same frame
    #TODO: Change door functions to allow colour to be set when door created, automatically setting up recievers.

    selectInit((6,6),boxes)
levels.append(level5)


def level6():
    fillRect((4,5),(9,5),'w')
    setPanel(5,5,'g')
    fillRect((3,0),(3,9),'w')
    setPanel(3,8,'g')
    
    emitterSprite(9,7,dir=0)
    emitterSprite(5,9,dir=3,colour='green')
    emitterSprite(9,2,dir=0,colour='blue')
    emitterSprite(1,0,dir=1,colour='yellow')
    emitterSprite(0,8,dir=2,colour='purple')
    
    

    recieverSprite(4,7,dir=0,colour='green')
    recieverSprite(5,0,dir=3,colour='blue')
    recieverSprite(4,2,dir=0,colour='yellow')
    recieverSprite(1,9,dir=1,colour='purple')
    recieverSprite(9,8,dir=2,colour='red')

    emitterActivators = dict.fromkeys(('green','blue','yellow','purple'), emitterActivate)
    laserEvent(
        **emitterActivators
        # red = levelEnd
    )
    
level6()


root.mainloop() #Ensure all functions are defined before this is run.