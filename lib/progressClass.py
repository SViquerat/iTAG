import os, glob, sqlite3
import pickle
import datetime
import gc
import getopt
from tkinter import *
from PIL import Image, ImageOps, ImageDraw, ImageTk, ImageFont
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
import csv
from tkinter import messagebox, ttk,simpledialog
from platform import architecture


class Progress(Toplevel):
    def __init__(self, parent, PARAMETERDICT, dump=False):
        self.GLOBALS = PARAMETERDICT[0]
        self.TRANSLATION = PARAMETERDICT[1]
        Toplevel.__init__(self, parent)
        self.RELIEF = "raised"
        self.parent = parent
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        if not dump:
            self.img = Image.open(os.path.join(self.GLOBALS['RESPATH'], "processing_" + self.GLOBALS['LANGUAGE'] + ".TkT"))
        else:
            self.img = Image.open(os.path.join(self.GLOBALS['RESPATH'], "dumping.TkT"))
        x = self.img.size[0]
        y = self.img.size[1]
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        xpos = w / 2 - x / 2
        ypos = h / 2 - y / 2
        # self.geometry('%dx%d+%d+%d' % (xpos, ypos, x, y+40))
        # self.geometry(str(x) + "x" + str(y+40) +"+"+str(xpos)+"+"+str(ypos))
        # self.geometry(str(x) + "x" + str(y+40))

        self.resizable(0, 0)
        self.overrideredirect(True)
        self.img = ImageTk.PhotoImage(self.img)

        self.cFrame = Frame(self, bd=2, relief=SUNKEN, width=x, height=y)
        self.cFrame.grid_rowconfigure(0, weight=1)
        self.cFrame.grid_columnconfigure(0, weight=1)
        self.canvas = Canvas(self.cFrame, bd=0, width=x, height=y)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.pack(fill=BOTH)
        self.cFrame.pack(fill=BOTH)

        self.Progress = Frame(self, bd=2, relief=SUNKEN, height=40)
        self.pb = ttk.Progressbar(self.Progress, mode='indeterminate', length=x - 200)
        self.pbLabel = Label(self.Progress, text=self.TRANSLATION['PROGRESS_TEXT'], width=10, font=self.GLOBALS['LABELFONT'])
        self.pbLabel.grid(column=0, row=0)
        self.pb.grid(column=1, row=0)
        self.Progress.pack(fill=X, expand=1)
        self.update()

    def DONE(self):
        self.destroy()

    def STEP(self):
        self.pb.step()
        self.update()