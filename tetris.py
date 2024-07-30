from tkinter import *
from types import MethodType # to alter certain methods
import random
import time
import sys
import os
import threading


pieces_d = { 
            "piece_I" : [  [1,4],  [1,5],  [1,6],  [1,7] ],
            "piece_J" : [  [1,4],  [2,4],  [2,5],  [2,6] ],
            "piece_L" : [  [1,6],  [2,4],  [2,5],  [2,6] ],
            "piece_O" : [  [1,5],  [1,6],  [2,5],  [2,6] ],
            "piece_S" : [  [1,5],  [1,6],  [2,4],  [2,5] ],
            "piece_T" : [  [1,5],  [2,4],  [2,5],  [2,6] ],
            "piece_Z" : [  [1,4],  [1,5],  [2,5],  [2,6] ]            
            }

            
class tetrisapp():
    def __init__(self):
        self.running = True
        self.game_started = False
        self.interface = Tk()
        self.interface.geometry("600x600")        
        self.canvas = Canvas(self.interface, bg = "white", width = 600, height = 600)
        self.canvas.pack()
        self.counter = 100
        self.current_win = "na"
        self.previous_win = "na"
        self.can_pause = False
        
    def bringtofront(self, previous_win, new_win):
        if game.previous_win == "na":
            game.previous_win = game.mainmenu_win
        self.previous_win = previous_win
        self.current_win = new_win
        for i in new_win.shapelist:
            game.canvas.tag_raise(i)
        if hasattr(new_win, "grid_dict"):
            for i in new_win.grid_dict:
                print(i)
                game.canvas.tag_raise(new_win.grid_dict[i].shape)
        for i in new_win.buttonlist:
            if hasattr(i, "scope"):
                self.current_win.selector = i
        if self.current_win == game.mainmenu_win:
            self.game_started = False
            game.tetrisgame_win.stamper_queue = []
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope()) 
            game.interface.bind("<Escape>", lambda x:  game.method_handler())
        if self.current_win == game.highscore_win:
            self.game_started = False
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<y>", lambda x: print(game.current_win.selector.scope))
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope()) 
            game.interface.bind("<Escape>", lambda x:  game.method_handler())
        if self.current_win == game.tetrisgame_win:
            self.game_started = True
            start_message()
            self.can_pause = True
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<Down>", lambda x: print("down"))
            game.interface.bind("<Up>", lambda x: print("up")) 
            game.interface.bind("<Left>", lambda x: print("left"))       
            game.interface.bind("<Right>", lambda x: print("right"))     
            game.interface.bind("<x>", lambda x: game.tetrisgame_win.stamper_queue.pop(1))       
            game.interface.bind("<d>", lambda x: print(game.tetrisgame_win.stamper_queue[2].squarelist))                
        if self.current_win == game.pause_win:
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope())  
            game.interface.bind("<Escape>", lambda x:  game.method_handler())            
            self.can_pause = False
        print(game.current_win)

    def rungame(self):
        self.g = threading.Thread(target=game_loop) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
        self.g.start()
        self.interface.mainloop()
        
    def exit(self):
        self.running = False
        sys.exit()
        
    def method_handler(self):
        if self.current_win == game.pause_win:
            print("HERE")
            self.can_pause = False
            game.bringtofront(game.pause_win, game.tetrisgame_win)
            return
        if self.can_pause == False:
            print("Can't pause")
            if self.current_win == game.highscore_win:
                game.bringtofront(game.previous_win, game.mainmenu_win)
        else:
            game.bringtofront(game.previous_win, game.pause_win)
        

game = tetrisapp()  
        
class class_window():    
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = game.canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name
        self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        self.buttonlist = []
        self.current_stamper = False
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

class class_window_game():    
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = game.canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name
        self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        self.shapelist_2 = [] # For stamped blocks only. Separate list so UI elements don't get accidentally deleted 
        self.buttonlist = []
        self.stamper_queue = []
        self.current_stamper = False
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
    
    def stamp_maker(self):
        colorlist = ["cyan", "blue", "orange", "yellow", "green", "#bc8ad0", "red"]
        choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"]
        piece = random.choice(choicelist)
        index = choicelist.index(piece)
        color = colorlist[index]
        slist = []
        for i in range(0,4):
            r = pieces_d[piece][i][0]
            c = pieces_d[piece][i][1]
            object = square(r,c,-55+(c*25),110+(r*25), color)
            slist.append(object)           
        object = stamper(slist, piece)
        return object
       
    def queue_arranger(self):
        for d in range(0,4):
            object = self.stamper_queue[d]
            delta_x = 0
            if object.blocktype  == "piece_I":
                delta_x = - 8
            if object.blocktype  == "piece_O":
                delta_x = - 10
            for x in object.squarelist:
                x.b = x.b + (d*85)
                x.a = x.a + delta_x
                game.canvas.moveto(x.shape, x.a, x.b)
                
    

class button():
    def __init__(self,x,y,name, tied_window):
        self.x = x 
        self.y = y
        self.name = name
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        self.text = game.canvas.create_text(x+75,y+25,text=name, font=("Arial", 15)) 
        self.tied_window = tied_window

    def role(self):
        game.bringtofront(game.previous_win, self.tied_window)

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")
        self.scope = "Start"

class square():
    def __init__(self,row,column,a,b,color):
        self.row = row
        self.column = column
        self.a = a
        self.b = b
        self.occupier = color # color
        self.outl = "white"
        w = 0.5
        if self.occupier == "#dde5e3":
            self.outl = "grey"
            w = 2
        elif self.occupier != "#bfb7b6":
            w = 1
            self.outl = "black"
        self.shape = game.canvas.create_rectangle(a,b,a+25,b+25, fill=self.occupier, width=w, outline = self.outl)       

