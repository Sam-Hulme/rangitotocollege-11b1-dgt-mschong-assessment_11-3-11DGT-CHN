import tkinter
from tkinter import *

root = tkinter.Tk()
root.configure(bg='red')

#This game uses a panel system for elements, with a grid of canvases that can be modified to have images or solid colours displayed.
panelColumns = 10
panelRows = 10
panelWidth = 64 #These values can be adjusted and everything will be resized accordingly.
panelHeight = 64
panels = [[]] #The canvases themselves that will be drawn to to show sprites.
objects = [[]] #A grid of empty strings that will be filled to reflect the types of objects at each location
objectColours = { # A dictionary of the colours of solid colour objects
    "w":"#367FEC",
    "f": "#555555"
}
"""
    w = Wall,
    f = floor,
    [empty] = nothing,
    b = box,
    l = laser,
    e = emitter,
    r = reciever
"""
boxBlocks = ['b','w','e','r'] #Objects that block box movement

levels = []
level = 0
colours = []

laserFloors = []
selectedObject = []
laserEmitter = [0,0,0,False]
laserRecievers = {}
laserEvents = {}
frozen = False
global selectLoop #The event for the selected rectangle moving animation
selectLoopFrames = 0
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

panels[0][0].create_text(32,32,text=level,fill='white')
def nextLevel(): #Reset everything and start the next level
    global level
    global laserFloors
    global laserData
    global selectedObject
    global objects
    global laserEmitter
    global laserRecievers
    global laserEvents
    global frozen
    for y in range(10):
        for x in range(10):
            panels[y][x].delete("all") #Clear all panels in the level
            objects[y][x] = ['','',''] #Reset object array
    root.unbind_all("<Button-1>")
    root.unbind_all("<Key>")
    laserFloors = [] #Reset all variables
    laserData = laserData = [[0,0,0,False],[0,0,0,False]]
    selectedObject = []
    laserEmitter = [0,0,0,False]
    laserRecievers = {}
    laserEvents = {}
    frozen = False

    level += 1
    panels[0][0].create_text(32,32,text=level,fill='white')
    levels[level]()

def freeze(): #Unbind everything to freeze the level
    global frozen
    root.unbind_all("<Key>")
    root.unbind_all("<Button-1>")
    frozen = True


def setPanel(y, x, type): #set a single panel to a solid colour object
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type], tags="main")
    objects[y][x][0] = type
    

# for i in range(3,9):
#    solidColour(panels[i][8],"#367FEC")

# for i in range(2,8):
#     solidColour(panels[3][i],"#367FEC")

def fillRect(startCoords,endCoords,type): #Fill a rectangle of panels
    for x in range(startCoords[1],endCoords[1]+1):
        for y in range(startCoords[0],endCoords[0]+1):
            panels[y][x].delete("main") #Delete what is currently in the panel to not waste memory
            panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type], tags="main")
            objects[y][x][0] = type
            #panels[y][x].create_text(panelWidth/2,panelHeight/2,text=type)



def boxSprite(y,x,flipped):
    panels[y][x].delete("main")
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,outline="#787FB6",width=8,fill="#171717", tags="main")
    startX = panelWidth/4.5
    endX = panelWidth-panelWidth/4.5
    if flipped:
        temp = startX #Temporarily write startX to a variable so they can be swapped
        startX = endX
        endX = temp
    panels[y][x].create_line(startX,panelHeight/4.5,endX,panelHeight-panelHeight/4.5,fill="#62f960",width=5, tags="main")
    objects[y][x][2] = objects[y][x][0]
    objects[y][x][0] = "b"
    objects[y][x][1] = flipped
    return panels[y][x]

def laserSprite(x,y,rot,emitter = False):
    if not emitter and not objects[y][x][0] == 'l': 
        panels[y][x].delete("main") #Don't delete the emitter sprite or the sprite of other lasers (if laser goes over itself)
        objects[y][x][0] = "l"
    if (rot == 'y'):
        startX = panelWidth/2
        startY = 0
        endX = startX
        endY = panelHeight
        dir = panelWidth
        if (emitter):
            endY = panelHeight*0.75
    elif (rot == 'x'):
        startX = 0
        startY = panelHeight/2
        endX = panelWidth
        endY = startY
        dir = panelHeight #The dimension to use to determine the size of the laser
        if (emitter):
            endX = panelWidth*0.75
    panels[y][x].create_line(startX,startY,endX,endY,width=dir/3.2,fill="#FF6A6A", tags="main")
    panels[y][x].create_line(startX,startY,endX,endY,width=dir/(64/12),fill="#d10202", tags="main")

