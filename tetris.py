from tkinter import *
from types import MethodType # to alter certain methods
import random
import time
import sys
import os
import threading

class tetrisapp():
    def __init__(self):
        self.interface = Tk()
        self.interface.geometry("600x600")        
        self.canvas = Canvas(self.interface, bg = "white", width = 600, height = 600)
        self.canvas.pack()
        self.counter = 100
        self.current_win = "na" 
        
    def bringtofront(self, window):
        for i in window.shapelist:
            game.canvas.tag_raise(i)
        self.current_win = window
        for i in window.buttonlist:
            if hasattr(i, "scope"):
                self.current_win.selector = i
        print("change")

    def rungame(self):
        self.g = threading.Thread(target=game_loop) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
        self.g.start()
        self.interface.mainloop()

game = tetrisapp()  
        
class class_window():    
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = game.canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name
        self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        self.buttonlist = []
        self.selector = "null"
        
    def __str__(self):
        return f"{self.name}"
        
    def selector_mover(self, delta_y):
        for i in self.buttonlist:
            if hasattr(i, "scope"):
                for d in self.buttonlist:
                    if d.y == (i.y + delta_y):
                        i.y = d.y
                        game.canvas.moveto(i.shape, d.x-4, d.y-4)
                        i.scope = d.role
                        return
                        
    def selector_picker(self):
        pass  


class button():
    def __init__(self,x,y,name, tied_window):
        self.x = x 
        self.y = y
        self.name = name
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        self.text = game.canvas.create_text(x+75,y+25,text=name, font=("Arial", 15)) 
        self.tied_window = tied_window
        
    def role(self):
        pass

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")
        self.scope = "Start"
        
def game_loop():
    counter = 100
    while True:
        while game.current_win == game.mainmenu_win:
            counter += -1
            time.sleep(55)
            print(game.current_win, counter)
            if counter == 0:
                counter = 100
        while game.current_win == game.tetrisgame_win:
            counter += -1
            time.sleep(0.1)
            print(game.current_win, counter)
            if counter == 0:
                counter = 100
                
game.mainmenu_win = class_window("mainmenu_win", "orange", 0, 0, 600,600)
game.tetrisgame_win = class_window("tetrisgame_win", "grey", 0, 0, 600,600)       
game.interface.bind("<q>", lambda x: game.bringtofront(game.mainmenu_win))
game.interface.bind("<w>", lambda x: game.bringtofront(game.tetrisgame_win))
game.interface.bind("<r>", lambda x: print(game.current_win))
game.interface.bind("<y>", lambda x: print(game.current_win.scope))
game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
game.interface.bind("<Return>", lambda x: game.current_win.selector.scope) 

startbutton = button(225,100,"Start", game.mainmenu_win) # need to change the last arg
highscoresbutton = button(225,175,"High Scores", game.mainmenu_win)
exitbutton = button(225,250,"Exit", "na")
selector = selector(225,100) 
game.mainmenu_win.buttonlist = [startbutton, highscoresbutton, exitbutton, selector]

def exit_role():
    sys.exit()
 
exitbutton.role = MethodType(exit_role, exitbutton) 

for i in game.mainmenu_win.buttonlist:
    game.mainmenu_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.mainmenu_win.shapelist.append(i.text)


game.bringtofront(game.mainmenu_win)
game.rungame()


    
    # current_window = "no"
    
    # def __init__(self,name,color,x1,y1,x2,y2):
        # self.shape = canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        # self.name = name
        # self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        # self.buttonlist = []
        # interface.bind("<q>", lambda x: class_window.bringtofront(mainmenu_win))
        # interface.bind("<w>", lambda x: class_window.bringtofront(game_win))
        # interface.bind("<r>", lambda x: print(class_window.current_window))

    # def __str__(self):
        # return f"{self.name}"
    
    # def bringtofront(self):
        # for i in self.shapelist:
            # canvas.tag_raise(i)
        # print(self,"1...", class_window.current_window)
        # self.current_window = self
        # print(self,"2...", class_window.current_window)
        # return self.current_window

    
# class button():
    # def __init__(self,x,y,name, tied_window):
        # self.x = x 
        # self.y = y
        # self.name = name
        # self.shape = canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        # self.text = canvas.create_text(x+75,y+25,text=name, font=("Arial", 15)) 
        # self.tied_window = tied_window
        
    # def __str__(self):
        # return f"{self.name}"    
        
    # def shape(self):
        # return self.shape

# class square():
    # def __init__(self,row,column,a,b,color):
        # self.row = row
        # self.column = column
        # self.a = a
        # self.b = b
        # self.occupier = color
        # self.outl = "white"
        # w = 0.5
        # if self.occupier == "#dde5e3":
            # self.outl = "grey"
            # w = 2
        # elif self.occupier != "#bfb7b6":
            # w = 1
            # self.outl = "black"
        # self.shape = canvas.create_rectangle(a,b,a+25,b+25, fill=self.occupier, width=w, outline = self.outl)     

# mainmenu_win = class_window("mainmenu_win", "orange", 0, 0, 600,600)
# startbutton = button(225,100,"Start", mainmenu_win) # need to change the last arg
# placeholderbutton = button(225,175,"High Scores", mainmenu_win)
# exitbutton = button(225,250,"Exit", "na")
# mainmenu_win.buttonlist = [startbutton, placeholderbutton, exitbutton]
# for i in mainmenu_win.buttonlist:
    # mainmenu_win.shapelist.append(i.shape)
    # mainmenu_win.shapelist.append(i.text)

# game_win = class_window("game_win", "grey", 0, 0, 600, 600)

# current_win = mainmenu_win

# current_win = game_win.bringtofront(current_win)
   
# interface.bind("<q>", lambda x: class_window.bringtofront(mainmenu_win))
# interface.bind("<w>", lambda x: class_window.bringtofront(game_win))


# def game_loop():
    # class_window.current_window = mainmenu_win.bringtofront()
    # counter = 100
    # while True:
        # while class_window.current_window == mainmenu_win:
            # counter += -1
            # time.sleep(0.1)
            # print("mainmenu_win", counter)
            # if counter == 0:
                # counter = 100
        # while class_window.current_window == game_win:
            # counter += -1
            # time.sleep(0.1)
            # print("game_win", counter)
            # if counter == 0:
                # counter = 100

# g = threading.Thread(target=game_loop, args=()) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
# g.start()

# interface.mainloop()