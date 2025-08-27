import tkinter
from tkinter import *

root = tkinter.Tk()
root.configure(bg='red')

#This game uses a panel system for elements, with a grid of canvases that can be modified to have images or solid colours displayed.
panelColumns = 10
panelRows = 10
panelWidth = 64
panelHeight = 64
panels = [[]] #The canvases themselves that will be drawn to to show sprites.
objects = [[]] #A grid of empty strings that will be filled to reflect the types of objects at each location
objectColours = { # A dictionary of the colours of solid colour objects
    "w":"#367FEC",
    "f": "#555555"
}
"""
    w = Wall
    f = floor
    [empty] = nothing
    b = box
    l = laser
    e = emitter
"""

laserFloors = []
selectedObject = []
laserData = [[0,0,0,False],[0,0,0,False]]
# def init(): #Run once to initialise an empty level, returns a 2d array with all the canvas objects. Running again will reset the level.
#     objects = [[]]
#     for a in panels:
#         for i in a:
#             i.destroy() #Destroy existing panels (if the function is run multiple times)
for i in range(panelColumns*panelRows):
    row = len(panels)-1
    if (len(panels[row])+1 > panelColumns): #if the current row list would have more items than the desired column count, move to the next row
        panels.append([])
        objects.append([])
    row = len(panels)-1
    column = len(panels[row])
    panel = Canvas(root, width=panelWidth, height=panelHeight, bg="black", highlightthickness=0, bd=0)
    panel.grid(row=row, column=column)
    panels[row].append(panel) #Add all panels to a list (so they can be iterated through)
    objects[row].append(['','',''])
    # return panels

def setPanel(y, x, type): #set a single panel to a solid colour object
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type])
    objects[y][x][0] = type
    

# for i in range(3,9):
#    solidColour(panels[i][8],"#367FEC")

# for i in range(2,8):
#     solidColour(panels[3][i],"#367FEC")

def fillRect(startCoords,endCoords,type): #Fill a rectangle of panels
    for x in range(startCoords[1],endCoords[1]+1):
        for y in range(startCoords[0],endCoords[0]+1):
            panels[y][x].delete("all") #Delete what is currently in the panel to not waste memory
            panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type])
            objects[y][x][0] = type
            #panels[y][x].create_text(panelWidth/2,panelHeight/2,text=type)



def boxSprite(y,x,flipped,under):
    panels[y][x].delete("all")
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,outline="#787FB6",width=8,fill="#171717")
    startX = panelWidth/4.5
    endX = panelWidth-panelWidth/4.5
    if flipped:
        temp = startX #Temporarily write startX to a variable so they can be swapped
        startX = endX
        endX = temp
    panels[y][x].create_line(startX,panelHeight/4.5,endX,panelHeight-panelHeight/4.5,fill="#62f960",width=5)
    objects[y][x][0] = "b"
    objects[y][x][1] = flipped
    objects[y][x][2] = under

def laserSprite(x,y,rot,emitter = False):
    if not emitter:
        panels[y][x].delete("all") #Don't delete the emitter sprite
    if (rot == 'y'):
        startX = panelWidth/2
        startY = 0
        endX = startX
        endY = panelHeight
        if (emitter):
            endY = panelHeight*0.75
    elif (rot == 'x'):
        startX = 0
        startY = panelHeight/2
        endX = panelWidth
        endY = startY
        if (emitter):
            endX = panelWidth*0.75
    panels[y][x].create_line(startX,startY,endX,endY,width=20,fill="#FF6A6A")
    panels[y][x].create_line(startX,startY,endX,endY,width=12,fill="#d10202")
    objects[y][x][0] = "l"

def emitterSprite(y,x,active):
    panels[y][x].delete("all")
    panels[y][x].create_oval(0,panelHeight/2,panelWidth,panelHeight,outline="#b0b0b0",fill="#3e3e3e",width=6)
    objects[y][x][0] = "e"
    if (active == True):
        laserSprite(x,y,"y",True)
    panels[y][x].bind("<Button-1>", lambda event: laserMove(y,x,0))
    
def laserMove(y,x,dir):
    emitterSprite(y,x,True)
    laserData[0] = [y,x,dir,True]
    for l in objects:
        for i in l:
            if i[0] == "l":
                panels[i]
    while True: # 0 = up, 1 = right, 2 = down, 3 = left (this is the side of the box, the laser will have the oppisite number)
        if (dir == 0):
            y -= 1
            rot = "y"
        elif (dir == 1):
            x += 1
            rot = "x"
        elif (dir == 2):
            y += 1
            rot = "y"
        elif dir == 3:
            x -= 1
            rot = "x"
        try:
            if (x < 0 or y < 0):
                raise IndexError
            elif (objects[y][x][0] == "w" or objects[y][x][0] == "f"):
                if objects[y][x][0] == "f":
                    panels[y][x].delete("all") #Delete what is currently in the panel to not waste memory
                    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill="#523B3B")
                    objects[y][x][1] = True
                    laserFloors.append(panels[y][x]) #Save the glowing panel to a list so it can be iterated and reset when the laser is updated.
                break #If laser collides with a wall, floor, or leaves the screen, stop running.
            elif (objects[y][x][0] == "b"):
                boxFlipped = objects[y][x][1]
                if (boxFlipped and (dir == 3 or dir == 1)) or (not boxFlipped and (dir == 2 or dir == 0)):
                    dir -= 1
                    if dir < 0:
                        dir = 3
                else:
                    dir += 1
                    if dir > 3:
                        dir = 0
            else:
                laserSprite(x,y,rot)
            #panels[y][x].create_text(panelWidth/2, panelHeight/2, text=dir) #Debug code to check the direction of lasers
        except IndexError:
            break #If it tries to check a panel outside the range, which means it has left the screen and should stop.

def objectMove(event, object):
    global selectedObject
    if (len(selectedObject) == 0):
        selectedObject = object
    x = selectedObject[1]
    y = selectedObject[0]
    type = objects[y][x][0]
    flipped = objects[y][x][1]
    if objects[y][x][2] != '':
        setPanel(y,x,objects[y][x][2])
    else:
        panels[y][x].delete("all")
        objects[y][x] = ['','','']

    if (event.keysym == "w"):
        y -= 1
        if y < 0:
            y = 0
    elif event.keysym == "a":
        x -= 1
        if x < 0:
            x = 0
    elif event.keysym == 's':
        y += 1
        if y > 9:
            y = 9
    elif event.keysym == 'd':
        x += 1
        if x > 9:
            x = 9

    if (type == "b"):
        boxSprite(y,x,flipped,objects[y][x][0])
    selectedObject = [y,x]
    if laserData[0][3]:
        laserMove(laserData[0][0],laserData[0][1],laserData[0][2])
    # print(selectedObject)
    

#TODO: Make it remember what tiles are supposed to be floors if another object is on top.
#TODO: Move sprite functions to seperate file


    
# for i in objects:
#     print(i)



