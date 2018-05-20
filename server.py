# DON'T BE A DICK PUBLIC LICENSE
#
#> Version 1.1, December 2016
#
#> Copyright (C) 2018 Jaakko Sirén & Olli Peura
#
#Everyone is permitted to copy and distribute verbatim or modified
#copies of this license document.
#
#> DON'T BE A DICK PUBLIC LICENSE
#> TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#1. Do whatever you like with the original work, just don't be a dick.
#
#   Being a dick includes - but is not limited to - the following instances:
#
# 1a. Outright copyright infringement - Don't just copy this and change the name.
# 1b. Selling the unmodified original with no work done what-so-ever, that's REALLY being a dick.
# 1c. Modifying the original work to contain hidden harmful content. That would make you a PROPER dick.
#
#2. If you become rich through modifications, related works/services, or supporting the original work,
#share the love. Only a dick would make loads off this work and not buy the original work's
#creator(s) a pint.
#
#3. Code is provided with no warranty. Using somebody else's code and bitching when it goes wrong makes
#you a DONKEY dick. Fix the problem yourself. A non-dick would submit the fix back.
        
from tkinter import *
import random
import time
import sys
import itertools
from random import randint
import socket,os
from threading import Thread
import time



class Worm:
    def __init__(self, canvas, color):
        self.canvas = canvas
        canvas.bind_all('<KeyPress-Left>', self.move_left)
        canvas.bind_all('<KeyPress-Right>', self.move_right)
        canvas.bind_all('<KeyPress-Up>', self.move_up)
        canvas.bind_all('<KeyPress-Down>', self.move_down)
        self.lastCoords=[]
        self.lenght =0
        self.color = color
        self.childs=[]
        self.pos=[0,0]
        self.ran = self.getRandomCoords()
        self.food = canvas.create_rectangle(self.ran, self.ran, self.ran+50, self.ran+50, fill='red')
        self.id = canvas.create_rectangle(50, 50, 0, 0, fill=color)
        self.move =0
        self.x = 100
        self.y = 0
        self.direction = 1
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
        self.is_hitting_bottom = False

    def move_left(self, event):
        if self.direction!=1:
            self.direction=2
    def move_right(self, event):
        if self.direction!=2:
            self.direction=1
    def move_up(self, event):
        if self.direction!=3:
            self.direction=4
    def move_down(self, event):
        if self.direction!=4:
            self.direction=3
    def getRandomCoords(self):
        return float(randint(0, 19)*50)

    def testForSelfCollision(self):
        if [self.pos[0], self.pos[1]] in self.lastCoords[-1*self.lenght:]:
            sys.exit()

    def testForCollision(self, position):
        if self.ran == position[0] and self.ran==position[1] and self.ran+50==position[2] and self.ran+50==position[3]:
            self.ran = self.getRandomCoords()
            self.canvas.delete(self.food)
            self.lenght = self.lenght+1
            self.food = canvas.create_rectangle(self.ran, self.ran, self.ran+50, self.ran+50, fill=self.color)

    def draw(self):

        self.move = self.move +1
        self.pos = self.canvas.coords(self.id)
        if self.move == 100:
            print("move")
            i=0
            try:
                for _ in itertools.repeat(None, self.lenght):
                    self.canvas.delete(self.childs[i])
                    i = i+1
            except:
                pass

            self.childs=[]
            i=1
            self.testForCollision(self.pos)
            self.testForSelfCollision()
            self.lastCoords.append([self.pos[0],self.pos[1]])
            for _ in itertools.repeat(None, self.lenght):
                self.childs.append(canvas.create_rectangle(self.lastCoords[-i][0], self.lastCoords[-i][1], self.lastCoords[-i][0]+50, self.lastCoords[-i][1]+50, fill="red"))
                i = i+1
            self.move =0
            if self.direction == 1:
                self.canvas.move(self.id, 50, 0)
            if self.direction == 2:
                self.canvas.move(self.id, -50, 0)
            if self.direction == 3:
                self.canvas.move(self.id, 0, 50)
            if self.direction == 4:
                self.canvas.move(self.id, 0, -50)

        if self.pos[0] > self.canvas_width or self.pos[0]<0 or self.pos[1]<0 or self.pos[1]>self.canvas_height:
            print("kusit")
            sys.exit()

tk = Tk()
tk.title('Worm')
canvas = Canvas(tk, width=1000, height=1000, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

worm = Worm(canvas, 'black')
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    os.remove("/tmp/socketname")
except OSError:
    pass
s.bind("/tmp/socketname")
s.listen(1)
conn, addr = s.accept()
    

def thread2():
    global worm
    print("hi t2")
    
    while 1:
        data = conn.recv(1024)
        if data: 
            data = data.decode()
            if data=="banana":
                continue
            else:
                if "up" in data:
                    if worm.direction != 3:
                        worm.direction=4
                        print("ylös")
                elif "down" in data:
                    if worm.direction != 4:
                        worm.direction=3
                        print("alas")
                elif "right" in data:
                    if worm.direction != 2:
                        worm.direction=1
                        print("oikea")
                elif "left" in data:
                    if worm.direction != 1:
                        worm.direction = 2
                        print("vasen")
                else:
                    #worm.direction = randint(1,4)
                    print(data)


thread2 = Thread( target=thread2, args=() )

thread2.start()

print("th1")
while 1:
        time.sleep(0.008)
        worm.draw()
        tk.update_idletasks()
        tk.update()
