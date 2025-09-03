import tkinter
from tkinter import *
from laser import *



def levelEnd(): #Runs when the level is completed
    freeze()
    root.after(2000,nextLevel)



def level0():
    global colours
    colours = [False]
    
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
    global colours
    colours = [False]

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

root.mainloop()