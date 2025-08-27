import tkinter
from tkinter import *
from laser import *


selectedObject = []

fillRect([5,3],[8,6],"f")
fillRect([3,1],[8,1],"w")
fillRect([3,8],[8,8],"w")
fillRect([3,2],[3,7],"w")

box1 = boxSprite(4,7,False,'')
box2 = boxSprite(5,3,True,'f')
emitterSprite(8,7,False,0)

selectedObject = [5,3]
root.bind("<Key>",lambda event: objectMove(event, selectedObject))
box1.bind("<Button-1>", lambda event: objectSelect(box1))
box2.bind("<Button-1>", lambda event: objectSelect(box2))


root.mainloop()