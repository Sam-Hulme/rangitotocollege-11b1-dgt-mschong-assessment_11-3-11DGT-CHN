import tkinter as tk
from tkinter import *
import random
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
button = tk.Button(root, text="🍍", width="20", command=addhouse)
button.grid(row=0,column=0,sticky="ew")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
def popuploop():
    popup = Toplevel(root)
    popup.geometry(f"{160}x{90}+{random.randint(0,width)}+{random.randint(0,height)}") 
    popuphouse = Label(popup, image=image)
    popuphouse.pack()
    popup.protocol("WM_DELETE_WINDOW", popuploop)
    popup.bind("<KeyPress>", stop)
    root.after(1000, popuploop)

def stop(event):
    if (event.keysym == 'c'):
        root.destroy()

root.after(1000, popuploop)
root.bind("<KeyPress>", stop)
popuploop()
root.protocol("WM_DELETE_WINDOW", popuploop)
root.mainloop()




