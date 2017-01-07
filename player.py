#!/usr/bin/env python3
import pygame
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import os
import inspect

class App(object):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.root = tkinter.Tk()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('mp3 player')

        self.frm = ttk.Frame(self.root)
        self.frm.grid(column=0, row=0, sticky='nsew')

        self.im_play=PhotoImage(file="images/play.png")
        self.im_stop=PhotoImage(file="images/stop.png")
        self.im_add=PhotoImage(file="images/add.png")
        self.im_rem=PhotoImage(file="images/del.png")
        self.im_clr=PhotoImage(file="images/clear.png")

        button_make = ttk.Button(self.frm, text='Play')
        button_make.config(image=self.im_play)
        button_make['command'] = self.play
        button_make.grid(column=2, row = 1, sticky=N)

        button_stop = ttk.Button(self.frm, text='Stop')
        button_stop.config(image=self.im_stop)
        button_stop['command'] = self.stop
        button_stop.grid(column=3, row = 1, sticky=N)

        button_add = ttk.Button(self.frm, text='Add')
        button_add.config(image=self.im_add)
        button_add['command'] = self.add
        button_add.grid(column=4, row = 1, sticky=N)

        button_del = ttk.Button(self.frm, text='Del')
        button_del.config(image=self.im_rem)
        button_del['command'] = self.rem
        button_del.grid(column=5, row = 1, sticky=N)

        button_clr = ttk.Button(self.frm, text='clear')
        button_clr.config(image=self.im_clr)
        button_clr['command'] = self.clear
        button_clr.grid(column=6, row = 1, sticky=N)

        self.listbox = Listbox(self.frm)
        self.listbox.grid(column=1, row = 3, columnspan=6, sticky='we')

        for child in self.frm.winfo_children(): child.grid_configure(padx=5, pady=5)
        
    def play(self):
        for idx, item in enumerate(self.listbox.get(0, END)):
            print(item) 
            pygame.mixer.music.load(str("\""+item+"\""))
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def add(self):
        self.frm.filename = askopenfilename(initialdir = "~")
        self.listbox.insert(END, self.frm.filename)

    def rem(self):
        pass

    def clear(self):
        pass

app = App()
app.root.mainloop()
