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



def selectInit(selectedObject,movables):
    '''Automatically select a box and bind movement keys and mouse clicking to boxes'''
    objectSelect(0, movables[0])

    root.bind("<Key>",lambda event: objectMove(event, selectedObject))
    for i in movables:
        i.bind("<Button-1>", objectSelect)


    

# def doorRect(reverse,start,end): 
#     '''Open multiple doors'''
#     for y in range(start[0],end[0]+1):
#         for x in range(start[1],end[1]+1):
#             doorOpen(reverse,y,x)

def level0():
    '''Basic laser and mirror reflection intro.'''
    
    fillRect([3,2],[6,6],"f")
    fillRect([2,8],[6,8],'w')
    fillRect([1,2],[1,8],'w')
    # setPanel(2,5,'w')

    movables = []
    movables.append(mirrorSprite(2,7,flipped=False))

    emitterSprite(6,7,active=False,dir=0)
    recieverSprite(2,2,laser=False,dir=3,colour='red')


    # laserEvent(
    #     red = levelEnd
    #     #Put functions for different colours here
    #     #Use lambda for single expression functions
    # )
    
    selectInit((2,7),movables)


levels.append(level0)
# level0()

def level1():
    '''Moving mirrors intro.'''

    fillRect([5,3],[8,6],"f")
    fillRect([3,1],[8,1],"w")
    fillRect([3,8],[8,8],"w")
    fillRect([3,2],[3,7],"w")

    movables = []
    movables.append(mirrorSprite(4,7,flipped=False))
    movables.append(mirrorSprite(5,3,flipped=True))
    # boxes.append(boxSprite(6,5,False))
    # boxes.append(boxSprite(6,6,True))

    emitterSprite(8,7,active=False,dir=0)
    recieverSprite(8,2,laser=False,dir=2,colour='red')

    # laserEvent(
    #     red = levelEnd
    #     #Put functions for different colours here
    # )
    selectInit((5,3),movables)

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

    movables = []
    movables.append(mirrorSprite(3,4,flipped=False))
    movables.append(mirrorSprite(8,1,flipped=True))

    emitterSprite(4,8,active=False,dir=3)
    recieverSprite(1,8,laser=False,dir=1,colour='red')
    recieverSprite(0,3,laser=False,dir=0,colour='green')

    # laserEvent(
    #     green = doorOpen,
    #     red = levelEnd #TODO: Make red reciever always the reciever for winning
    #     #Put functions for different colours here
    # )


    selectInit((3,4),movables)
levels.append(level2)


def level3():
    '''Glass intro'''
    fillRect([0,0],[9,9],'w')
    fillRect([1,1],[8,9],'')
    fillRect([1,5],[8,5],'g')
    fillRect([1,6],[3,7],'f')
    fillRect([1,8],[8,8],'g')


    fillRect([4,1],[4,4],'d',colour='red')

    movables = []
    movables.append(mirrorSprite(4,7,flipped=False))
    movables.append(mirrorSprite(5,1,flipped=True))
    movables.append(mirrorSprite(3,2,flipped=False))
    movables.append(mirrorSprite(7,9,flipped=True))

    emitterSprite(8,7,dir=0)
    recieverSprite(8,2,laser=False,dir=2,colour='red')
    recieverSprite(1,9,laser=False,dir=0,colour="green")

    # laserEvent(
    #    red = doorOpen,
    #    green = levelEnd  
    # )

    selectInit((5,9),movables)

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
    
    movables = []
    movables.append(prismSprite(1,2,dir=0))
    movables.append(mirrorSprite(1,1,flipped=False))
    movables.append(mirrorSprite(7,3,flipped=True))
    movables.append(mirrorSprite(1,6,flipped=False)) #TODO: make it more clear that boxes keep doors open
    emitterSprite(9,5,active=False,dir=0)
    recieverSprite(0,3,laser=False,dir=0,colour='green')
    recieverSprite(6,9,laser=False,dir=1,colour='red')
    recieverSprite(1,5,laser=False,dir=3,colour='blue')

    # doorOpeners = dict.fromkeys(('red','green'), doorOpen)
    # laserEvent(
    #     **doorOpeners,
    #     blue = levelEnd
    # )


    selectInit((7,3),movables)
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


    movables = []
    movables.append(prismSprite(6,6,dir=3))
    movables.append(mirrorSprite(1,7,flipped=True))
    movables.append(prismSprite(1,4,dir=0))
    movables.append(mirrorSprite(7,4,flipped=False))
    movables.append(prismSprite(1,0,dir=3))
    emitterSprite(5,9,active=False,dir=3)
    recieverSprite(1,8,laser=False,dir=1,colour='green')
    recieverSprite(9,7,laser=False,dir=2,colour='blue')
    recieverSprite(0,3,laser=False,dir=0,colour='yellow')
    recieverSprite(1,1,laser=False,dir=3,colour='purple')
    recieverSprite(9,3,laser=False,dir=2,colour='orange')
    recieverSprite(7,9,laser=False,dir=1,colour='red')

    # doorOpeners = dict.fromkeys(('green','blue','yellow','purple','orange'), doorOpen)
    # laserEvent(
    #     **doorOpeners,
    #     red = levelEnd
    # )

    #TODO: Split laser doesn't move through door opened on the same frame
    #TODO: Change door functions to allow colour to be set when door created, automatically setting up recievers.

    selectInit((6,6),movables)
