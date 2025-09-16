'''All the functions and variables for the laser game'''
from tkinter import *
from core import *
import time

root.title("Laser")

objectColours = { # A dictionary of the colours of solid colour objects
    "w":"#367FEC",
    "f": "#555555"
    # "d": "#F3C873" #TODO: Add proper sprite for doors
}
objectSprites = {} #This dictionary is filled after functions are defined to avoid errors.
laserColours = {
    'red': "#f62d2d",
    'green': "#37EA0A",
    'blue': "#203AFF",
    'yellow': "#F2EB1E",
    'purple': "#C41EF2",
    'orange': "#F87219"
}
frameColours = { #Darker colours for frames which look less out of place on doors.
    'red': "#971f1f",
    'green': "#259509",
    'blue': "#142394",
    'yellow': "#B39B16",
    'purple': "#821A9F",
    'orange': "#B65218"
}
"""
    w = Wall,
    f = floor,
    [empty] = nothing,
    b = box,
    l = laser,
    e = emitter,
    r = reciever,
    d = door,
    p = prism
"""
boxBlocks = ['b','w','e','r','d','p','g'] #Objects that block box movement
laserBlocks = ['f','w','d']

levels = []
level = 0


laserFloors = []
selectedObject = []
laserEmitters = {
    False: [0,0,0,False]
}
laserRecievers = {}
laserEvents = {}
doors = {}
frozen = False
global selectLoop #The event for the selected rectangle moving animation
selectLoopFrames = 0
# def init(): #Run once to initialise an empty level, returns a 2d array with all the canvas objects. Running again will reset the level.
#     objects = [[]]
#     for a in panels:
#         for i in a:
#             i.destroy() #Destroy existing panels (if the function is run multiple times)
init(columns=10,rows=10,width=64,height=64)
from core import panelWidth, panelHeight


def nextLevel(): #Reset everything and start the next level
    global level
    global laserFloors
    global laserData
    global selectedObject
    global objects
    global laserEmitters
    global laserRecievers
    global laserEvents
    global frozen
    global doors
    for y in range(10):
        for x in range(10):
            panels[y][x].delete("all") #Clear all panels in the level
            objects[y][x] = ['','',''] #Reset object array
            panels[y][x].unbind("<Button-1>")
    root.unbind_all("<Key>")
    laserFloors = [] #Reset all variables
    laserData = [[0,0,0,False],[0,0,0,False]]
    selectedObject = []
    laserEmitters = {False: [0,0,0,False]}
    laserRecievers = {}
    laserEvents = {}
    doors = {}
    frozen = False

    level += 1
    levels[level]()

def freeze(): #Unbind everything to freeze the level
    global frozen
    root.unbind_all("<Key>")
    frozen = True


def setPanel(y, x, type, **data): #set a single panel to a solid colour object
    panels[y][x].delete("main")
    if type in objectColours:
        panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type], tags="main")
    elif not type == '':
        objectSprites[type](y,x,**data)
    objects[y][x][0] = type
    return panels[y][x]
    

# for i in range(3,9):
#    solidColour(panels[i][8],"#367FEC")

# for i in range(2,8):
#     solidColour(panels[3][i],"#367FEC")

"""
IDEAS:

Box that is destroyed by the laser:
    Object that respawns the box if it is destroyed
    Breaking animation
    Spawn boxes behind a door to force player to start laser
    'box detector' that activates a colour similar to a reciever when box is moved on top
    Rename current reflector box to 'mirror' to avoid confusion
    Box sprite looks like a light brown crate (subject to change)
    Could be introduced in level 7

Emitters activated by recievers:
    Short delay with emitter 'warming up' to make it clear what is happening
    Redo emitter sprite:
        To avoid confusion and better seperate them, give emitters new sprites
        The sprite will feature a triangle from the bottom of the panel to around 3/4 or 4/5 up
        At the top of the triangle there is a circle with a larger circle around it.
        The laser starts from the middle of the circle
        Both circles glow red when the emitter is active
        Two rings around halfway up the emitter that are coloured based on what reciever activates it (grey for default player activated emitter)
    Could be introduced in level 6

'Bluetooth' boxes:
    Boxes come in pairs with a circle and a spiral shape in the middle.
    Colour of the spiral determines which box connects to which.
    Laser goes in one box and comes out the other in the same direction.
    Both boxes can be moved just like any other.
    Might be scrapped if too many other features are added.

Level transition animation:
    Rather than instantly switching levels, have an animation of the laser moving to the next level
    Empty level with laser in the middle from one side of the screen to the other
    Have occasional white objects move backwards quickly to make it look like the laser is moving fast
    Make each level end with the laser going off the screen in the appropriate direction for the next level's first emitter
    The laser reaches the next level and hits the bottom of the emitter, which activates when clicked like normal

"""

