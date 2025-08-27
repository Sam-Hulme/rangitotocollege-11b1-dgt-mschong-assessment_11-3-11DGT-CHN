import tkinter
from tkinter import *
from laser import *


selectedObject = []

fillRect([5,3],[8,6],"f")
fillRect([3,1],[8,1],"w")
fillRect([3,8],[8,8],"w")
fillRect([3,2],[3,7],"w")

boxSprite(4,7,False,'')
boxSprite(5,3,True,'f')
emitterSprite(8,7,False)

selectedObject = [5,3]
root.bind("<Key>",lambda event: objectMove(event, selectedObject))


root.mainloop()