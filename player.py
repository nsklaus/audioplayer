#!/usr/bin/env python3
import pygame
from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter import ttk

# TODO: remember last visited folder in filedialog
# TODO: make the player to automatically go to the next song
# TODO: make double click on a song to start playing

class App(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()

        pygame.mixer.init()
        self.root = Tk()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('mp3 player')
        # self.root.grid_columnconfigure(1, weight=1)
        # self.root.grid_rowconfigure(2, weight=1)

        gui_style = ttk.Style()
        gui_style.configure('My.TFrame', background='#334353')
        self.frm = ttk.Frame(self.root, style='My.TFrame')
        self.frm.pack(anchor=N)
        # self.frm.grid(column=0, row=0, sticky='news')

        self.current_song = 0

        self.im_back = PhotoImage(file="images/back.png")
        self.im_play = PhotoImage(file="images/play.png")
        self.im_next = PhotoImage(file="images/next.png")
        self.im_stop = PhotoImage(file="images/stop.png")
        self.im_add = PhotoImage(file="images/add.png")
        self.im_rem = PhotoImage(file="images/del.png")
        self.im_clr = PhotoImage(file="images/clear.png")

        button_back = ttk.Button(self.frm)
        button_back.config(image=self.im_back)
        button_back['command'] = self.back
        button_back.pack(side=LEFT)

        button_play = ttk.Button(self.frm)
        button_play.config(image=self.im_play)
        button_play['command'] = self.play
        button_play.pack(side=LEFT)

        button_next = ttk.Button(self.frm)
        button_next.config(image=self.im_next)
        button_next['command'] = self.next
        button_next.pack(side=LEFT)

        button_stop = ttk.Button(self.frm)
        button_stop.config(image=self.im_stop)
        button_stop['command'] = self.stop
        button_stop.pack(side=LEFT)

        button_add = ttk.Button(self.frm)
        button_add.config(image=self.im_add)
        button_add['command'] = self.add
        button_add.pack(side=LEFT)

        button_del = ttk.Button(self.frm)
        button_del.config(image=self.im_rem)
        button_del['command'] = self.rem
        button_del.pack(side=LEFT)

        button_clr = ttk.Button(self.frm)
        button_clr.config(image=self.im_clr)
        button_clr['command'] = self.clear
        button_clr.pack(side=LEFT)

        self.listbox = Listbox(self.root)
        self.listbox.pack(fill=BOTH, expand=YES)


    def back(self):
        current = self.listbox.curselection()
        prev = current[0] - 1
        self.play(trackn=prev)
        pass

    def play(self, trackn=None):
        if not trackn:
            print("trackn is null")
            my_string = self.listbox.get(0)
            self.listbox.selection_clear(0, END)
            self.listbox.selection_set(0, 0)
            pygame.mixer.music.load(my_string)
        else:
            print("trackn is not null")
            my_string = self.listbox.get(trackn)
            self.listbox.selection_clear(0, END)
            self.listbox.selection_set(trackn, trackn)
            pygame.mixer.music.load(my_string)

        pygame.mixer.music.play()

    def next(self):
        current = self.listbox.curselection()
        prev = current[0] + 1
        self.play(trackn=prev)

    def stop(self):
        pygame.mixer.music.stop()

    def add(self):
        self.frm.filename = askopenfilenames(initialdir="~")
        self.listbox.insert(END, self.frm.filename)

    def rem(self):
        current = self.listbox.curselection()

        pass

    def clear(self):
        pass

app = App()
app.root.mainloop()
