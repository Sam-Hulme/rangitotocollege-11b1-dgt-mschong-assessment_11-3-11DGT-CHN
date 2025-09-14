from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.configure(bg='black')

currentGame = 1
currentTitle = ''
currentImage = ''
titles = ['Laser','2048','Don\'t 2048']
images = ["house.png",'house.png','house.png'] #the house image is the placeholder dw about it

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


def start():
    root.destroy()
    if currentGame == 1:
        import laserlevels
    elif currentGame == 2:
        import game2048 #2048 had to be named 'game2048' because just a number doesnt work
    elif currentGame == 3:
        import dont2048

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

startButton = Button(root,text='Start',width=20,command=start)
startButton.grid(row=2,column=1,pady=(10,20))
changeGame(0)


root.mainloop()