import tkinter as tk
from tkinter import *
r = 0
c = 0
root = tk.Tk()
image = PhotoImage(file="C:/Users/samhu/Downloads/goober_2.png")
def addhouse():
    house = tk.Label(root, image=image)
    house.grid(row=r, column=c)
    r += 1
    if (r > 8):
        r = 0
        c += 1

root.title("house")
button = tk.Button(root, text="stop", width=25, command=addhouse)
button.pack()

root.mainloop()