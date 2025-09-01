import tkinter
from tkinter import *
from laser import *


selectedObject = []

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
recieverSprite(8,2,False,2)


selectedObject = [5,3]
objectSelect(0, boxes[0])


root.bind("<Key>",lambda event: objectMove(event, selectedObject))
for i in boxes:
    i.bind("<Button-1>", objectSelect)


root.mainloop()