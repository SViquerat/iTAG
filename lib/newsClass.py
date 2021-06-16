import os, glob, sqlite3
import pickle
import datetime
import gc
import getopt
from tkinter import *
from PIL import Image, ImageOps, ImageDraw, ImageTk, ImageFont
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
import csv
from tkinter import messagebox, ttk, simpledialog
from platform import architecture


class News(Toplevel):  # change layout, looks ugly! #maybe add options for templates / saving settings?
    def __init__(self, parent, GLOBALS):
        Toplevel.__init__(self, parent)
        self.resizable(0, 0)
        self.RELIEF = "raised"
        self.transient(parent)
        self.parent = parent
        self.body = Frame(self)
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.bind("<F1>", self.DONE)
        self.bind("<Escape>", self.DONE)
        self.title(GLOBALS['LONGVERSION'] + "! Help Page")
        self.iconbitmap(GLOBALS['ICONPATH'])

        MSGtext = GLOBALS['LONGVERSION'] + "\n\n"
        basename = os.path.dirname(sys.argv[0])
        helpname = os.path.join(GLOBALS['HELPFILE'])
        with open(helpname, 'rU') as f:
            for line in f:
                MSGtext = MSGtext + line
        MSGtext = MSGtext + GLOBALS['ABOUTTEXT']
        yscroll = Scrollbar(self.body, orient=VERTICAL)
        yscroll.grid(row=0, column=1, sticky=N + S)
        NEWS = Text(self.body, bg="#FFFFFD", fg="#5766EA", wrap=WORD, font=GLOBALS['HELPFONT'],
                    yscrollcommand=yscroll.set)
        NEWS.insert(INSERT, MSGtext)
        NEWS.config(state=NORMAL)
        NEWS.grid(row=0, column=0)
        yscroll.config(command=NEWS.yview)
        self.body.pack()
        self.wait_window(self)

    def DONE(self, event=None):
        self.destroy()
