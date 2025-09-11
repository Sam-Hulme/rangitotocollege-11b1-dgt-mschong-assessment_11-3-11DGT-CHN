from tkinter import *
from core import *
import random

init(columns=4,rows=4,width=64,height=64)
from core import panelWidth, panelHeight

numbers = [] #Numbers is used to iterate over each number box that exists
for y in panels:
    for x in y:
        row = x.grid_info()['row']
        column = x.grid_info()['column']
        objects[row][column] = [0,False] #Objects is used for values that need to be accessed based on panel coordinates

def numberSprite(y,x,number,ghost=False):
    if not ghost and not objects[y][x][1] == False:
        panels[y][x].after_cancel(objects[y][x][1])
        objects[y][x][1] = False #False is used as a default because after event ids are stored as integers so 0 might be an id
    panels[y][x].delete('main')
    displayNumber = 2**number #Number variable is linear and increases by one each time
    blue = number*8+30
    colour = f"#{hex(9+blue)[2:]}{hex(29+blue)[2:]}{hex(51+blue)[2:]}"
    outlineColour = f"#{hex(29+blue)[2:]}{hex(49+blue)[2:]}{hex(71+blue)[2:]}"
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,width=6,outline=outlineColour,fill=colour,tags='main')
    panels[y][x].create_text(panelWidth/2,panelHeight/2,text=displayNumber,fill='white',font=("Arial",16,'bold'),tags='main')
    if not ghost: #Ghost is true if the number is displayed for the moving animation and shouldn't actually exist as an object.
        numbers.append([y,x,number])
        objects[y][x][0] = number

numberSprite(0,1,1)
numberSprite(2,3,2)

def deleteGhost(y,x):
    if objects[y][x][0] == 0: #Don't delete if it actually does exist, this is a final failsafe if it runs at the exact wrong time
        panels[y][x].delete('main')

def fuseNumbers(y,x,number):
    newNumber = number+1
    for i in numbers:
        if i[0] == y and i[1] == x:
            numbers.remove(i)
    numberSprite(y,x,newNumber)
    # for a in panels:
    #     for b in a:
    #         y = b.grid_info()['row']
    #         x = b.grid_info()['column']
    #         if objects[y][x][0] != 0:
    #             b.create_text(10,10,text='O',fill='white',tags='o')
    #         else:
    #             b.delete('o')
    #         b.delete('n')
    # for i in numbers:
    #     panels[i[0]][i[1]].create_text(10,20,text='N',fill='white',tags='n')

def move(dir):
    if dir == 0: 
        axis = 0
        reverse = False
    elif dir == 1:
        axis = 1
        reverse = True
    elif dir == 2:
        axis = 0
        reverse = True
    elif dir == 3:
        axis = 1
        reverse = False
    oldNumbers = sorted(numbers, key=lambda i: i[axis], reverse=reverse)
    """Sort the numbers array into a new array in ascending or decending order of the x or y axis depending on the direction to move.
    This means that there will never be the issue of a number colliding with another before that number moves away, causing it to not move fully.
    Make a new list because removing items from a list in a for loop can break it, and to not mess up the order of the actual numbers array."""
    moved = False
    for i in oldNumbers:
        fused = False
        # print(i)
        y = i[0]
        x = i[1]
        panels[y][x].delete('main')
        numbers.remove(i)
        objects[y][x][0] = 0
        while True:
            xOld = x #Store a copy of the previous x and y values to revert to if another number is in the way
            yOld = y
            if dir == 0 and y > 0:
                y -= 1
            elif dir == 1 and x < 3:
                x += 1
            elif dir == 2 and y < 3:
                y += 1
            elif dir == 3 and x > 0:
                x -= 1
            else:
                break
            if not objects[y][x][0] == 0: #Check if the box would move inside another
                if objects[y][x][0] == i[2]: #If both numbers are the same
                    fuseNumbers(y,x,i[2])
                    moved = True
                    fused = True
                    break #Don't run the usual code to create a new number box, this is done in the fuseNumbers function
                else:
                    x = xOld #Revert coordinates
                    y = yOld
                    break
            moved = True
            # print(x,i[2])
            numberSprite(y,x,i[2],True) #Create a number at each location to make it look like the box actually moved
            objects[y][x][1] = panels[y][x].after(30, deleteGhost, y, x) #Wait a short time and then delete the fake number
        # print('done')
        if fused:
            continue
        numberSprite(y,x,i[2])
    if moved: #Only create a new box if any numbers moved
        while True:
            y = random.randint(0,3)
            x = random.randint(0,3)
            if objects[y][x][0] == 0: #If the random position is empty, create a new number there. Otherwise, try again.
                numberSprite(y,x,1)
                break
    if len(numbers) == 16:
            stuck = True
            for n in numbers:
                x = n[1]
                y = n[0]
                adjacent = [ #Every number next to the current one
                    [y-1,x],
                    [y+1,x],
                    [y,x+1],
                    [y,x-1]
                ]
                for i in adjacent:
                    if (i[0] in [-1,4] or i[1] in [-1,4]): #If it is trying to check a number outside the screen
                        continue #Skip this number and check the next one
                    if objects[i[0]][i[1]][0] == n[2]: #If the number is the same as the current number
                        # print("Not stuck")
                        stuck = False #The game is not stuck, continue
                        break
            if stuck:
                fail()
                
def fail():
    print("Game Over")
    text = Label(root, text='Game Over!', font=('Arial', 24, 'bold'), fg='white', bg='black')
    text.grid(row=4,column=0,columnspan=4,sticky='nsew')
    restart = Button(root,text='Restart')
    end = Button(root,text='Return')
    restart.grid(row=5,column=0,columnspan=2,sticky='nsew')
    end.grid(row=5,column=2,columnspan=2,sticky='nsew')
    # for i in ['<w>','<a>','<s>','<d>']:
    
    # for a in panels:
    #     for b in a:
    #         y = b.grid_info()['row']
    #         x = b.grid_info()['column']
    #         if objects[y][x][0] != 0:
    #             b.create_text(10,10,text='O',fill='white',tags='o')
    #         else:
    #             b.delete('o')
    #         b.delete('n')
    # for i in numbers:
    #     panels[i[0]][i[1]].create_text(10,20,text='N',fill='white',tags='n')

buttons = []
buttons.append(root.bind('<w>', lambda event: move(0)))
buttons.append(root.bind("<a>", lambda event: move(3)))
buttons.append(root.bind("<s>", lambda event: move(2)))
buttons.append(root.bind("<d>", lambda event: move(1)))

        

root.mainloop()