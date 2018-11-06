#!/usr/bin/env python3
import pygame
from mutagen.mp3 import MP3
from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter import ttk

# TODO: make proper stop functionality (atm it works but it's not cleanly done)

class App(object):

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        pygame.init()

        pygame.mixer.init()
        self.root = Tk()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('mp3 player')
        self.parent_path = ""
        self.track_list = []
        self.current_song = 0
        self.song_text = ""
        self.song_length = 0

        self.frm = ttk.Frame(self.root)
        self.frm.pack(anchor=N)

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

        self.frame_slider = Frame(self.root)
        self.song_label = Label(self.frame_slider, text="")
        self.song_label.pack(side=RIGHT, padx=5)
        self.scale = ttk.Scale(self.frame_slider, orient=HORIZONTAL, length=250, from_=1, to=100)
        self.frame_slider.pack(anchor=NW)
        self.scale.pack(side=LEFT, padx=5, pady=5)

        self.frame_listbox = Frame(self.root)
        self.listbox = Listbox(self.frame_listbox, background="WHITE")
        self.listbox.bind('<Double-Button-1>', self.list_click)
        self.scroll = ttk.Scrollbar(self.frame_listbox, orient="vertical", command=self.listbox.yview)

        self.listbox.configure(yscrollcommand=self.scroll.set)
        self.frame_listbox.pack(expand=True, fill=BOTH)
        self.listbox.pack(side="left", expand=True, fill=BOTH )
        self.scroll.pack(side="left", fill=Y)

    def play(self, trackn=None):
        song_end = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(song_end)
        for event in pygame.event.get():
            if event.type == song_end:
                if not self.current_song >= len(self.track_list):
                    self.scale.set(0)
                    self.current_song += 1

        if len(list(self.listbox.get(0, END))) > 0:  # if we have a list of song
            if not self.listbox.curselection():  # if no song is selected in the list
                self.listbox.selection_set(0, 0)  # set selection to first file

            if trackn is not None:
                if not trackn < 0 and not trackn >= len(self.track_list):
                    pygame.mixer.music.stop()
                    self.current_song = trackn

            if not self.current_song >= len(self.track_list):
                if not pygame.mixer.music.get_busy():
                    self.listbox.selection_clear(0, END)
                    self.listbox.selection_set(self.current_song, self.current_song)
                    # add back path to filename when loading a song
                    file = self.parent_path + "/" + self.track_list[self.current_song]
                    self.song_length = int(MP3(file).info.length)
                    songlength = self.song_length
                    self.scale.config(to=songlength)
                    # self.song_label["text"] =  audio.info.length # round((audio.info.length/60), 2)
                    pygame.mixer.music.load(self.parent_path + "/" + self.track_list[self.current_song])
                    pygame.mixer.music.play()
                else:
                    elapsed_seconds = int((pygame.mixer.music.get_pos()/1000))
                    self.scale.set(elapsed_seconds)
                    time_left_seconds = (self.song_length - elapsed_seconds)
                    minutes = time_left_seconds // 60
                    seconds = time_left_seconds % 60
                    final_time = str(minutes), ":", str(seconds).rjust(2, '0')
                    self.song_label["text"] = final_time
                    # self.scale.set()
                    # (pygame.mixer.music.get_pos()/1000)%60

        self.root.after(1000, self.play)

    def back(self):
        current = self.listbox.curselection()
        prev_track = current[0] - 1
        self.play(trackn=prev_track)

    def next(self):
        current = self.listbox.curselection()
        next_track = current[0] + 1
        self.play(trackn=next_track)

    def stop(self):
        pygame.mixer.music.stop()
        self.current_song = len(self.track_list)  # not sure if this is the correct way but it works

    def add(self):
        if self.parent_path:
            self.frm.filename = askopenfilenames(initialdir=self.parent_path)
        else:
            self.frm.filename = askopenfilenames(initialdir="~")

        if self.frm.filename:
            self.parent_path = self.frm.filename[0].rsplit('/', 1)[0]  # remember last visited dir

        for index, item in list(enumerate(self.frm.filename)):
            # don't show path in listbox  --> .replace(path, "")
            self.listbox.insert(END, self.frm.filename[index].replace(self.parent_path + "/", ""))

        self.track_list = list(self.listbox.get(0, END))  # get list of song

    def rem(self):
        current = self.listbox.curselection()
        self.listbox.delete(current)

    def clear(self):
        self.listbox.delete(0, END)

    def list_click(self, event):
        current = self.listbox.curselection()
        self.play(trackn=current[0])


app = App()
app.root.after(1000, app.play)
app.root.mainloop()
