from tkinter import *
import random
import time

interface = Tk()
interface.geometry("600x600")

# curr_window
# 0 = main menu
# 1 = game
# 2 = high score
# 3 = escape

curr_window = 0

# Classes

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")
        self.scope = False

class button():
    def __init__(self,x,y,name):
        self.x = x 
        self.y = y
        self.name = name
        self.shape = canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        self.text = canvas.create_text(x+75,y+25,text=name, font=("Arial", 15))        

class window():
    def __init__(self,color,x1,y1,x2,y2):
        self.shape = canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        
canvas = Canvas(interface, bg = 'white', width = 600, height = 600)
canvas.pack()

# canvas.create_rectangle((0,0,600,600), fill="orange", width = 0) REDUNDANT
# text = canvas.create_text(300,50,text="placeholder", font=("Arial", 24)) REDUNDANT

def selector_mover(selector, delta_x, delta_y):
    print("selector_mover")
    selector.x += delta_x
    selector.y += delta_y
    canvas.moveto(selector.shape, selector.x-3, selector.y-3) #these are offset by -3 because otherwise they get offset by the moveto function for some reason

def boundary_checker(selector, delta_y):
    print("boundary_checker")
    for i in range(len(menu_buttonlist)):
        print(selector.y+delta_y, menu_buttonlist[i].y)
        if selector.y+delta_y == menu_buttonlist[i].y:
            print(menu_buttonlist[i].text)
            return menu_buttonlist[i].text
    else:
        return False
    
def key_guide(curr_window, direction):
    if curr_window == 0:
        key_menu(curr_window, direction)
    if curr_window == 1:
        pass
    if curr_window == 2:
        pass
        
def key_menu(curr_window, direction):    
    if direction == ("right" or "left"):
        return
    elif direction == "up":
        d = boundary_checker(mainmenu_selector, -75)
        if d != False:
            selector_mover(mainmenu_selector, 0, -75)
            selector_mover.scope = d
    elif direction == "down":
        d = boundary_checker(mainmenu_selector, 75)
        if d != False:
            selector_mover(mainmenu_selector, 0, 75)
            selector_mover.scope = d
    elif direction == "enter":
        pass
        

def select():
    pass
        
def bring_to_front(window):
    instance_dict = vars(window)
    print(instance_dict)
    for key in instance_dict.keys():
        value = instance_dict.get(key)
        if isinstance(value, button):
            print("button FOUND") # I can just put this through the function again.
            bring_to_front(value) # starts another instance of the same function 
        else:
            # print(key)
            # print(type(instance_dict.get(key)))
            canvas.tag_raise(value)
    canvas.tag_raise(mainmenu_selector.shape)
            
# Creating the elements


# Windows - Main Menu
mainmenu = window("orange",0,0,600,600)
mainmenu.text = canvas.create_text(300,50,text="placeholder", font=("Arial", 24))
mainmenu.startbutton = button(225,100,"Start")
mainmenu.placeholderbutton = button(225,175,"placeholder")
mainmenu.exitbutton = button(225,250,"Exit")

# Windows - Game
gamewindow = window("grey",0,0,600,600)

# Windows - High Score
highscore = window("blue",0,0,600,600)

# Windows - Escape
escape = window("green",0,0,600,600)

# Buttons
# startbutton = button(225,100,"Start")
# placeholderbutton = button(225,175,"placeholder")
# exitbutton = button(225,250,"Exit")


canvas.tag_raise(mainmenu.shape)
# for i in range(len(mainmenu.shapelist)):
    # if hasattr(mainmenu.shapelist[i], "shape"):
        # canvas.tag_raise(mainmenu.shapelist[i].shape)
    # if hasattr(mainmenu.shapelist[i], "text"):
        # canvas.tag_raise(mainmenu.shapelist[i].text)
        


mainmenu_selector = selector(225,100)

# canvas.tag_raise(mainmenu.shape)

# Lists

menu_buttonlist = [mainmenu.startbutton, mainmenu.placeholderbutton, mainmenu.exitbutton]


bring_to_front(mainmenu)

# interface.bind("x", lambda x: selector_mover(sele)) ????


interface.bind("x", lambda x: print(selector_mover.scope))    ### DEBUG 

interface.bind("Enter", lambda x: key_guide(curr_window, "enter"))

interface.bind("<Right>", lambda x: key_guide(curr_window, "right"))
interface.bind("<Left>", lambda x: key_guide(curr_window, "left"))
interface.bind("<Up>", lambda x: key_guide(curr_window, "up"))
interface.bind("<Down>", lambda x: key_guide(curr_window, "down"))

# board.bind("<Right>", lambda x: mover(sele, x=50, y=0))
# board.bind("<Left>", lambda x: mover(sele, x=-50, y=0))
# board.bind("<Up>", lambda x: mover(sele, x=0, y=-50))
# board.bind("<Down>", lambda x: mover(sele, x=0, y=50))
        
interface.mainloop()