levels.append(level5)


def level6():
    '''Colour-activated emitter intro'''
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

    # emitterActivators = dict.fromkeys(('green','blue','yellow','purple'), emitterActivate)
    # laserEvent(
    #     **emitterActivators,
    #     red = levelEnd
    # )


def level7():
    fillRect((5,0),(9,3),'f') #Fill all panels in the bottom half with floors and leave empty gaps only where lasers go to make the level less confusing and intimidating.
    setPanel(5,2,'')
    fillRect((0,0),(0,8),'w')
    fillRect((4,0),(4,9),'w')
    fillRect((5,5),(6,5),'f')
    fillRect((7,5),(9,7),'f')
    fillRect((6,3),(8,3),'w')
    setPanel(8,4,'g')
    setPanel(4,4,'g')
    setPanel(6,4,'g')
    fillRect((6,1),(8,3),'w')
    setPanel(6,2,'g')
    setPanel(7,3,'g')
    setPanel(7,2,'')
    setPanel(4,2,'g')
    setPanel(4,6,'g')
    setPanel(4,8,'g')
    fillRect((5,5),(6,7),'w')
    setPanel(5,7,'g')  
    fillRect((5,9),(9,9),'f')
    
    # boxSpawnerSprite(5,8)
    # boxSpawnerSprite(6,8,open=True)

    movables = []
    movables.append(boxSpawnerSprite(0,9,colour='green'))
    movables.append(boxSpawnerSprite(3,0,colour='blue'))
    movables.append(mirrorSprite(7,2,flipped=False))
    movables.append(mirrorSprite(8,5,flipped=False))
    movables.append(mirrorSprite(5,6,flipped=False))



    # boxSprite(3,0,stage=0)
    # boxSprite(2,1,stage=1)
    # boxSprite(3,2,stage=2)
    # boxSprite(2,3,stage=3)
    # boxSprite(3,4,stage=4)
    emitterSprite(9,4,dir=0)
    recieverSprite(0,2,colour='blue',dir=0)
    recieverSprite(0,4,colour='green',dir=0)
    boxButtonSprite(0,0,colour='yellow')
    boxButtonSprite(5,9,colour='red')
    recieverSprite(0,8,dir=0,colour='purple')
    emitterSprite(9,8,dir=0,colour='yellow')
    setPanel(1,2,'d',colour='yellow')
    setPanel(1,4,'d',colour='purple',reverse=True,open=True)
    setPanel(1,0,'d',colour='yellow',reverse=True,open=True)
    setPanel(4,9,'d',colour='purple')

    selectInit((0,9),movables)
    def yellow(reverse,colour):
        doorOpen(reverse,colour)
        emitterActivate(reverse,colour)

    # laserEvent(
    #     blue = boxSpawnerActivate,
    #     green = boxSpawnerActivate,
    #     yellow = yellow
    # )

def level8():
    
    movables = []
    movables.append(boxSpawnerSprite(5,7))
    movables.append(boxSpawnerSprite(4,7,colour='red'))

    emitterSprite(8,8,dir=0)
    emitterSprite(8,9,dir=0,colour='red')
    boxButtonSprite(5,4,colour='red')

    selectInit((5,7),movables)

    # laserEvent(red = emitterActivate)
    


