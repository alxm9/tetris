from tkinter import *
import random
import time

interface = Tk()
interface.geometry("600x600")

curr_window = 0

# Classes

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")

class button():
    def __init__(self,x,y,name):
        self.x = x 
        self.y = y
        self.name = name
        canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        text = canvas.create_text(x+75,y+25,text=name, font=("Arial", 15))        
     
        
canvas = Canvas(interface, bg = 'white', width = 600, height = 600)
canvas.pack()

canvas.create_rectangle((0,0,600,600), fill="orange", width = 0)
text = canvas.create_text(300,50,text="placeholder", font=("Arial", 24))

def selector_mover(selector, x, y):
    pass

def key_guide(curr_window, direction):  
    if curr_window == 0:
        pass
        
def key_menu(curr_window, direction ):    
# Creating the elements

startbutton = button(225,100,"Start")
placeholderbutton = button(225,175,"placeholder")
exitbutton = button(225,250,"Exit")

mainmenu_selector = selector(225,100)

buttonlist = [startbutton, placeholderbutton, exitbutton]

interface.bind("x", lambda x: selector_mover(sele))

board.bind("<Right>", lambda x: key_guide(curr_window, "right"))
board.bind("<Left>", lambda x: key_guide(curr_window, "left"))
board.bind("<Up>", lambda x: key_guide(curr_window, "up"))
board.bind("<Down>", lambda x: key_guide(curr_window, "down"))

# board.bind("<Right>", lambda x: mover(sele, x=50, y=0))
# board.bind("<Left>", lambda x: mover(sele, x=-50, y=0))
# board.bind("<Up>", lambda x: mover(sele, x=0, y=-50))
# board.bind("<Down>", lambda x: mover(sele, x=0, y=50))
        
interface.mainloop()