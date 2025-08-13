import tkinter as tk
from tkinter import *
root = tk.Tk()
houser = 1
housec = 0
image = PhotoImage(file="C:/Users/samhu/Downloads/goober_2.png")
root.iconphoto(True,image)
def addhouse():
    global houser
    global housec
    house = tk.Label(root, image=image)
    house.grid(row = houser, column = housec)
    housec += 1
    if (housec > 6):
        housec = 0
        houser += 1

root.title("house")
button = tk.Button(root, text="stop", width="20", command=addhouse)
button.grid(row=0,column=0,sticky="ew")

root.mainloop()