def fillRect(startCoords,endCoords,type,**data): #Fill a rectangle of panels
    objectsCreated = []
    xStep = 1 # geometry dash reference???
    yStep = 1
    if startCoords[1] > endCoords[1]: #If start x is more than end x, go backwards
        xStep = -1
    if startCoords[0] > endCoords[0]:
        yStep = -1
    for x in range(startCoords[1],endCoords[1]+1,xStep):
        for y in range(startCoords[0],endCoords[0]+1,yStep):
            panels[y][x].delete("main") #Delete what is currently in the panel to not waste memory
            if type in objectColours.keys():
                panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill=objectColours[type], tags="main")
            elif not type == '':
                objectSprites[type](y,x,**data)
            objects[y][x][0] = type
            objectsCreated.append(panels[y][x])
    return objectsCreated
            #panels[y][x].create_text(panelWidth/2,panelHeight/2,text=type)



def boxSprite(y,x,**data):
    '''
    data:
    flipped (bool)
    '''
    flipped = data['flipped'] #Object data (direction, colour, ect) is passed through **kwargs so that fillRect can work for all of them
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

def prismSprite(y,x,**data):
    '''
    data:
    dir (int)
    '''
    dir = data['dir']
    panels[y][x].delete("main")
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,outline="#EE78EE",width=8,fill="#3C3C3C", tags='main')
    w = panelWidth
    h = panelHeight
    scale = 4
    xq1 = w/scale #x quarter 1
    xq2 = w/2
    xq3 = w-w/scale
    yq1 = h/scale
    yq2 = h/2
    yq3 = h-h/scale


    x1 = xq2 #Half way across
    y1 = yq1 #A quarter down

    x2 = xq1 #A quarter across
    y2 = yq3 #3 quarters down

    x3 = xq3 #3 quarters across
    y3 = yq3 #3 quarters down
    if (dir == 2):
        y2 = h/scale
        y3 = h/scale
        y1 = h-h/scale
    elif dir == 1:
        x1 = xq1
        x3 = xq3
        y3 = yq2
    elif dir == 3:
        x1 = xq3
        x2 = xq3
        y3 = xq2
        x3 = xq1

    # elif dir == 1:
    #     x1 = 
    panels[y][x].create_polygon(x1,y1,x2,y2,x3,y3, fill="#A7A7A7",tags='main')
    objects[y][x][2] = objects[y][x][0]
    objects[y][x][0] = 'p'
    objects[y][x][1] = dir
    #One point should be half way across and a third down. The other two should be two thirds down and at opisote thirds
    return panels[y][x]

def glassSprite(y,x,**data):
    '''
    data:
    laser (bool)
    '''
    if 'laser' in data:
        laser = data['laser']
    else:
        laser = False
    if not laser:
        panels[y][x].delete('main')
        objects[y][x] = ['','','']
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill='',outline='#EEEEEE',width=8,tags='main')
    w = panelWidth/9
    h = panelHeight/9

    panels[y][x].create_line(w*2,h,w,h*2,width=4,fill='#EEEEEE',tags='main')
    panels[y][x].create_line(panelWidth-w*2,panelHeight-h,panelWidth-w,panelHeight-w*2,width=4,fill='#EEEEEE',tags='main')
    objects[y][x][0] = 'g'

