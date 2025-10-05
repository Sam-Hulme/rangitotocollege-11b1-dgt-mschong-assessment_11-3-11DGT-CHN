import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
import os
import psutil
import time


memory = psutil.virtual_memory()
total_mem = str(round(memory.total/1000000))
remaining_mem = str(round((memory.total-memory.available)/1000000))
percentage_mem = 100 - memory.percent #memory.percent is the percent of memory used, so 100 - memory.percent is the percentage of memory remaining

def number_punctuation(number, extra = ''):
    '''Add a comma to thousands (only works for whole numbers, breaks with floats)'''
    if len(number) > 3:
        return number[:-3] + ',' + number[-3:] + extra
    else:
        return number + extra
# wait = int(input("Delay: "))
# print(number_punctuation(total_mem,' MB'))
# print(round(memory.used/1000000), 'MB')
# print(memory.percent)
time.sleep(0)

root = tk.Tk()
root.attributes('-topmost', True)
houser = 1
housec = 0


image = PhotoImage(file=os.path.relpath('house.png', os.path.dirname(__file__)))
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
root.geometry(f"{520}x{65}+{50}+{50}") 
# button = tk.Button(root, text="🍍", width="20", command=addhouse)
# button.grid(row=0,column=0,sticky="ew")
ramText = Label(root, text='Remaining RAM:', font=('Comic Sans MS', 14, 'bold'))
ramText.config(text="Remaining RAM: " + number_punctuation(remaining_mem,' MB') + " / " + number_punctuation(total_mem, ' MB'))
ramText.grid(row=0,column=0,sticky='w',padx=10)
ramMeter = ttk.Progressbar(length=500)
ramMeter.grid(row=1,column=0,pady=(0,10), padx=10)
ramMeter['value'] = percentage_mem


width = root.winfo_screenwidth()
height = root.winfo_screenheight()
def popuploop():
    global memory
    global remaining_mem
    global total_mem
    global percentage_mem
    global ramText
    global ramMeter
    memory = psutil.virtual_memory()
    remaining_mem = str(round((memory.total-memory.used)/1000000)) #Update the remaining ram meter
    ramText.config(text="Remaining RAM: " + number_punctuation(remaining_mem,' MB') + " / " + number_punctuation(total_mem, ' MB'))
    percentage_mem = 100 - memory.percent
    ramMeter['value'] = percentage_mem
    
    popup = Toplevel(root)
    popup.geometry(f"{160}x{90}+{random.randint(0,width)}+{random.randint(0,height)}") 
    popuphouse = Label(popup, image=image)
    popuphouse.pack()
    popup.protocol("WM_DELETE_WINDOW", popuploop)
    popup.focus_force()
    popup.attributes('-topmost', True) #Bring the popup to the top, but dont keep it there (to keep the ram meter over it)
    popup.attributes('-topmost', False)
    popup.bind("<KeyPress>", stop)
    root.after(100, popuploop)

    root.focus_force()

def stop(event):
    if (event.keysym == 'c'):
        root.destroy()
root.bind("<KeyPress>", stop)
root.after(100, popuploop)
popuploop()
root.protocol("WM_DELETE_WINDOW", popuploop)
root.mainloop()