class stamper():
    def __init__(self, squarelist, blocktype):
        self.squarelist = squarelist # we're going to have square instances      
        self.blocktype = blocktype
        
    def move_down(self):
        for i in self.squarelist:
            self.squarelist[i].y = self.squarelist[i].y + 25
    
    def move_lr(self, delta_x):
        for i in self.squarelist:
            self.squarelist[i].x = self.squarelist[i].x + delta_x
    
def start_message():
        startrect = game.canvas.create_rectangle(200, 200, 400, 300, fill="orange", width=1, outline = "white")
        text = game.canvas.create_text(300,250,text="START", font=("Arial", 17))
        game.interface.after(400, delete_message, startrect, text)

def delete_message(inv, txt):
    game.canvas.delete(inv, txt)
    
def game_loop():
    game.current_win.selector_mover(0)
    game.pause_win.selector_mover(0)
    while game.running == True:
        while (game.current_win != game.tetrisgame_win):
            if game.running == False:
                return
            if game.current_win == game.mainmenu_win:
                game.counter = 200
            time.sleep(0.1)
            print(game.current_win,"not game", game.counter)
        while game.current_win == game.tetrisgame_win:
            if game.running == False:
                return
            while len(game.tetrisgame_win.stamper_queue) < 4:
                instance = game.tetrisgame_win.stamp_maker()
                game.tetrisgame_win.stamper_queue.append(instance)
                print(game.tetrisgame_win.stamper_queue)
                if len(game.tetrisgame_win.stamper_queue) == 4:
                    game.tetrisgame_win.queue_arranger()
            instance = False
            game.counter += -1
            time.sleep(0.1)
            print(game.current_win, game.counter)
            if game.counter == 0:
                game.counter = 200


# Windows                
game.mainmenu_win = class_window("mainmenu_win", "orange", 0, 0, 600,600)     
game.tetrisgame_win = class_window_game("tetrisgame_win", "green", 0, 0, 600,600)  
game.highscore_win = class_window("highscore_win", "green", 0, 0, 600,600) 
game.pause_win = class_window("pause_win", "grey", 150,450,450,150)

# mainmenu_win
startbutton = button(225,100,"Start", game.tetrisgame_win) # need to change the last arg
highscoresbutton = button(225,175,"High Scores", game.highscore_win)
exitbutton = button(225,250,"Exit", "na")
menuselector = selector(225,100)
game.mainmenu_win.buttonlist = [startbutton, highscoresbutton, exitbutton, menuselector]

# tetrisgame_win
game.tetrisgame_win.upnext_shape = game.canvas.create_rectangle((30,120,145,500), fill="black", width = 0.5, outline = "white")
game.tetrisgame_win.upnext_text = game.canvas.create_text(85,105,text="UP NEXT", font=("Arial", 12))
game.tetrisgame_win.level = 1
game.tetrisgame_win.level_text = game.canvas.create_text(300,30,text=("Lv.",game.tetrisgame_win.level), font=("Arial", 24))
game.tetrisgame_win.score = 0
game.tetrisgame_win.score_container = game.canvas.create_rectangle((450,120,570,150), fill="black", width = 0.5, outline = "white")
game.tetrisgame_win.score_text = game.canvas.create_text(510,105,text="SCORE", font=("Arial", 12))
game.tetrisgame_win.score_display = game.canvas.create_text(510,135,text=game.tetrisgame_win.score, font=("Arial", 12),  fill = "white")
game.tetrisgame_win.shapelist = [game.tetrisgame_win.shape,game.tetrisgame_win.upnext_shape,game.tetrisgame_win.upnext_text,game.tetrisgame_win.level_text,game.tetrisgame_win.score_container,game.tetrisgame_win.score_text,game.tetrisgame_win.score_display]

# pausewin
game.pause_text = game.canvas.create_text(300,180,text="Game Paused", font=("Arial", 24))
game.pause_win.shapelist.append(game.pause_text)
pause_menubutton = button(225,250,"Main Menu", game.mainmenu_win)
pause_exitbutton = button(225,325,"Exit", "na")
pauseselector = selector(225,250)
game.pause_win.buttonlist = [pause_menubutton, pause_exitbutton, pauseselector]

w1 = game.mainmenu_win # self
def exit_role(w1):
    game.running = False
    print("EXITING")
    sys.exit()
exitbutton.role = MethodType(exit_role, exitbutton)

w2 = game.pause_win # self
def exit_role(w2):
    game.running = False
    print("EXITING")
    sys.exit()
pause_exitbutton.role = MethodType(exit_role, pause_exitbutton)

game.tetrisgame_win.grid_dict = {}
for r in range(1,21):
    for c in range(1,11):
        game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25), "#bfb7b6") 

    # def block_maker():
        # colorlist = ["cyan", "blue", "orange", "yellow", "green", "#bc8ad0", "red"]
        # choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"]
        # piece = random.choice(choicelist)
        # index = choicelist.index(piece)
        # color = colorlist[index]
        # slist = []
        # for i in range(0,4):
            # r = pieces_d[piece][i][0]
            # c = pieces_d[piece][i][1]
            # object = square(r,c,150+(c*25),40+(r*25), color)
            # slist.append(object)        
        # return slist
        
# startbutton.role = MethodType(game.bringtofront(game))

for i in game.mainmenu_win.buttonlist:
    game.mainmenu_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.mainmenu_win.shapelist.append(i.text)

for i in game.pause_win.buttonlist:
    game.pause_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.pause_win.shapelist.append(i.text)        
        
game.interface.bind("<Destroy>", lambda x: game.exit())

game.bringtofront("na",game.mainmenu_win)
game.rungame()