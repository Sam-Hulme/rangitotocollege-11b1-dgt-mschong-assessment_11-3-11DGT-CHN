import tkinter
from tkinter import *
# from bindglobal import BindGlobal


root = tkinter.Tk()
screenWidth = 400
screenHeight = 600
w = Canvas(root, width=screenWidth, height=screenHeight, bg="black")
w.pack()
window = Toplevel(root)
window.attributes('-topmost', True)
window.attributes("-alpha", 0.6)
text = Label(window, text="touching")
window.configure(bg="white", height=100, width=100)
height = 10

newPanelX = 0
newPanelY = 0
panels = []
for i in range(100):
    panel = w.create_rectangle(newPanelX,newPanelY,newPanelX+40,newPanelY+60,fill="black") #Create a 40x60 rectangle at the next location
    newPanelX += 40 #Move the next location right by 40
    if (newPanelX >= screenWidth):
        newPanelX = 0 #Reset next panel X to the left and move the Y down by 60
        newPanelY += 60
    panels.append(panel) #Add all panels to a list (so they can be iterated through)
box = w.create_rectangle(10,height,20,40, fill="blue")
boxCoords = w.coords(box)

def up(event):
    w.move(box,0,-5)
    global boxCoords
    boxCoords = w.coords(box)
    

def teleport(event):
    w.moveto(box,event.x,event.y)
    global boxCoords
    boxCoords = w.coords(box)


# def panelScan(panel, result):
#     if (result == True):
#         w.itemconfigure(panel, fill="blue")
#     else:
#         w.itemconfigure(panel, fill="black")
def panelCollision(panel):
    #w.itemconfigure(panel, fill="purple")
    panelX = root.winfo_x() + w.coords(panel)[0]
    panelY = root.winfo_y() + w.coords(panel)[1]

    windowLeft = window.winfo_x() - 20 #Subtracted half the width of the panels to make it seem based on the middle of the pannel rather than the corner.
    windowRight = window.winfo_x() + window.winfo_width() - 20
    windowTop = window.winfo_y() - 30
    windowBottom = window.winfo_y() + window.winfo_height() - 30
    if (panelX > windowLeft and panelX < windowRight and panelY > windowTop and panelY < windowBottom):
        w.itemconfigure(panel, fill="blue")
    else:
        w.itemconfigure(panel, fill="black")
    #     w.after(50, panelScan, panel, True)
    # else:
    #     w.after(50, panelScan, panel, False)
    # w.after(1,panelCollisionLoop)

#panelLoops = panels[0]
def panelCollisionLoop():
    # global panelLoops
    # panelLoops += 1
    # if (panelLoops > max(panels)): #Reset once all panels done.
    #     panelLoops = panels[0]
    #     root.after(100,panelCollisionLoop)
    # else:
    #     panelCollision(panelLoops-1)
    for i in panels:
        panelCollision(i)
    root.after(100,panelCollisionLoop)

def collisioncheck():
    boxX = root.winfo_x() + boxCoords[0] #The window position plus the box position in the window
    boxY = root.winfo_y() + boxCoords[1]

    windowLeft = window.winfo_x()
    windowRight = window.winfo_x() + window.winfo_width()
    windowTop = window.winfo_y()
    windowBottom = window.winfo_y() + window.winfo_height()
    global text
    if (boxX > windowLeft and boxX < windowRight and boxY > windowTop and boxY < windowBottom):
        text.pack()
    else:
        text.pack_forget()
    root.after(10,collisioncheck)

root.bind_all("<KeyPress-w>",up)
root.bind_all("<Button-1>", teleport)
root.after(10,collisioncheck)
root.after(10,panelCollisionLoop)


root.mainloop() 