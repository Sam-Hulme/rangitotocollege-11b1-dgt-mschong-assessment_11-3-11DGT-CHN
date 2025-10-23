'''The actual level design that imports and calls functions from the laser file.'''
import tkinter
from tkinter import *
from laser import *
import laser
from core import *
import sys
import os
import ast
import copy


def selectInit(selectedObject, movables):
    '''Automatically select a box and bind movement keys and mouse clicking to boxes'''
    for i in movables:
        y = i.grid_info()['row']
        x = i.grid_info()['column']
        if [y, x] == selectedObject:
            # Check which object in the objects list should start selected
            selectedPanel = i
            break
    objectSelect(0, selectedPanel)
    laser.selectedObject = selectedObject
    root.bind("<Key>", lambda event: objectMove(event, selectedObject))
    for i in movables:
        i.bind("<Button-1>", objectSelect)


# def doorRect(reverse,start,end):
#     '''Open multiple doors'''
#     for y in range(start[0],end[0]+1):
#         for x in range(start[1],end[1]+1):
#             doorOpen(reverse,y,x)

def level0():
    '''Basic laser and mirror reflection intro.'''

    fillRect([3, 2], [6, 6], "f")
    fillRect([2, 8], [6, 8], 'w')
    fillRect([1, 2], [1, 8], 'w')
    # setPanel(2,5,'w')

    movables = []
    movables.append(mirrorSprite(2, 7, flipped=False))

    emitterSprite(6, 7, active=False, dir=0)
    recieverSprite(2, 2, laser=False, dir=3, colour='end')

    # laserEvent(
    #     red = levelEnd
    #     #Put functions for different colours here
    #     #Use lambda for single expression functions
    # )

    selectInit([2, 7], movables)


levels.append(level0)
# level0()


def level1():
    '''Moving mirrors intro.'''

    fillRect([5, 3], [8, 6], "f")
    fillRect([3, 1], [8, 1], "w")
    fillRect([3, 8], [8, 8], "w")
    fillRect([3, 2], [3, 7], "w")

    movables = []
    movables.append(mirrorSprite(4, 7, flipped=False))
    movables.append(mirrorSprite(5, 3, flipped=True))
    # boxes.append(boxSprite(6,5,False))
    # boxes.append(boxSprite(6,6,True))

    emitterSprite(8, 7, active=False, dir=0)
    recieverSprite(8, 2, laser=False, dir=2, colour='end')

    # laserEvent(
    #     red = levelEnd
    #     #Put functions for different colours here
    # )
    selectInit([5, 3], movables)


levels.append(level1)


def level2():
    '''Doors intro'''
    fillRect([5, 2], [5, 8], "w")
    fillRect([2, 5], [3, 8], "f")
    fillRect([0, 9], [8, 9], "w")
    fillRect([0, 0], [9, 0], "w")
    fillRect([0, 1], [0, 8], 'w')
    fillRect([9, 1], [9, 9], "w")
    fillRect([6, 1], [8, 8], 'f')

    setPanel(5, 1, 'd', colour='red')

    movables = []
    movables.append(mirrorSprite(3, 4, flipped=False))
    movables.append(mirrorSprite(8, 1, flipped=True))

    emitterSprite(4, 8, active=False, dir=3)
    recieverSprite(1, 8, laser=False, dir=1, colour='end')
    recieverSprite(0, 3, laser=False, dir=0, colour='red')

    # laserEvent(
    #     green = doorOpen,
    #     red = levelEnd #TODO: Make red reciever always the reciever for winning
    #     #Put functions for different colours here
    # )

    selectInit([3, 4], movables)


levels.append(level2)


def level3():
    '''Glass intro'''
    fillRect([0, 0], [9, 9], 'w')
    fillRect([1, 1], [8, 9], '')
    fillRect([1, 5], [8, 5], 'g')
    fillRect([1, 6], [3, 7], 'f')
    fillRect([1, 8], [8, 8], 'g')

    fillRect([4, 1], [4, 4], 'd', colour='red')

    movables = []
    movables.append(mirrorSprite(4, 7, flipped=False))
    movables.append(mirrorSprite(5, 1, flipped=True))
    movables.append(mirrorSprite(3, 2, flipped=False))
    movables.append(mirrorSprite(7, 9, flipped=True))

    emitterSprite(8, 7, dir=0)
    recieverSprite(8, 2, laser=False, dir=2, colour='red')
    recieverSprite(1, 9, laser=False, dir=0, colour="end")

    # laserEvent(
    #    red = doorOpen,
    #    green = levelEnd
    # )

    selectInit([4, 7], movables)


levels.append(level3)


