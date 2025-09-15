'''2048 but you have to lose before getting 128'''
from tkinter import *
from core import *
import random

init(columns=4,rows=4,width=64,height=64)
from core import panelWidth, panelHeight

root.title("Don't 2048")

highestNumber = 0
def numberSprite(y,x,number,ghost=False):
    if not ghost and not objects[y][x][1] == False:
        panels[y][x].after_cancel(objects[y][x][1])
        objects[y][x][1] = False #False is used as a default because after event ids are stored as integers so 0 might be an id
    panels[y][x].delete('main')
    displayNumber = 2**number #Number variable is linear and increases by one each time
    global highestNumber
    if displayNumber > highestNumber:
        highestNumber = displayNumber #Store the highest number in a variable used to calculate the player's score
        if highestNumber in [256,128,64,32]:
            goalFail(number)
    blue = number*4+30
    colour = f"#{hex(151-blue)[2:]}{hex(109-blue)[2:]}{hex(109-blue)[2:]}"
    outlineColour = f"#{hex(171-blue)[2:]}{hex(120-blue)[2:]}{hex(129-blue)[2:]}"
    panels[y][x].create_rectangle(0,0,panelWidth,panelHeight,width=6,outline=outlineColour,fill=colour,tags='main')
    panels[y][x].create_text(panelWidth/2,panelHeight/2,text=displayNumber,fill='white',font=("Arial",16,'bold'),tags='main')
    if not ghost: #Ghost is true if the number is displayed for the moving animation and shouldn't actually exist as an object.
        numbers.append([y,x,number])
        objects[y][x][0] = number




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

def move(event):
    if event.keysym in ['w','W','Up']:
        dir = 0
        axis = 0
        reverse = False
    elif event.keysym in ['d','D','Right']:
        dir = 1
        axis = 1
        reverse = True
    elif event.keysym in ['s','S','Down']:
        dir = 2
        axis = 0
        reverse = True
    elif event.keysym in ['a','A','Left']:
        dir = 3
        axis = 1
        reverse = False
    else:
        return #If the pressed key isn't a direction key
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
                end(True)

# goalFrame = Frame(root,width=panelWidth*4,height=30,bg='black')
# goalFrame.grid(row=4,column=0,columnspan=4)



points = [1000,500,100,5,0]
def goalFail(number):
    global currentGoal
    currentGoal = number+1
    goal = goals[number-5]
    goal.create_line(0,0,42,42,fill='red',width=6)
    goal.create_line(42,0,0,42,fill='red',width=6)
    global score
    score = points[number-4]
    if number == 8:
        end(False)

    
goals = []
extras = [] #A list of extra objects (the text and buttons for game over or victory)
def reset():
    '''Reset and initialise variables. Used at the start and when restarting.'''
    global numbers
    numbers = [] #Numbers is used to iterate over each number box that exists
    for y in panels:
        for x in y:
            x.delete('main')
            row = x.grid_info()['row']
            column = x.grid_info()['column']
            objects[row][column] = [0,False] #Objects is used for values that need to be accessed based on panel coordinates
    for i in extras:
        i.destroy()
    numberSprite(random.randint(0,3),random.randint(0,3),1)
    numberSprite(random.randint(0,3),random.randint(0,3),2)
    root.bind('<Key>',move)
    
    global goals
    for i in goals:
        i.destroy()
    goals = []
    for i in range(4):
        goal = Canvas(root,width=42,height=42,bg='black',highlightthickness=0)
        goal.grid(row=4,column=i,pady=(10,6))
        info = [
            ['32','red'],
            ['64','orange'],
            ['128','yellow'],
            ['256','lime']
        ]
        goal.circle = goal.create_oval(2,2,40,40,outline=info[i][1],width=3)
        goal.create_text(21,21,anchor=CENTER,text=info[i][0],fill='white',font=('Arial',12,'bold'),justify=CENTER)
        goals.append(goal)
    global currentGoal
    global score
    global highestNumber
    currentGoal = 5
    score = 1000
    highestNumber = 0
reset()    


def end(fail):
    print("Game Over")
    if fail:
        title = "Didn\'t 2048!"
        subtitle = f'Score: {score}'
        goals[currentGoal-5].itemconfig(goals[currentGoal-5].circle, fill='green')
    else:
        title = "Game Over!"
        subtitle = "You did 2048!"
    frame = Frame(root,width=panelWidth*4,height=30,bg='black') #Create a frame to make the game over text a fixed height.
    #The width is the width of four panels
    frame.grid_propagate(0)
    frame.grid(row=5,column=0,columnspan=4,sticky='nsew')
    extras.append(frame)
    text = Label(frame, text=title, font=('Arial', 24, 'bold'), fg='white', bg='black')
    text.place(x = frame.winfo_reqwidth() // 2, y = frame.winfo_reqheight() // 2, anchor = CENTER)
    extras.append(text)
    scoreText = Label(root, text=subtitle, font=("Arial", 14), fg='white', bg='black')
    extras.append(scoreText)
    scoreText.grid(row=6,column=0,columnspan=4,sticky='new',pady=(0,4))
    restart = Button(root,text='Restart',command=reset)
    extras.append(restart)
    end = Button(root,text='Return',command=exit)
    extras.append(end)
    restart.grid(row=7,column=0,columnspan=2,sticky='nsew')
    end.grid(row=7,column=2,columnspan=2,sticky='nsew')
    root.unbind('<Key>')

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
    #     panels[i[0]][i[1]].create_text(10,20,text='N',fill='white',tags='n'

def exit():
    root.destroy()
    import menu

root.protocol("WM_DELETE_WINDOW", exit)

root.mainloop()