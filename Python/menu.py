from tkinter import *
import subprocess
from PIL import Image, ImageTk

root = Tk()
root.configure(bg='black')

currentGame = 1
currentTitle = ''
currentImage = ''
titles = ['Laser','2048','Don\'t 2048']
images = ["house.png",'mschong.png','house.png'] #the house image is the placeholder dw about it
editor = False

def changeGame(dir):
    global currentGame
    currentGame += dir
    if currentGame > 3:
        currentGame = 1
    elif currentGame < 1:
        currentGame = 3
    global currentTitle
    global currentImage
    currentTitle = titles[currentGame-1]
    currentImage = images[currentGame-1]
    title.configure(text=currentTitle)
    image = Image.open(currentImage)
    image = image.resize((480,270))
    global tkImage
    tkImage = ImageTk.PhotoImage(image)
    logo.config(image=tkImage)
    if currentGame == 1 and editorAvailable:
        levelEditorButton.grid(row=3,column=1,pady=(0,20))
        # Add the level editor button
    else:
        levelEditorButton.grid_forget() 
        # Remove the level editor button without deleting it
        


def start(startEditor = ''):
    global runningText
    runningText = Canvas(root,width=300,height=120,bg='black',highlightthickness=5)
    runningText.create_text(150,50,text='Game Running',font=("Arial",15,'bold'),fill='white')
    runningText.create_text(150,70,text='Close game to continue',font=('Arial',10),fill='white')
    runningText.place(x=root.winfo_width()/2,y=root.winfo_height()/2,anchor='center')
    global editor
    editor = startEditor
    root.after(2,runGame)



def runGame():
    if currentGame == 1:
        subprocess.run(["python","laserlevels.py",editor]) # Info on whether or not to start in the editor is passed to the laser script
    elif currentGame == 2:
        subprocess.run(["python","game2048.py"]) # 2048 had to be named 'game2048' because just a number didn't work
    elif currentGame == 3:
        subprocess.run(["python","dont2048.py"])
    runningText.destroy()

title = Label(root,text=currentTitle,fg='white',bg='black',font=('Arial',20,'bold'))
title.grid(row=0,column=1,sticky='nsew',padx=20,pady=10)

arrowL = Canvas(root, width=25, height=50,bg='black',highlightthickness=0)
arrowL.create_polygon(20,0,0,25,20,50,fill='white',outline='grey',width=3)
arrowL.grid(row=1,column=0,padx=20,sticky='W')
arrowL.bind('<Button-1>', lambda event: changeGame(-1))

arrowR = Canvas(root, width=25, height=50,bg='black',highlightthickness=0)
arrowR.create_polygon(0,0,20,25,0,50,fill='white',outline='grey',width=3)
arrowR.grid(row=1,column=2,padx=20,sticky='E')
arrowR.bind('<Button-1>', lambda event: changeGame(1))

logo = Label(root, bg='black')
logo.grid(row=1,column=1,pady=(0,10))


levelEditorButton = Button(root,text='Level Editor',width=20,command=lambda: start(startEditor='true')) # Has to be a string for some reason
try:
    f = open('data.txt') # Open the data.txt file to read
    data = f.readlines()
    editorAvailable = (data[1].lower() == "true")
    # Check if the line contains the text "true", returns true if it does.
    # The second line of the file stores whether or not the level editor is available
    f.close()
    
except FileNotFoundError:
    # If this is the first launch, the file won't exist, so create it.
    editorAvailable = False
    f = open("data.txt", "x")
    f.write('0') #Level
    f.write('\n') # New line
    f.write('False') #Editor unlocked

if editorAvailable:
    levelEditorButton.grid(row=3,column=1,pady=(0,20))

startButton = Button(root,text='Start',width=20,command=start)
startButton.grid(row=2,column=1,pady=(10,20))
changeGame(0)


root.mainloop()