def level4():
    '''Prism intro'''
    fillRect([0, 0], [9, 9], 'w')
    fillRect([1, 1], [8, 8], '')
    fillRect([2, 1], [2, 2], 'w')
    fillRect([1, 4], [2, 4], 'w')
    fillRect([2, 5], [2, 7], 'w')
    fillRect([3, 1], [8, 1], 'f')
    fillRect([3, 5], [5, 5], 'w')
    glassSprite(2, 8)

    setPanel(2, 3, 'd', colour='green')
    setPanel(1, 8, 'd', colour='red')

    movables = []
    movables.append(prismSprite(1, 2, dir=0))
    movables.append(mirrorSprite(1, 1, flipped=False))
    movables.append(mirrorSprite(7, 3, flipped=True))
    # TODO: make it more clear that boxes keep doors open
    movables.append(mirrorSprite(1, 6, flipped=False))
    emitterSprite(9, 5, active=False, dir=0)
    recieverSprite(0, 3, laser=False, dir=0, colour='red')
    recieverSprite(6, 9, laser=False, dir=1, colour='green')
    recieverSprite(1, 5, laser=False, dir=3, colour='end')

    # doorOpeners = dict.fromkeys(('red','green'), doorOpen)
    # laserEvent(
    #     **doorOpeners,
    #     blue = levelEnd
    # )

    selectInit([7, 3], movables)


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
    fillRect([0, 0], [9, 9], 'w')
    fillRect([1, 1], [8, 8], '')
    fillRect([7, 5], [8, 5], 'w')
    fillRect([4, 1], [8, 1], 'f')
    setPanel(3, 5, 'w')
    setPanel(1, 0, '')

    fillRect([1, 5], [2, 5], 'd', colour='green')
    fillRect([3, 6], [3, 8], 'd', colour='blue')
    fillRect([3, 1], [3, 4], 'd', colour='yellow')
    setPanel(2, 0, 'd', colour='purple')
    fillRect([4, 5], [6, 5], 'd', colour='orange')

    movables = []
    movables.append(prismSprite(6, 6, dir=3))
    movables.append(mirrorSprite(1, 7, flipped=True))
    movables.append(prismSprite(1, 4, dir=0))
    movables.append(mirrorSprite(7, 4, flipped=False))
    movables.append(prismSprite(1, 0, dir=3))
    emitterSprite(5, 9, active=False, dir=3)
    recieverSprite(1, 8, laser=False, dir=1, colour='green')
    recieverSprite(9, 7, laser=False, dir=2, colour='blue')
    recieverSprite(0, 3, laser=False, dir=0, colour='yellow')
    recieverSprite(1, 1, laser=False, dir=3, colour='purple')
    recieverSprite(9, 3, laser=False, dir=2, colour='orange')
    recieverSprite(7, 9, laser=False, dir=1, colour='end')

    # doorOpeners = dict.fromkeys(('green','blue','yellow','purple','orange'), doorOpen)
    # laserEvent(
    #     **doorOpeners,
    #     red = levelEnd
    # )

    # TODO: Split laser doesn't move through door opened on the same frame
    # TODO: Change door functions to allow colour to be set when door created, automatically setting up recievers.

    selectInit([6, 6], movables)


levels.append(level5)


def level6():
    '''Colour-activated emitter intro'''
    fillRect((4, 5), (9, 5), 'w')
    setPanel(5, 5, 'g')
    fillRect((3, 0), (3, 9), 'w')
    setPanel(3, 8, 'g')

    emitterSprite(9, 7, dir=0)
    emitterSprite(5, 9, dir=3, colour='green')
    emitterSprite(9, 2, dir=0, colour='blue')
    emitterSprite(1, 0, dir=1, colour='yellow')
    emitterSprite(0, 8, dir=2, colour='purple')

    recieverSprite(4, 7, dir=0, colour='green')
    recieverSprite(5, 0, dir=3, colour='blue')
    recieverSprite(4, 2, dir=0, colour='yellow')
    recieverSprite(1, 9, dir=1, colour='purple')
    recieverSprite(9, 8, dir=2, colour='end')

    # emitterActivators = dict.fromkeys(('green','blue','yellow','purple'), emitterActivate)
    # laserEvent(
    #     **emitterActivators,
    #     red = levelEnd
    # )
levels.append(level6)

def level7():
    # Fill all panels in the bottom half with floors and leave empty gaps only where lasers go to make the level less confusing and intimidating.
    fillRect((5, 0), (9, 3), 'f')
    setPanel(5, 2, '')
    fillRect((0, 0), (0, 8), 'w')
    fillRect((4, 0), (4, 9), 'w')
    fillRect((5, 5), (6, 5), 'f')
    fillRect((7, 5), (9, 7), 'f')
    fillRect((6, 3), (8, 3), 'w')
    setPanel(8, 4, 'g')
    setPanel(4, 4, 'g')
    setPanel(6, 4, 'g')
    fillRect((6, 1), (8, 3), 'w')
    setPanel(6, 2, 'g')
    setPanel(7, 3, 'g')
    setPanel(7, 2, '')
    setPanel(4, 2, 'g')
    setPanel(4, 6, 'g')
    setPanel(4, 8, 'g')
    fillRect((5, 5), (6, 7), 'w')
    setPanel(5, 7, 'g')
    fillRect((5, 9), (9, 9), 'f')

    # boxSpawnerSprite(5,8)
    # boxSpawnerSprite(6,8,open=True)

    movables = []
    movables.append(boxSpawnerSprite(0, 9, colour='green'))
    movables.append(boxSpawnerSprite(3, 0, colour='blue'))
    movables.append(mirrorSprite(7, 2, flipped=False))
    movables.append(mirrorSprite(8, 5, flipped=False))
    movables.append(mirrorSprite(5, 6, flipped=False))

    # boxSprite(3,0,stage=0)
    # boxSprite(2,1,stage=1)
    # boxSprite(3,2,stage=2)
    # boxSprite(2,3,stage=3)
    # boxSprite(3,4,stage=4)
    emitterSprite(9, 4, dir=0)
    recieverSprite(0, 2, colour='blue', dir=0)
    recieverSprite(0, 4, colour='green', dir=0)
    boxButtonSprite(0, 0, colour='yellow')
    boxButtonSprite(5, 9, colour='end')
    recieverSprite(0, 8, dir=0, colour='purple')
    emitterSprite(9, 8, dir=0, colour='yellow')
    setPanel(1, 2, 'd', colour='yellow')
    setPanel(1, 4, 'd', colour='purple', reverse=True, open=True)
    setPanel(1, 0, 'd', colour='yellow', reverse=True, open=True)
    setPanel(4, 9, 'd', colour='purple')

    selectInit([0, 9], movables)

    # def yellow(reverse, colour):
    #     doorOpen(reverse, colour)
    #     emitterActivate(reverse, colour)
