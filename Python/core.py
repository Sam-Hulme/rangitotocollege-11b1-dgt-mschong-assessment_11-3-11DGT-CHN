'''A file imported by the actual games that creates the panels and defines basic variables.'''

import tkinter
from tkinter import *

root = tkinter.Tk()
root.configure(bg='black')

panels = [[]] #The canvases themselves that will be drawn to to show sprites.
objects = [[]] #A grid of empty strings that will be filled to reflect the types of objects at each location
panelWidth = 0
panelHeight = 0

#This game uses a panel system for elements, with a grid of canvases that can be modified to have images or solid colours displayed.

def init(columns,rows,width,height):
    for i in range(columns*rows):
        row = len(panels)-1
        if (len(panels[row])+1 > columns): #if the current row list would have more items than the desired column count, move to the next row
            panels.append([])
            objects.append([])
        row = len(panels)-1
        column = len(panels[row])
        panel = Canvas(root, width=width, height=height, bg="black", highlightthickness=0, bd=0)
        panel.grid(row=row, column=column)
        panels[row].append(panel) #Add all panels to a list (so they can be iterated through)
        objects[row].append(['','',''])
        global panelWidth
        global panelHeight
        panelWidth = width
        panelHeight = height
    root.update_idletasks()
        # return panels


def leveltemplate(event = ''):
    for y in panels:
        for x in y:
            x.delete('debug')
            row = x.grid_info()["row"]
            column = x.grid_info()["column"]
            x.create_rectangle(0,0,panelWidth,panelHeight,fill='',outline='white',tags='debug')
            x.create_text(panelWidth/2,panelHeight/2,text=f"{row}, {column}",fill='white', tags='debug')
    root.after(1000,leveltemplate)

root.bind("<space>",leveltemplate)

def _create_circle(self, x, y, r, **kwargs): # https://stackoverflow.com/a/17985217 Modified code from user mgold on stackoverflow. Licenced under CC BY-SA 4.0
    '''Creates a circle based on a center point and radius rather than two corners like the original oval function.'''
    if 'rY' in kwargs: #rY allows for the radius to be changed vertically seperately for an oval shape
        rY = kwargs['rY']
        kwargs.pop('rY')
    else:
        rY = r
    return self.create_oval(x-r, y-rY, x+r, y+rY, **kwargs)
Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    '''The same as above but for an arc.'''
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs.pop("end") - kwargs["start"]
    if 'rY' in kwargs:
        rY = kwargs['rY']
        kwargs.pop('rY')
    else:
        rY = r
    return self.create_arc(x-r, y-rY, x+r, y+rY, **kwargs)
Canvas.create_circle_arc = _create_circle_arc

'''Next commit notes:




'''