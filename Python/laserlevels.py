import tkinter
from tkinter import *
from laser import *



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
        if (objects[y][x][0] == ''):
            setPanel(y,x,'d')
        #     print("door closed")
        # else:
        #     print("already closed")

def level0():

    
    fillRect([3,2],[6,6],"f")
    fillRect([2,8],[6,8],'w')
    fillRect([1,2],[1,8],'w')
    # setPanel(2,5,'w')

    boxes = []
    boxes.append(boxSprite(2,7,False))

    emitterSprite(6,7,False,0)
    recieverSprite(2,2,False,3,'red')

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

    fillRect([5,3],[8,6],"f")
    fillRect([3,1],[8,1],"w")
    fillRect([3,8],[8,8],"w")
    fillRect([3,2],[3,7],"w")

    boxes = []
    boxes.append(boxSprite(4,7,False))
    boxes.append(boxSprite(5,3,True))
    # boxes.append(boxSprite(6,5,False))
    # boxes.append(boxSprite(6,6,True))

    emitterSprite(8,7,False,0)
    recieverSprite(8,2,False,2,'red')


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
    fillRect([5,2],[5,8],"w")
    fillRect([2,5],[3,8],"f")
    fillRect([0,9],[8,9],"w")
    fillRect([0,0],[9,0],"w")
    fillRect([0,1],[0,8],'w')
    fillRect([9,1],[9,9],"w")
    fillRect([6,1],[8,8],'f')
    setPanel(5,1,'d')

    boxes = []
    boxes.append(boxSprite(3,4,False))
    boxes.append(boxSprite(8,1,True))

    emitterSprite(4,8,False,3)
    recieverSprite(1,8,False,1,'red')
    recieverSprite(0,3,False,0,'green')

    selectedObject = [5,3]
    objectSelect(0, boxes[0])

    

    laserEvent(
        red = levelEnd,
        green = lambda reverse: doorOpen(reverse,5,1)
        #Put functions for different colours here
    )


    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level2)

def level3():
    fillRect([0,0],[9,9],'w')
    fillRect([1,1],[8,8],'')
    fillRect([2,1],[2,2],'w')
    fillRect([1,4],[2,4],'w')
    setPanel(2,3,'d')
    setPanel(1,8,'d')
    fillRect([2,5],[2,7],'w')
    fillRect([3,1],[8,1],'f')
    
    boxes = []
    boxes.append(prismSprite(1,2,0))
    boxes.append(boxSprite(5,5,False))
    boxes.append(boxSprite(7,3,True))
    boxes.append(boxSprite(1,6,False))
    emitterSprite(9,5,False,0)
    recieverSprite(0,3,False,0,'green')
    recieverSprite(6,9,False,1,'red')
    recieverSprite(1,5,False,3,'blue')


    laserEvent(
        red = lambda reverse: doorOpen(reverse,2,3),
        green = lambda reverse: doorOpen(reverse,1,8),
        blue = levelEnd
    )



    selectedObject = [5,5]
    objectSelect(0, boxes[1])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in boxes:
        i.bind("<Button-1>", objectSelect)
levels.append(level3)


root.mainloop() #Ensure all functions are defined before this is run.