def levelEditor():
    for y in range(10):
        for x in range(10):
            panels[y][x].create_rectangle(0,0,panelWidth-1,panelHeight-1,outline='white',width=1) #Create a border around each panel to highlight the grid objects can be created in.
    text = Label(root,text='Level Editor',fg='white',bg='black',font=('Arial',20,'bold'))
    subtext = Label(root,text='Select objects to add to level.',fg='white',bg='black',font=('Arial',14))
    text.grid(row=0,column=10,columnspan=3,sticky='nsew')
    subtext.grid(row=1,column=10,columnspan=3,sticky='nsew')
    selectableObjects = []
    fakeObjectSprites = {
        'w': lambda panel,dir,flipped,noborder: setPanelFake(panel,'w'), 
        'f': lambda panel,dir,flipped,noborder: setPanelFake(panel,'f'),
        'g': glassSpriteFake,
        'e': emitterSpriteFake,
        'r': recieverSpriteFake,
        'm': mirrorSpriteFake,
        'p': prismSpriteFake,
        'd': doorSpriteFake,
        's': boxSpawnerSpriteFake,
        'n': boxButtonSpriteFake
    }
    global objectData
    objectData = {}
    for n,sprite,i in zip(fakeObjectSprites, fakeObjectSprites.values(), range(10)):
        panel = Canvas(root,width=48,height=48,bg='black',highlightthickness=0,bd=0)
        if i < 3:
            panel.grid(row=i+2,column=10)
        elif i < 7:
            panel.grid(row=i-1,column=11)
        else:
            panel.grid(row=i-5,column=12)
        root.update_idletasks() #Update info so canvas width and height are accurate.
        sprite(panel,dir=0,flipped=False,noborder=True)
        selectableObjects.append(panel)
        panel.bind("<Button-1>",lambda event: selectObject(panel,n))
    rotate = Canvas(root,width=48,height=48,bg='black',highlightthickness=0,bd=0)
    delete = Canvas(root,width=48,height=48,bg='black',highlightthickness=0,bd=0)
    rect = Canvas(root,width=48,height=48,bg='black',highlightthickness=0,bd=0)
    rotate.grid(row=6,column=10,rowspan=2)
    delete.grid(row=6,column=11,rowspan=2)
    rect.grid(row=6,column=12,rowspan=2)

    root.update_idletasks()
    rotateSprite(rotate)
    deleteSprite(delete)
    rectSprite(rect)

    colours = {False: "#4E4E4E"} #A dictioanry of colour codes with one for a default colour
    colours.update(laserColours.items())

    colourFrame = Frame(root, bg='black', borderwidth=0)
    colourFrame.grid(row=8,column=10,columnspan=3)
    colourButtons = {}
    for n, c, i in zip(colours, colours.values(), range(len(laserColours))):
        panel = Canvas(colourFrame,width=36,height=36,bg='black',highlightthickness=0,bd=0)
        panel.grid(row=0,column=i,padx=2)
        root.update_idletasks()
        w = panel.winfo_width()
        h = panel.winfo_height()
        circle = panel.create_oval(2,2,w-2,h-2,fill=c,outline="#9a9a9a",width=4) #2 off the edges to fit the full circle and outline in the canvas.
        panel.bind("<Button-1>",lambda event: selectColour(n))
        colourButtons[n] = [panel,circle]


    def selectObject(panel,object):
        global objectData
        try:
            #Reset the previously selected panel and clear the objectData dictionary
            objectData['panel'].delete('selected')
            fakeObjectSprites[objectData['object']](objectData['panel'],dir=0,flipped=False,noborder=True)
        except KeyError:
            pass #Continue if there is no panel previously selected
        objectData = {}
        selectIndicator(panel)
        objectData['object'] = object
        objectData['panel'] = panel
        objectData['dir'] = 0
        objectData['flipped'] = False
        if object in ['e','s']: #Objects with default colours
            objectData['colour'] = False
        else: #Objects that need a colour
            objectData['colour'] = 'red'
        objectData['reverse'] = False
    
    def rotateObject():
        try:
            objectData['panel']
        except KeyError:
            return #Don't run if an object hasn't been selected yet.
        if objectData['object'] == 'm':
            objectData['flipped'] = not objectData['flipped'] 
        elif objectData['object'] == 'd':
            objectData['reverse'] = not objectData['reverse'] #Change whether the door is open or closed when unpowered
        else:
            dir = objectData['dir']
            dir += 1
            if dir > 3:
                dir = 0
            objectData['dir'] = dir
        fakeObjectSprites[objectData['object']](objectData['panel'],dir=objectData['dir'],flipped=objectData['flipped'],reverse=objectData['reverse'])

    def selectColour(colour):
        try:
            objectData['panel']
        except KeyError:
            return #Don't run if an object hasn't been selected yet.
        if colour == False and objectData['object'] not in ['e','s']:
            colour = 'red' #If the colour is false but the object can't have a default colour, set the colour to red.
            #TODO: Make default colour disappear when an object that requires a colour is selected.
        try: #Remove the green outline from the previous colour if it exists.
            colourButtons[colour][0].itemconfigure(colourButtons[colour][1],outline="#9a9a9a")
        except KeyError:
            pass
        objectData['colour'] = colour
        fakeObjectSprites[objectData['object']](objectData['panel'],colour=objectData['colour'])
        
        colourButtons[colour][0].itemconfigure(colourButtons[colour][1],outline="#6cca41")



        
        

levelEditor()


root.mainloop() #Ensure all functions are defined before this is run.