def laserSprite(x,y,**data):
    '''
    data:
    emitter (bool),
    dir (int)
    '''
    dir = data['dir']
    try:
        emitter = data['emitter']
    except KeyError:
        emitter = False
    glass = False
    if objects[y][x][0] == 'g': 
        glass = True
    if not emitter and not objects[y][x][0] == 'l': 
        panels[y][x].delete("main") #Don't delete the emitter sprite or the sprite of other lasers (if laser goes over itself)
        objects[y][x][0] = "l"
    if (dir in [0,2]):
        startX = panelWidth/2 - 0.5
        startY = 0
        endX = startX
        endY = panelHeight
        rot = panelWidth
        if (emitter):
            if dir == 0:
                endY = panelHeight/3 - 1
            else:
                startY = panelHeight/1.5 + 1

    elif (dir in [1,3]):
        startX = 0
        startY = panelHeight/2 - 0.5
        endX = panelWidth
        endY = startY
        rot = panelHeight #The dimension to use to determine the size of the laser
        if (emitter):
            if dir == 3:
                endX = panelWidth/3 - 1
            else:
                startX = panelWidth/1.5 + 1

    panels[y][x].create_line(startX,startY,endX,endY,width=rot//3,fill="#FF6A6A", tags="main")
    panels[y][x].create_line(startX,startY,endX,endY,width=rot/(64/13),fill="#d10202", tags="main")
    if glass:
        glassSprite(y,x,laser=True)


def emitterSprite(y,x,**data): 
    '''
    data:
    active (bool),
    dir (int),
    colour (string),
    fade (int)
    '''
    try:
        active = data['active']
    except KeyError:
        active = False
    try:
        colour = data['colour']
    except KeyError:
        colour = False
    try:
        fade = data['fade']
    except KeyError:
        fade = 0
    dir = data['dir'] #As with most things, 0 = up, 1 = right, 2 = down, and 3 = left

    w = panelWidth
    h = panelHeight
    panels[y][x].delete("main") 
    if fade == 0:
        if active:
            centerColour = "#d10202"
            outerColour = "#FF6A6A"
        else:
            centerColour = "#AFAFAF"
            outerColour = "#AFAFAF"
    else:
        if fade > 0: #Fade out
            centerRed = hex(207+(fade+1)*-3)[2:] #fade increases by one each animation frame
            centerGreen = hex(2+(fade+1)*20)[2:] #Convert it to base 16 and remove the first two characters (which are '0x')
            centerBlue = hex(2+(fade+1)*20)[2:]
            outerRed = hex(255+(fade+1)*-8)[2:]
            outerGreen = hex(107+(fade+1)*7)[2:]
            outerBlue = hex(107+(fade+1)*7)[2:]
            root.after(100, lambda: emitterSprite(y,x,dir=dir,colour=colour,fade=fade-1)) #Update again after 100 ms with fade one lower
        elif fade < 0: #Fade in
            fade = abs(fade)
            centerRed = hex(177+(fade+1)*3)[2:]
            centerGreen = hex(-38+(fade+1)*-20)[2:]
            centerBlue = hex(-38+(fade+1)*-20)[2:]
            outerRed = hex(175+(fade+1)*8)[2:]
            outerGreen = hex(177+(fade+1)*-7)[2:]
            outerBlue = hex(177+(fade+1)*-7)[2:]
            print(-38+(fade+1)*-20)
            print(hex(-38+(fade+1)*-20))
            if fade-1 == 0:
                print('g')
                laserMove(y,x,dir,True) #Activate the emitter with split true 
                emitterSprite(y,x,dir=dir,colour=colour,active=True) #Manually activate the emitter sprite because laserMove() with split set to true doesn't do it automatically\
            else:
                root.after(100, lambda: emitterSprite(y,x,dir=dir,colour=colour,fade=fade-1))

        # else:
        #     emitterSprite(y,x,active=active,dir=dir,colour=colour) #Start over using regular colour values
        #     return
        centerColour = "#" + str(centerRed) + str(centerGreen) + str(centerBlue) #Combine all three values into colour code
        outerColour = "#" + str(outerRed) + str(outerGreen) + str(outerBlue)


    if dir == 0: #Change location and angle variables based on direction of emitter
        coordsTip = w//2, h//3
        leftBase = w/(64/22), h
        rightBase = w/(w/42), h
        arcCenter = w//2, h//6+h//20
        circleAngle = 270
        angleOffsetStart = 0
        angleOffsetEnd = 2
    elif dir == 1:
        coordsTip = round(w/1.5), h//2
        leftBase = 0, h/(64/22)
        rightBase = 0, h/(64/42)
        arcCenter = w//1.2-w//20, h//2
        circleAngle = 180
        angleOffsetStart = 0 
        angleOffsetEnd = 2
    elif dir == 2:
        coordsTip = w//2, round(h/1.5) #Needs to be rounded up ('//' divides and floors)
        leftBase = w/(64/22), 0
        rightBase = w/(w/42), 0
        arcCenter = w//2, h//1.2-h//20
        circleAngle = 90
        angleOffsetStart = 2
        angleOffsetEnd = 0
    elif dir == 3:
        coordsTip = w//3, h//2
        leftBase = w, h/(64/22)
        rightBase = w, h/(64/42)
        arcCenter = w//6+w//20, h//2
        circleAngle = 0
        angleOffsetStart = 2
        angleOffsetEnd = 0

    if colour:
        ringColour = frameColours[colour]
    else:
        ringColour = "#AFAFAF"
    # panels[y][x].create_oval(0,panelHeight/2,panelWidth,panelHeight,outline="#b0b0b0",fill="#3e3e3e",width=6, tags="main")
    panels[y][x].create_polygon(*coordsTip, *leftBase, *rightBase, fill="#5E5E5E")
    panels[y][x].create_circle(*coordsTip, w//10,rY=h//10, fill=centerColour, outline='')
    panels[y][x].create_circle(*coordsTip, w//6,rY=h//6, outline=outerColour, fill='',width=3)
    panels[y][x].create_circle_arc(*arcCenter, w//2-w//20, rY=h//2-h//20, style='arc', outline=ringColour, fill='', width=3, start=circleAngle-14-angleOffsetStart, end=circleAngle+14+angleOffsetEnd)
    panels[y][x].create_circle_arc(*arcCenter, w//2+w//20, rY=h//2+h//20, style='arc', outline=ringColour, fill='', width=3, start=circleAngle-15-angleOffsetStart, end=circleAngle+15+angleOffsetEnd)
    panels[y][x].unbind("<Button-1>")
    if (active == True):
        laserSprite(x,y,dir=dir,emitter=True)
    objects[y][x][0] = "e"
    objects[y][x][1] = dir
    objects[y][x][2] = colour
    if colour == False:
        panels[y][x].bind("<Button-1>", lambda event: laserMove(y,x,dir))
    else:
        laserEmitters[colour] = [y,x,dir,active] #Store data in a variable that can be accessed to activate the reciever

def recieverSprite(y,x,**data): 
    '''
    data:
    laser (bool),
    dir (int),
    colour (string)
    '''
    try:
        laser = data['laser']
    except KeyError:
        laser = False
    dir = data['dir']
    colour = data['colour']
    #Note: Dir will be the direction of the incoming laser, so it will be inverted from the direction of the emitter
    laserRecievers[colour] = [y,x,dir,laser]
    panels[y][x].delete("main")
    try:
        outline = laserColours[colour]
    except KeyError:
        outline = "#FFFFFF" #If the colour is not yet set in the dictionary, use a placeholder
    oval = panels[y][x].create_oval(0,panelHeight/2,panelWidth,panelHeight,outline=outline,fill="#3e3e3e",width=6, tags="main")
    if (laser):
        laserSprite(x,y,dir=dir,emitter=True)
        panels[y][x].itemconfig(oval, fill="#f88080")
    objects[y][x][0] = 'r'
    objects[y][x][1] = dir
    objects[y][x][2] = colour
    

def doorSprite(y,x,**data):
    '''
    data:
    colour (string)
    '''
    colour = data['colour']

    global doors
    panels[y][x].delete('main')
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill="#F3C873", tags="main")
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,fill='',outline=frameColours[colour],width=8,tags='frame')
    doors.setdefault(colour,[]) #If this colour is not already in the doors dictionary, create a list inside it
    if (y,x) not in doors[colour]:
        doors[colour].append((y,x))
    # print(doors)
    objects[y][x][0] = 'd'
    objects[y][x][1] = colour
    objects[y][x][2] = 0

    
def laserMove(y,x,dir,split = False, first = False):
    if first or not split:
        for c, i in laserRecievers.items():
            recieverSprite(i[0],i[1],laser=False,dir=i[2],colour=c)
            # print(f"Resetting '{c}' laser")
            # if not i[3]: #If emitter is not active
            try: 
                laserEvents[c](True,c) #Run the event function in reverse mode to do things such as close doors when reciever is deactivated.
            except KeyError:
                print(f"WARNING: '{c}' reciever has no function set.")
    if not split: #Split is true if the laser has been split from a prism. This deletes lasers differently
        yLoop = 0
        xLoop = 0
        emitterSprite(y,x,active=True,dir=dir,colour=objects[y][x][2])
        global laserEmitters
        laserEmitters[False] = [y,x,dir,True]
        for l in objects: #Iterate over existing lasers to remove them
            for i in l:
                if i[0] == "l" or i[0] == 'g':
                    panels[yLoop][xLoop].delete("main")
                    if i[0] == 'g':
                        glass = True
                    else:
                        glass = False
                    objects[yLoop][xLoop] = ['','','']
                    if glass:
                        glassSprite(yLoop,xLoop)
                xLoop += 1
            xLoop = 0    
            yLoop += 1
        for i in laserFloors: #Reset glowing floors
            setPanel(i[0],i[1],'f')
            laserFloors.remove(i)
    while True: # 0 = up, 1 = right, 2 = down, 3 = left (this is the side of the box, the laser will have the oppisite number)
        if (dir == 0):
            y -= 1
        elif (dir == 1):
            x += 1
        elif (dir == 2):
            y += 1
        elif dir == 3:
            x -= 1
        try:
            if (x < 0 or y < 0):
                raise IndexError #Also raise indexerror if the coordinates go below zero
            elif (objects[y][x][0] in laserBlocks):
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
                if (objects[y][x][1] == dir and not frozen):
                    recieverSprite(y,x,laser=True,dir=dir,colour=objects[y][x][2])
                    # print(f"{objects[y][x][2]} reciever active")
                    try:
                        laserEvents[objects[y][x][2]](False,objects[y][x][2])
                    except KeyError:
                        print(f"ERROR: '{objects[y][x][2]}' reciever has no set function.")
                break
            elif (objects[y][x][0] == 'p'):
                if objects[y][x][1] == dir:
                    dir += 1
                    if dir > 3:
                        dir = 0
                    oldDir = dir
                    if not split:
                        laserMove(y,x,dir,True,True)
                    else:
                        laserMove(y,x,dir,True)
                    for i in range(2):
                        dir -= 1
                        if dir < 0:
                            dir = 3
                    laserMove(y,x,dir,True)
                    dir = oldDir
                    laserMove(y,x,dir,True)
                break
            else:
                laserSprite(x,y,dir=dir)
            #panels[y][x].create_text(panelWidth/2, panelHeight/2, text=dir) #Debug code to check the direction of lasers
        except IndexError:
            break #If it tries to check a panel outside the range, which means it has left the screen and should stop.
    

def objectMove(event, object):
    if frozen:
        return
    if event.keysym not in ['w','W','a','A','s','S','d','D','Up','Left','Down','Right']: #If the pressed key is not a directional key
        return
    global selectedObject
    if (len(selectedObject) == 0):
        selectedObject = object
    x = selectedObject[1]
    y = selectedObject[0]
    type = objects[y][x][0]
    dir = objects[y][x][1]
    panels[y][x].unbind("<Button-1>") #Unbind move select
    panels[y][x].delete("selected")
    if objects[y][x][2] not in ['','l']:
        setPanel(y,x,objects[y][x][2])
    else:
        panels[y][x].delete("main")
        objects[y][x] = ['','','']

    if (event.keysym in ['w','W','Up']):
        y -= 1
        if y < 0:
            y = 0
    elif event.keysym in ['a','A','Left']:
        x -= 1
        if x < 0:
            x = 0
    elif event.keysym in ['s','S','Down']:
        y += 1
        if y > 9:
            y = 9
    elif event.keysym in ['d','D','Right']:
        x += 1
        if x > 9:
            x = 9
    if objects[y][x][0] in boxBlocks: 
        y = selectedObject[0]
        x = selectedObject[1] #Revert movement, making functions below replace existing box that was removed above.
    objectSprites[type](y,x,flipped=dir,dir=dir)
    selectedObject = [y,x]
    panels[y][x].bind("<Button-1>", objectSelect)
    # panels[0][0].delete("all")
    # panels[0][0].create_text(32,32,text=[y,x],fill="white")
    if [y,x] in laserFloors:
        laserFloors.remove([y,x])
    if laserEmitters[False][3]:
        emitter = laserEmitters[False]
        laserMove(emitter[0],emitter[1],emitter[2])
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
    # print(f"object at {y},{x} selected")
    selectIndicator()

def selectIndicator():
    global selectedObject
    x = selectedObject[1]
    y = selectedObject[0]
    panels[y][x].delete('selected')
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight, outline="green", width=16, fill='', tags='selected') #Empty fill to make it only an outline
    panels[y][x].tag_raise('frame')
    
def selectAnimation(y,x):
    global selectLoopFrames
    #TODO: make animation for selected object frame
    

def laserEvent(**events):
    global laserEvents
    laserEvents = events


objectSprites = {
    'b': boxSprite,
    'p': prismSprite,
    'g': glassSprite,
    'l': laserSprite,
    'r': recieverSprite,
    'e': emitterSprite,
    'd': doorSprite
}

def emitterActivate(reverse,colour):
    '''Activate an emitter'''
    emitter = laserEmitters[colour]
    if not reverse and not emitter[3]:
        emitterSprite(emitter[0],emitter[1],dir=emitter[2],colour=colour,fade=-9) #Run the emitter function with the fade argument to make it start the animation
    elif emitter[3]:
        emitterSprite(emitter[0],emitter[1],dir=emitter[2],colour=colour,fade=9)
        #Laser is automatically removed if not updated every tick
# for i in objects:
#     print(i)