levels.append(level7)
    # laserEvent(
    #     blue = boxSpawnerActivate,
    #     green = boxSpawnerActivate,
    #     yellow = yellow
    # )

def level8():

    movables = []
    movables.append(boxSpawnerSprite(5, 7))
    movables.append(boxSpawnerSprite(4, 7, colour='red'))

    emitterSprite(8, 8, dir=0)
    emitterSprite(8, 9, dir=0, colour='red')
    boxButtonSprite(5, 4, colour='red')

    selectInit([5, 7], movables)

    # laserEvent(red = emitterActivate)


def levelEditor():
    try:
        root.after_cancel(laser.runEndEvent) 
        # Cancel the event from running this again
    except ValueError:
        pass
    global exitButton
    try:
        exitButton.destroy()
    except NameError:
        pass
    global editorLevelTemp
    global selectedObjectTemp
    global selectedObject
    global revealSelected
    revealSelected = ''
    def selectIndicatorFlash(panel, draw):
        """Flash the selection indicator on and off for the selected panel."""
        global selectedObject
        if selectedObject == []:
            return
        panel = panels[selectedObject[0]][selectedObject[1]]
        if draw:
            selectIndicator(False, selectedObject, ignoreSpawners=False)
            panel.tag_raise('selected')
        else:
            panel.delete('selected')

        panel.after(800, lambda: selectIndicatorFlash(panel, not draw)) 
        # Run the function again after 800ms with draw inverted.

    if editorLevelTemp:
        # If a temporary level exists
        createLevel(editorLevelTemp, selectedObjectTemp, fake=True)
        selectedObject = selectedObjectTemp
        if selectedObject != []:
            selectIndicatorFlash(panels[selectedObject[0]][selectedObject[1]], True)            
    laser.endEvent = levelEditor
    for y in range(10):
        for x in range(10):
            # Create a border around each panel to highlight the grid objects can be created in.
            panels[y][x].create_rectangle(
                0, 0, panelWidth-1, panelHeight-1, outline='white', width=1, tags='highlight')
    titleFrame = Frame(root, bg='black', borderwidth=0)
    text = Label(titleFrame, text='Level Editor', fg='white',
                 bg='black', font=('Arial', 20, 'bold'))
    subtext = Label(titleFrame, text='Select objects to add to level.',
                    fg='white', bg='black', font=('Arial', 13))
    selectionNote = Label(root, text='Right click movable object\nto make it start selected.',
                    fg='white', bg='black', font=('Arial', 14, 'bold'))
    titleFrame.grid(row=0, column=10, columnspan=3)
    text.grid(row=0, column=0, sticky='nsew')
    subtext.grid(row=1, column=0, sticky='nsew')
    selectionNote.grid(row=1, column=10, columnspan=3, sticky='nsew')
    selectableObjects = []
    global objectData
    objectData = {}

    for o, sprite, i in zip(fakeObjectSprites, fakeObjectSprites.values(), range(10)):
        panel = Canvas(root, width=48, height=48, bg='black',
                       highlightthickness=0, bd=0)
        if i < 3:
            panel.grid(row=i+2, column=10)
        elif i < 7:
            panel.grid(row=i-1, column=11)
        else:
            panel.grid(row=i-5, column=12)
        # Update info so canvas width and height are accurate.
        root.update_idletasks()
        if o == 'r':
            dir = 2 # Reciever is upside down to start.
        else:
            dir = 0
        sprite(panel, dir=dir, flipped=False, noborder=True)
        selectableObjects.append(panel)
        # Current has to be used because otherwise there is a bug where it always uses the last value of the loop for every object
        panel.bind("<Button-1>", lambda event, currentPanel=panel,
                   currentObj=o: selectObject(currentPanel, currentObj))
    
    dataButtons = Frame(root, bg='black', borderwidth=0)
    dataButtons.grid(row=6, column=10, columnspan=3, rowspan=3)
    rotate = Canvas(dataButtons, width=48, height=48, bg='black',
                    highlightthickness=0, bd=0)
    delete = Canvas(dataButtons, width=48, height=48, bg='black',
                    highlightthickness=0, bd=0)
    rect = Canvas(dataButtons, width=48, height=48, bg='black',
                  highlightthickness=0, bd=0)
    rotate.grid(row=0, column=0, pady=25, padx=10)
    delete.grid(row=0, column=1, pady=25, padx=10)
    rect.grid(row=0, column=2, pady=25, padx=10)

    root.update_idletasks()
    rotateSprite(rotate)
    deleteSprite(delete)
    rectSprite(rect)

    # A dictioanry of colour codes with one for a default colour
    colours = {False: "#4E4E4E"}
    colours.update(laserColours.items())

    colourFrame = Frame(dataButtons, bg='black', borderwidth=0)
    colourFrame.grid(row=1, column=0, columnspan=3)
    colourButtons = {}

    for n, c, i in zip(colours, colours.values(), range(len(laserColours))):
        panel = Canvas(colourFrame, width=36, height=36,
                       bg='black', highlightthickness=0, bd=0)
        if n == False:
            rowspan = 2
            column = 0
        else:
            rowspan = 1
            column = i-((i-1)//3*3)+1
        panel.grid(row=i//4, column=column, padx=2, pady=2, rowspan=rowspan)
        root.update_idletasks()
        w = panel.winfo_width()
        h = panel.winfo_height()
        # 2 off the edges to fit the full circle and outline in the canvas.
        circle = panel.create_oval(
            2, 2, w-2, h-2, fill=c, outline="#9a9a9a", width=4)
        panel.bind("<Button-1>", lambda event,
                   current=n: selectColour(current))
        colourButtons[n] = [panel, circle]


    def selectObject(panel, object):
        global objectData
        try:
            # Reset the previously selected panel and clear the objectData dictionary
            objectData['panel'].delete('selected')
            if objectData['object'] == 'r':
                dir = 2
            else:
                dir = 0
            fakeObjectSprites[objectData['object']](
                objectData['panel'], dir=dir, flipped=False, noborder=True)
            if objectData['colour'] == 'end':
                objectData['colour'] = False
            colourButtons[objectData['colour']][0].itemconfigure(
                colourButtons[objectData['colour']][1], outline="#9a9a9a")
            try:
                objectData['panel'].after_cancel(objectData['after_id'])
                # Cancel previous delay
            except ValueError:
                pass
            except KeyError:
                pass
        except KeyError:
            pass  # Continue if there is no panel previously selected
        delete.delete('selected')
        objectData = {}
        selectIndicator(panel)
        objectData['object'] = object
        objectData['panel'] = panel
        if object == 'r':
            objectData['dir'] = 2
        else:
            objectData['dir'] = 0
        objectData['flipped'] = False

        if object in ['r', 'n']:  # Objects that need a colour
            objectData['colour'] = 'end'
        elif object == 'd':
            objectData['colour'] = 'red'
        else: # Objects with default colours
            objectData['colour'] = False

        if object in ['r', 'n', 's', 'e']:
            colourButtons[False][0].itemconfig(colourButtons[False][1], outline="#6cca41") 
            # Show that the default colour is selected
        elif object == 'd':
            colourButtons['red'][0].itemconfig(colourButtons['red'][1], outline="#6cca41") 
            # Red is the default for doors.

        if object in ['r', 'n']:
            colourButtons[False][0].itemconfig(colourButtons[False][1], fill="#e2acb4")
            # Change the default colour button to the end colour
        else:
            colourButtons[False][0].itemconfig(colourButtons[False][1], fill="#4E4E4E")
            # Revert it if a different object is selected.
        objectData['reverse'] = False

    def rotateObject(event):
        try:
            objectData['panel']
        except KeyError:
            return  # Don't run if an object hasn't been selected yet.
        try:
            objectData['panel'].after_cancel(objectData['after_id'])
            # Cancel previous delay
        except ValueError:
            pass
        except KeyError:
            pass
        if objectData['object'] == 'm':
            objectData['flipped'] = not objectData['flipped']
        elif objectData['object'] == 'd':
            # Change whether the door is open or closed when unpowered
            objectData['reverse'] = not objectData['reverse']
        else:
            dir = objectData['dir']
            dir += 1
            if dir > 3:
                dir = 0
            objectData['dir'] = dir
        fakeObjectSprites[objectData['object']](objectData['panel'], dir=objectData['dir'],
                                                flipped=objectData['flipped'], reverse=objectData['reverse'], colour=objectData['colour'])
        
        objectData['after_id'] = objectData['panel'].after(
            2000, lambda panel=objectData['panel']: panel.tag_raise('selected'))
    rotate.bind("<Button-1>", rotateObject)

    def selectColour(colour):
        try:
            objectData['panel']
        except KeyError:
            return  # Don't run if an object hasn't been selected yet.
        try:
            objectData['panel'].after_cancel(objectData['after_id'])
            # Cancel previous delay
        except ValueError:
            pass
        except KeyError:
            pass
        if colour == False and objectData['object'] in ['r', 'n']:
            colour = 'end'
        if colour == False and objectData['object'] == 'd':
            # Doors must have a colour and don't activate colours, use red as a default.
            colour = 'red'
        try:  # Remove the green outline from the previous colour if it exists.
            if objectData['colour'] == 'end':
                objectData['colour'] = False 
                # Set object data colour to false because end is not a colour in the colourButtons dictionary.
            colourButtons[objectData['colour']][0].itemconfigure(
                colourButtons[objectData['colour']][1], outline="#9a9a9a")
        except KeyError:
            pass
        objectData['colour'] = colour

        fakeObjectSprites[objectData['object']](
            objectData['panel'], colour=objectData['colour'], dir=objectData['dir'], flipped=objectData['flipped'])
        
        if colour == 'end':
            colour = False
        colourButtons[colour][0].itemconfigure(
            colourButtons[colour][1], outline="#6cca41")

        objectData['after_id'] = objectData['panel'].after(
            2000, lambda panel=objectData['panel']: panel.tag_raise('selected'))

    def selectDelete(event):
        global objectData
        try:
            # Reset the previously selected panel and clear the objectData dictionary
            objectData['panel'].delete('selected')
            fakeObjectSprites[objectData['object']](
                objectData['panel'], dir=0, flipped=False, noborder=True)
            colourButtons[objectData['colour']][0].itemconfigure(
                colourButtons[objectData['colour']][1], outline="#9a9a9a")
        except KeyError:
            pass
        try:
            objectData['panel'].after_cancel(objectData['after_id'])
            # Cancel the event that adds the selection frame back
        except KeyError:
            pass
        objectData = {}
        objectData['object'] = ''
        selectIndicator(delete)
    delete.bind('<Button-1>', selectDelete)
    
    def highlightPanel(panel):
        try:
            # Check if an object (or the delete button) has been selected
            objectData['object']
        except KeyError:
            return

        if objectData['object'] == '':
            colour = "#DB3939"
        else:
            colour = "#60e8f7"
        
        panel.itemconfig('highlight', outline=colour, width=3)
    

    def build(panel):
        global objectData
        try:
            # Check if an object (or the delete button) has been selected
            objectData['object']
        except KeyError:
            return
        
        global selectedObject
        y = panel.grid_info()['row']
        x = panel.grid_info()['column']
        def changeDefaultSelected(y, x):
                global selectedObject
                panels[selectedObject[0]][selectedObject[1]].delete('selected') # Remove the selection indicator from the previously selected object
                selectedObject = [y,x]

        if objectData['object'] in movableObjects or objectData['object'] == 's':
            if selectedObject == []: 
                # Set the selectedObject variable and start the flashing function if this is the first movable placed
                selectedObject = [y,x]
                selectIndicatorFlash(panel, True)
                # Flashing function will automatically change based on the selectedObject variable
            panels[y][x].bind("<Button-3>", lambda event, y=y, x=x: changeDefaultSelected(y, x))
        else:
            panels[y][x].unbind("<Button-3>")

        try:
            objectPanel = objectData.pop('panel')
        except KeyError:
            pass
        # Remove the panel item from objectData to prevent issues with the setPanel function

        if objectData['object'] in ['s','e']:
            # Remove another spawner/emitter of this colour because only one can exist for each colour.
            for sY in range(10):
                for sX in range(10):
                    if objects[sY][sX][0] == 's' and objects[sY][sX][2] == objectData['colour']:
                        panels[sY][sX].delete('main')
                        panels[sY][sX].delete('frame')
                        objects[sY][sX] = ['','','']
                        if selectedObject == [sY,sX]:
                            # If the old spawner was selected, select the new one.
                            panels[sY][sX].delete('selected')
                            selectedObject = [y,x]
        setPanelFake(panel, type=objectData['object'], setData=True, **objectData)
        try:
            objectData['panel'] = objectPanel
        except UnboundLocalError:
            pass
        
        if selectedObject == [y,x] and not objectData['object'] in ['b','p','s']:
            # If the selected object is this panel, set it to a different panel.
            found = False
            for sY in range(10):
                for sX in range(10):
                    if objects[sY][sX][0] in movableObjects or objects[sY][sX][0] == 's':
                        # If it finds another movable, make it selected and break
                        changeDefaultSelected(sY, sX)
                        found = True
                        break
                if found:
                    break
            else:
                # If it loops through every panel an isn't broken (so no other movable exists)
                panels[y][x].delete('selected')
                selectedObject = []
                # Reset selectedObject

        # Use the setPanel function passing objectData as kwargs. This will only use data needed for the object being created and will delete an object if type=''.
        panel.tag_raise("highlight") #Raise the grid to be above the sprite

    for y in range(10):
        for x in range(10):
            panels[y][x].bind("<Enter>",lambda event, panel=panels[y][x]: highlightPanel(panel))
            panels[y][x].bind("<Leave>",lambda event, panel=panels[y][x]: panel.itemconfig('highlight', outline="white", width=1)) # Reset the colour.
            panels[y][x].bind("<Button-1>", lambda event, panel=panels[y][x]: build(panel))
    

    def saveLevelPopup():
        existsWarning = False
        def saveLevel():
            nonlocal existsWarning # Nonlocal defines variables that are neither global nor local, but are local to parent functions
            name = saveName.get()
            fileName = name.strip()
            fileNameRules = str.maketrans(" ", "_", "<>:\"/\\|?*") # Remove all characters that can't be in a file name
            fileName = fileName.translate(fileNameRules) # Use it to remove those characters from the file name, and replace spaces with underscores.
            if fileName.replace("_", "") == '':
                # If the name is empty or contains only spaces (replaced by underscores, removed to check)
                saveButton.grid_forget()
                cancelButton.grid_forget()
                # Remove the grid of the buttons (so they can be moved down after text is created)
                warningText = Label(savePopupFrame, text='Name must not be empty!', bg='black', fg="#ff5f5f", font=("Trebuchet MS", 10))
                warningText.grid(row=3,column=0)
                saveButton.grid(row=4,column=0, pady=(17,2))
                cancelButton.grid(row=5,column=0, pady=2)
                return

            fileName = fileName + ".txt"
            
            if os.path.exists(f"customLevels/{fileName}") and not existsWarning:
                # If a file of that name exists and the file exists warning hasn't been displayed.
                saveButton.grid_forget()
                cancelButton.grid_forget()
                # Remove the grid of the buttons (so they can be moved down after text is created)
                warningText = Label(savePopupFrame, text='Level of that name already saved.\nClick again to overwright. (OLD LEVEL WILL BE LOST)', bg='black', fg="#ff5f5f", font=("Trebuchet MS", 10))
                warningText.grid(row=3,column=0)
                saveButton.grid(row=4,column=0, pady=(17,2))
                cancelButton.grid(row=5,column=0, pady=2)
                existsWarning = True
                return
            
            file = open(f"customLevels/{fileName}", 'w')
            file.write(f"name = {name}\n")
            file.close() # Close the file to open it again in append mode (adds extra data rather than overwriting the existing data)

            file = open(f"customLevels/{fileName}", 'a')
            for i in objects: 
                # Write level object data to file
                i = str(i) # Convert list to a string
                i = i + "\n" # Add line break at the end
                file.write(i) # Add it to the level file
            #TODO: Add way to select initially selected movable object, and don't call the selectInit() function in createLevel() if there are no movables
            try:
                file.write(f"{selectedObject[0]} {selectedObject[1]}") # Store the position of the object that should start selected
            except IndexError:
                file.write("-1") # Store this if no movable objects exist
            file.close()
            savePopupFrame.destroy()


            
        savePopupFrame = Frame(root, bg='black', highlightbackground='white', highlightcolor='white', highlightthickness=5, borderwidth=10)
        saveTitle = Label(savePopupFrame, text='Save Level', bg='black', fg='white', font=("Trebuchet MS", 16, "bold"))
        saveSubtitle = Label(savePopupFrame, text='It will be saved in the \"Python/customLevels/\" folder', bg='black', fg='white', font=("Trebuchet MS", 12))
        saveTitle.grid(row=0,column=0,sticky='ew')
        saveSubtitle.grid(row=1,column=0,sticky='ew')
        saveName = Entry(savePopupFrame, width=30, font=("Arial", 14))
        saveName.grid(row=2,column=0,pady=(15,5))
        saveButton = Button(savePopupFrame, text='Save', width=32, command=saveLevel)
        saveButton.grid(row=3,column=0, pady=(17,2))
        cancelButton = Button(savePopupFrame, text='Cancel', width=32, command=lambda: savePopupFrame.destroy())
        cancelButton.grid(row=4,column=0, pady=2)
        savePopupFrame.grid(column=0,row=0,columnspan=13,rowspan=10)

    play = 0
    save = 0
    load = 0
    exit = 0
    # Create the button variables so they can be cleared

    buttonFrame = Frame(root, bg='black', borderwidth=5)
    buttonFrame.grid(row=9,column=10,columnspan=3,sticky='ew')

    def returnToEditor():
        nextLevel(load=-2) # Clear the level
        for y in range(10):
            for x in range(10):
                objects[y][x] = ['','','']
                # Clear the objects array too.
        levelEditor()

    def clearEditor(loadLevel = True):
        colourPanels = []
        for i in colourButtons.values():
            colourPanels.append(i[0])
        # Colour buttons is a list inside a dictionary so this has to be reversed to get the panels.
        editorObjects = []
        editorObjects.append(titleFrame)
        editorObjects.append(rotate)
        editorObjects.append(delete)
        editorObjects.append(rect)
        editorObjects.append(dataButtons)
        editorObjects.extend(selectableObjects)
        editorObjects.extend(colourPanels) 
        editorObjects.extend([play,save,load,exit])
        editorObjects.append(buttonFrame)
        editorObjects.append(selectionNote)
        # Create a list of every object of the level editor outside the normal grid

        for i in editorObjects:
            i.destroy()
            # Clear all of them

        if loadLevel:
            global editorLevelTemp
            editorLevelTemp = copy.deepcopy(objects) # deepcopy makes a copy including nested lists
            global selectedObjectTemp
            global selectedObject
            selectedObjectTemp = selectedObject.copy()
            # Store the current level in a temporary variable so it can be restored when level is exited
            if selectedObject == []:
                selectedObject = -1 # -1 is used in the level files for selectedObject, meaning no movables in level so don't run selectInit()
            global exitButton
            exitButton = Button(root, text='Return', command=returnToEditor)
            exitButton.grid(row=10,column=0,columnspan=10,pady=10)
            createLevel(objects, selectedObject)
        else:
            levelSelector()

    play = Button(buttonFrame,text='Play',command=clearEditor)
    save = Button(buttonFrame,text='Save', command=saveLevelPopup)
    load = Button(buttonFrame,text='Load', command=lambda: clearEditor(False))
    exit = Button(buttonFrame,text='Exit', command=lambda: root.destroy())

    play.grid(row=0,column=0)
    save.grid(row=0,column=1)
    load.grid(row=0,column=2)
    exit.grid(row=0,column=3)
    for i in range(4):
        buttonFrame.columnconfigure(i, weight=1)

levels.append(levelEditor) # levelEditor is 'level 8' so that it is loaded when level 7 is completed

def createLevel(objectsData, initialSelect, fake=False):
    """Build a level from object list. Used in level editor and when loading from a saved file."""
    nextLevel(load=-2)
    global objectData
    objectData = {}
    global selectedObject
    selectedObject = []
    laser.selectedObject = []
    root.update_idletasks()
    movables = []
    # print(objectsData)
    for y in range(10):
        for x in range(10):
            type = objectsData[y][x][0]
            data1 = objectsData[y][x][1]
            data2 = objectsData[y][x][2]
            objects[y][x] = ['','','']
            # Make sure the objects list is empty so that there isn't issues with movables storing themselves below them.
            # (Done after storing the data just in case)
            panels[y][x].delete('main')
            panels[y][x].delete('frame')
            if type != '': # If the panel shouldn't be empty.
                if type != 'd':
                    if fake:
                        setPanelFake(panels[y][x], type, setData=True, colour=data2, dir=data1,
                        flipped=data1, reverse=data1)
                        # Use the fake version of the sprites if fake mode is enabled (used when restoring editor level).
                    else:
                        setPanel(y, x, type, colour=data2, dir=data1,
                        flipped=data1, reverse=data1)
                else:
                    if fake:
                        setPanelFake(panels[y][x],type,setData=True,colour=data1,reverse=data2)
                    else:
                        setPanel(y,x,type,colour=data1,reverse=data2)
                if type in movableObjects or type == 's':
                    movables.append(panels[y][x])
                    # If the object is movable (or a spawner)
                # Most things that are required are stored in data 1, while colour is always stored in data2. (except doors and I cant be bothered changing everything)

    if (initialSelect != -1 or initialSelect != []) and not fake and movables != []:
        # initialSelect will be -1 if no movables are in the level.
        y = initialSelect[0]
        x = initialSelect[1]
        movables.remove(panels[y][x])
        movables.insert(0, panels[y][x])
        # Insert the object that starts selected at the start of the list so it starts selected.
        selectInit(initialSelect, movables)

# TODO: Make a unique colour for ending the level, replacing the default colour for objects that activate colours in the level editor.
# This will make it less confusing and also make red actually do something for objects activated by colours

def levelSelector():
    try:
        root.after_cancel(laser.runEndEvent) 
        # Cancel the event from running this again
    except ValueError:
        pass
    global exitButton
    try:
        exitButton.destroy()
    except NameError:
        pass
    try:
        levelInfo.destroy()
    except NameError:
        pass
    for y in range(10):
        for x in range(10):
            panels[y][x].delete('all')
            panels[y][x].grid_forget()
            objects[y][x] = ['','','']
            # Hide all panels (This screen doesn't use them)

    # Scrollable window logic and objects
    # Modified code from https://stackoverflow.com/a/71682458 (CC BY-SA 4.0)
    laser.endEvent = levelSelector
    root.geometry("350x450")
    # Create an outer frame
    outerFrame = Frame(root, bg='black', borderwidth=0)
    outerFrame.grid(column=0, row=0, sticky='NSEW')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    # Create a canvas in the frame
    innerCanvas = Canvas(outerFrame, bg='black', highlightthickness=0)
    # Create a scroll bar
    scrollbar = Scrollbar(outerFrame, orient=VERTICAL, command=innerCanvas.yview, width=15)
    scrollbar.pack(side=RIGHT, fill=Y)
    innerCanvas.pack(side=LEFT, fill=BOTH, expand=True)
    # Set the canvas to scroll with the scrollbar
    innerCanvas.configure(yscrollcommand = scrollbar.set)
    innerCanvas.bind(
        '<Configure>', lambda e: innerCanvas.configure(scrollregion=innerCanvas.bbox("all"))
    )
    # Create a frame inside the canvas that everything is stored in
    frame = Frame(innerCanvas, bg='black', borderwidth=0)
    innerCanvas.create_window((0, 0), window=frame, anchor="nw")

    # Actual text and buttons
    title = Label(frame,text="Level Selector", fg='white', bg='black', font=('Trebuchet MS',16,'bold'))
    subtitle = Label(frame, text="Pick a level below to play it.", fg='white', bg='black', font=('Trebuchet MS',12))

    title.grid(row=0,column=0,pady=(10,0), sticky='W')
    subtitle.grid(row=1,column=0,pady=(0,10), sticky='W')

    # colourKeys = Frame(root, bg='black', borderwidth=0)
    # defaultKey = Label(colourKeys, text='Default Levels', bg='black', fg="#2ADF2D", font=('Arial',10,'bold'))
    # customKey = Label(colourKeys, text='Custom Levels', bg='black', fg="#2A88DF", font=('Arial',10,'bold'))
    # defaultKey.grid(row=0,column=0, sticky='W')
    # customKey.grid(row=1,column=0, sticky='W')
    # colourKeys.grid(row=2,column=0, sticky='W')

    def loadLevel(level, custom):
        '''This function converts level data from a file to a string to actual level data.'''
        outerFrame.destroy()
        # Destroy the outer frame, all other objects of this screen are decendants of it so they are destroyed too.
        for y in range(10):
            for x in range(10):
                # Re-draw all the panels
                panels[y][x].grid(column=x, row=y)
        root.grid_columnconfigure(0, weight=0)
        root.grid_rowconfigure(0, weight=0)
        root.geometry("")
        if level == "editor":
            levelEditor()
        else:
            global exitButton
            exitButton = Button(root, text='Return', command=levelSelector)
            if not custom:
                exitButton.grid(row=10,column=0,columnspan=10,pady=10)
                nextLevel(load=level)
            else:
                file = open(f"customLevels/{customLevels[level]}")
                objectDataStr = file.readlines() # Read and store level data from level file
                file.close()
                objectDataStr.pop(0)
                initialSelect = objectDataStr.pop(10)
                initialSelect = initialSelect.rstrip()
                if initialSelect != '-1':
                    # If initialSelect is not -1, so there are movables which should be initialised
                    initialSelect = initialSelect.split(" ")
                    for i in range(len(initialSelect)):
                        initialSelect[i] = int(initialSelect[i])
                else:
                    initialSelect = -1
                # Remove the first and last lines (not object data)
                # Store the last line (object that should start selected)
                # Remove new line indicator, put it in a list, and change strings to integers.

                # for i in objectData:
                #     print(i)
                # for i in range(len(objectData)):
                #     objectData[i] = objectData[i].rstrip() # Remove new line characters
                #     objectData[i] = objectData[i].replace(' ','') # Remove spaces
                #     objectData[i] = objectData[i][1:-1] # Remove starting and ending square brackets
                #     dataList = objectData[i].split('],') # Split it into a list based on commas after closing brackets (to not split by data items)
                #     for j in range(len(dataList)):
                #         if dataList[j][-1] != ']':
                #             # Add the closing bracket back (this is removed above).
                #             # The last item of each line won't have it removed because it doesn't end in "]," (it ends in "]")
                #             dataList[j] = dataList[j] + "]"
                #         object = dataList[j].split(',')
                #         dataList[j] = object
                # ^^ This was removed because I found a better way to convert to list, but kept incase needed ^^
                objectData = []
                for i in range(len(objectDataStr)):
                    objectDataStr[i] = objectDataStr[i].rstrip() # Remove new line characters
                    objectData.append(ast.literal_eval(objectDataStr[i])) # Uses an ast library function to get a list from a string formatted as a list.
                global levelInfo
                levelInfo = Label(root, text=f"Custom Level \"{level}\"", bg='black', fg='white', font=('Arial', 12, 'bold'))
                levelInfo.grid(row=10, column=0, columnspan=10, pady=(10,0), sticky='ew')
                exitButton.grid(row=11, column=0, columnspan=10, pady=(0,10))
                createLevel(objectData, initialSelect)
        
    levelEditorButton = Label(frame, text='Level Editor', bg='black', fg="#EEC24A", font=('Arial', 12, 'bold'))
    # Add underline when hovered over.
    levelEditorButton.bind("<Enter>", lambda event: levelEditorButton.config(font = ('Arial', 12, 'bold', 'underline')))
    # Remove underline when mouse leaves.
    levelEditorButton.bind("<Leave>", lambda event: levelEditorButton.config(font = ('Arial', 12, 'bold')))
    # Load level when clicked
    levelEditorButton.bind("<Button-1>", lambda event: loadLevel("editor", False))
    levelEditorButton.grid(row=3,column=0,pady=(0,10), sticky=W, padx=5)

    defaultText = Label(frame, text='Default Levels', bg='black', fg="#FFFFFF", font=('Arial',10,'bold'))
    defaultText.grid(row=4,column=0,sticky=W,pady=(0,5))
    for i in range(len(levels)-1): # Don't include the level editor from the levels list
        # Create a button for every level
        text = Label(frame,text=f"• Level {i}", bg='black', fg='#2ADF2D', font=('Arial', 12, 'bold'))
        text.grid(row=i+5,column=0,pady=5,padx=(35,0),sticky=W)
        # Add underline when hovered over.
        text.bind("<Enter>", lambda event, object=text: object.config(font = ('Arial', 12, 'bold', 'underline')))
        # Remove underline when mouse leaves.
        text.bind("<Leave>", lambda event, object=text: object.config(font = ('Arial', 12, 'bold')))
        # Load level when clicked
        text.bind("<Button-1>", lambda event, level=i: loadLevel(level, False))

    # Checks for files in the customLevels folder
    files = os.listdir('customLevels/')
    customLevels = {}
    notLevels = []
    for i in files:
        # Remove items that aren't levels
        if i[-4:] != ".txt":
            # If the file does not end in .txt
            notLevels.append(i) 
            # Store it in a list to delete later (removing items from a list currently being iterated causes problems)
            continue
            # Don't try to open it (it might be a directory or something that can't be opened)
        file = open(f"customLevels/{i}")
        firstLine = file.readline()
        firstLine = firstLine.rstrip()
        # Read the first line
        if firstLine[:6] != "name =":
            # If the file does not start with the level's name
            notLevels.append(i) 
            # Store it in a list to delete later (removing items from a list currently being iterated causes problems)
            continue
        customLevels[firstLine[7:]] = i # Store the level name (the text after 'name = ' on the first line) and file in a dictionary
        file.close()
    
    for i in notLevels:
        files.remove(i)
        # Remove everything that isn't a level from the files list
    
    
    if len(customLevels) > 0:
        columnoffset = len(levels) + 5
        customText = Label(frame, text='Custom Levels', bg='black', fg="#FFFFFF", font=('Arial',10,'bold'))
        customText.grid(row=columnoffset,column=0,sticky=W,pady=(10,5))
        for i, n in zip(customLevels, range(len(customLevels))):
            text = Label(frame,text=f"• {i}", bg='black', fg='#2A88DF', font=('Arial', 12, 'bold'))
            text.grid(row=n+columnoffset+1,column=0,pady=5,padx=(35,0),sticky=W)
            # Add underline when hovered over.
            text.bind("<Enter>", lambda event, object=text: object.config(font = ('Arial', 12, 'bold', 'underline')))
            # Remove underline when mouse leaves.
            text.bind("<Leave>", lambda event, object=text: object.config(font = ('Arial', 12, 'bold')))
            # Load level when clicked
            text.bind("<Button-1>", lambda event, level=i: loadLevel(level, True))
        
    

if not os.path.isdir("customLevels"):
    # If the custom levels folder doesn't exist
    os.mkdir("customLevels")

editorStr = sys.argv[1] # Argument passed to this script from menu.py
editor = bool(editorStr)
if editor:
    levelEditor()
else:
    with open('data.txt') as f:
        level = int(f.readline())
        # Read the first line of the file and convert it to int.
    if level == 8:
        levelSelector() # Load the level selector if the level has been completed
    else:
        laser.endEvent = nextLevel # Set endEvent to the function that should run after a level is completed.
        # laser. is used to ensure that the value in the laser script is changed, not just the one local to this file.
        laser.level = level
        levels[level]()


# for i in objects:
#     print(i)
        


root.mainloop()  # Ensure all functions are defined before this is run.