def emitterSprite(y,x,active,dir): #As with most things, 0 = up, 1 = right, 2 = down, and 3 = left
    #TODO: make versions of emitter and reciever sprites at different orientations
    panels[y][x].delete("main") 
    panels[y][x].create_oval(0,panelHeight/2,panelWidth,panelHeight,outline="#b0b0b0",fill="#3e3e3e",width=6, tags="main")
    panels[y][x].unbind("<Button-1>")
    if (active == True):
        laserSprite(x,y,"y",True)
    objects[y][x][0] = "e"
    objects[y][x][1] = dir
    panels[y][x].bind("<Button-1>", lambda event: laserMove(y,x,dir))

def recieverSprite(y,x,laser,dir,colour):
    #Note: Dir will be the direction of the incoming laser, so it will be inverted from the direction of the emitter
    laserRecievers[colour] = [y,x,dir,laser]
    panels[y][x].delete("main")
    oval = panels[y][x].create_oval(0,panelHeight/2,panelWidth,panelHeight,outline="#f62d2d",fill="#3e3e3e",width=6, tags="main")
    if dir == 0 or dir == 2:
        laserdir = 'y'
    else:
        laserdir = 'x'
    if (laser):
        laserSprite(x,y,laserdir,True)
        panels[y][x].itemconfig(oval, fill="#f88080")
    objects[y][x][0] = 'r'
    objects[y][x][1] = dir
    objects[y][x][2] = colour
    
    
def laserMove(y,x,dir):
    emitterSprite(y,x,True,dir)
    for c, i in laserRecievers.items():
        recieverSprite(i[0],i[1],False,i[2],c)
    global laserEmitter
    laserEmitter = [y,x,dir,True]
    yLoop = 0
    xLoop = 0
    for l in objects: #Iterate over existing lasers to remove them
        for i in l:
            if i[0] == "l":
                panels[yLoop][xLoop].delete("main")
                objects[yLoop][xLoop] = ['','','']
            xLoop += 1
        xLoop = 0    
        yLoop += 1
    for i in laserFloors: #Reset glowing floors
        setPanel(i[0],i[1],'f')
        laserFloors.remove(i)
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
                raise IndexError #Also raise indexerror if the coordinates go below zero
            elif (objects[y][x][0] == "w" or objects[y][x][0] == "f"):
                if objects[y][x][0] == "f":
                    panels[y][x].delete("main") #Delete what is currently in the panel to not waste memory
                    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill="#523B3B", tags="main")
                    objects[y][x][1] = True
                    laserFloors.append([y,x]) #Save the glowing panel to a list so it can be iterated and reset when the laser is updated.
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
            elif (objects[y][x][0] == 'r'): 
                    recieverSprite(y,x,True,dir,objects[y][x][2])
                    laserEvents[objects[y][x][2]]()
                    break
            else:
                laserSprite(x,y,rot)
            #panels[y][x].create_text(panelWidth/2, panelHeight/2, text=dir) #Debug code to check the direction of lasers
        except IndexError:
            break #If it tries to check a panel outside the range, which means it has left the screen and should stop.

def objectMove(event, object):
    if frozen:
        return
    global selectedObject
    if (len(selectedObject) == 0):
        selectedObject = object
    x = selectedObject[1]
    y = selectedObject[0]
    type = objects[y][x][0]
    flipped = objects[y][x][1]
    panels[y][x].unbind("<Button-1>") #Unbind move select
    panels[y][x].delete("selected")
    if objects[y][x][2] not in ['','l']:
        setPanel(y,x,objects[y][x][2])
    else:
        panels[y][x].delete("main")
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
    if objects[y][x][0] in boxBlocks: 
        y = selectedObject[0]
        x = selectedObject[1] #Revert movement, making functions below replace existing box that was removed above.
    if (type == "b"):
        boxSprite(y,x,flipped)
    selectedObject = [y,x]
    panels[y][x].bind("<Button-1>", objectSelect)
    panels[0][0].delete("all")
    panels[0][0].create_text(32,32,text=[y,x],fill="white")
    if [y,x] in laserFloors:
        laserFloors.remove([y,x])
    if laserEmitter[3]:
        laserMove(laserEmitter[0],laserEmitter[1],laserEmitter[2])
    selectIndicator()
    # print(selectedObject)

def objectSelect(event, object = 0):
    if (event != 0):
        object = event.widget
    global selectedObject
    objectInfo = object.grid_info()
    y = objectInfo['row']
    x = objectInfo['column']
    if (len(selectedObject) == 0):
        selectedObject = [y,x] #TODO: Make it set objectSelect to the objects position, not the panel itself.
    else:
        old = panels[selectedObject[0]][selectedObject[1]]
        old.delete('selected') #Delete the border from the old panel
    selectedObject = [y,x]
    selectIndicator()

def selectIndicator():
    global selectedObject
    x = selectedObject[1]
    y = selectedObject[0]
    panels[y][x].delete('selected')
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight, outline="green", width=16, fill='', tags='selected') #Empty fill to make it only an outline
    
def selectAnimation(y,x):
    global selectLoopFrames
    #TODO: make animation for selected object frame
    

def laserEvent(**events):
    global laserEvents
    laserEvents = events


    
# for i in objects:
#     print(i)



