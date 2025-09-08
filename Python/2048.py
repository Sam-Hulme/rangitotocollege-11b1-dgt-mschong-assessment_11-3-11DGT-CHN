from tkinter import *
from laser import * #This game is based on the first game, and uses a similar panel system

numbers = []
for y in panels:
    for x in y:
        row = x.grid_info()['row']
        column = x.grid_info()['column']
        objects[row][column] = 0
def numberSprite(y,x,number):
    panels[y][x].delete('main')
    displayNumber = 2**number #Number variable is linear and increases by one each time
    blue = number*4+20
    colour = f"#{hex(9+blue)[2:]}{hex(29+blue)[2:]}{hex(51+blue)[2:]}"
    outlineColour = f"#{hex(29+blue)[2:]}{hex(49+blue)[2:]}{hex(71+blue)[2:]}"
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,width=6,outline=outlineColour,fill=colour,tags='main')
    panels[y][x].create_text(panelWidth/2,panelHeight/2,text=displayNumber,fill='white',font=("Arial",16,'bold'),tags='main')
    numbers.append([y,x,number,0])
    objects[y][x] = number    

numberSprite(5,5,1)
numberSprite(5,6,1)

def move(dir):
    oldNumbers = numbers.copy() #Make a copy of the list because removing items from a list in a for loop can break it
    # oldNumbers.extend(numbers[:]) #Double the length of oldNumbers to run everything twice so that numbers move properly after collisions regardless of run order.
    for i in oldNumbers:
        # print(i)
        y = i[0]
        x = i[1]
        panels[y][x].delete('main')
        
        numbers.remove(i)
        objects[y][x] = 0
        while True:
            xOld = x #Store a copy of the previous x and y values to revert to if another number is in the way
            yOld = y
            if dir == 0 and y > 0:
                y -= 1
            elif dir == 1 and x < 9:
                x += 1
            elif dir == 2 and y < 9:
                y += 1
            elif dir == 3 and x > 0:
                x -= 1
            else:
                break
            print(x)
            if not objects[y][x] == 0:
                x = xOld
                y = yOld
                if (i[3] < 9):
                    i[3] += 1
                    oldNumbers.append(i)
                    # print(i[3])
                break
        print(y,x)
        numberSprite(y,x,i[2])
        # print(y,x,i[0],i[1])
        # print('')

root.bind("<w>", lambda event: move(0))
root.bind("<a>", lambda event: move(3))
root.bind("<s>", lambda event: move(2))
root.bind("<d>", lambda event: move(1))

        

root.mainloop()