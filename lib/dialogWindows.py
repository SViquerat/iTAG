# -*- coding: UTF-8 -*-
# this is wip to bring up to python 3.5
# csv export and buttons are wrong, amongst other things
import os
from tkinter import *
from PIL import Image, ImageTk
from lib import globalFunctions
from lib import smartObjects


class OKCANCEL(Toplevel):  # ok / cancel dialog
    def __init__(self, parent, PARAMETERDICT, mtext, ICON='info', dim=62):
        self.GLOBALS = PARAMETERDICT[0]
        self.TRANSLATION = PARAMETERDICT[1]
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._NULL)  # we need to include a check again...

        self.resizable(0, 0)
        self.iconbitmap(self.GLOBALS['ICONPATH'])
        # self.transient(self.parent)
        self.attributes('-topmost', True)

        fname = os.path.join(self.GLOBALS['RESPATH'], 'Icons', ICON + '.png')
        img = Image.open(fname).resize((dim, dim), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        BG = globalFunctions.lightgrey
        BG2 = globalFunctions.white

        mainWindow = Frame(self, bg=BG)
        tFrame = Frame(mainWindow, bg=BG2)
        tCanvas = Canvas(tFrame, width=dim, height=dim, highlightthickness=0, bg=BG2)
        tCanvas.create_image(0, 0, image=img, anchor="nw")
        tLabel = Label(tFrame, text=mtext, height=3, bg=BG2, bd=10, font=self.GLOBALS['LABELFONT'])
        tCanvas.pack(side='left')
        tLabel.pack(side='right')
        tFrame.grid(row=0, column=0)

        bFrame = Frame(mainWindow, bg=BG, bd=5)
        bOK = Button(bFrame, bd=1, text=self.TRANSLATION['BTN_OK'], command=self._OK, bg=BG, font=self.GLOBALS['BUTTONFONT'])
        bCANCEL = Button(bFrame, bd=1, text=self.TRANSLATION['BTN_CANCEL'], command=self._CANCEL, bg=BG, font=self.GLOBALS['BUTTONFONT'])
        bOK.pack(side='left')
        bCANCEL.pack(side='right')
        bFrame.grid(row=1, column=0, sticky=E)
        mainWindow.pack()
        self.wait_window(self)

    def _OK(self, Event=None):
        self.result = True
        self.destroy()

    def _CANCEL(self, Event=None):
        self.result = False
        self.destroy()

    def _NULL(self):
        pass

class WARNING(Toplevel):  # ok only dialog

    def __init__(self, parent, PARAMETERDICT, wtext, ICON='warning', dim=62, supress=False):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.GLOBALS = PARAMETERDICT[0]
        self.TRANSLATION = PARAMETERDICT[1]
        # self.grab_set()
        # self.initial_focus = self
        # self.initial_focus.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._NULL)  # we need to include a check again...
        # self.geometry("+"+str(self.winfo_screenwidth()/4)+"+"+str(self.winfo_screenheight()/4))
        self.resizable(0, 0)
        self.title(self.GLOBALS['TRANSLATION']['WARNING_TITLE'])
        self.iconbitmap(self.GLOBALS['ICONPATH'])
        self.attributes('-topmost', True)
        self.transient()
        self.noWARN = False

        fname = os.path.join(self.GLOBALS['RESPATH'], 'Icons', ICON + '.png')
        img = Image.open(fname).resize((dim, dim), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        BG = globalFunctions.lightgrey  # lower color
        BG2 = globalFunctions.white  # messagebox color

        mainWindow = Frame(self, bg=BG)
        tFrame = Frame(mainWindow, bg=BG2)
        tCanvas = Canvas(tFrame, width=dim, bg=BG2, height=dim, highlightthickness=0)
        tCanvas.create_image(0, 0, image=img, anchor="nw")
        tLabel = Label(tFrame, text=wtext, bg=BG2, height=3, font=self.GLOBALS['LABELFONT'], bd=10)
        tCanvas.pack(side='left')
        tLabel.pack(side='right')
        tFrame.grid(row=0, column=0)

        bFrame = Frame(mainWindow, bg=BG, bd=5)
        bOK = Button(bFrame, bd=1, text=self.GLOBALS['TRANSLATION']['BTN_OK'], command=self._DONE, bg=BG, font=self.GLOBALS['BUTTONFONT'])
        bOK.pack(side='left')
        if supress:
            nowarn = IntVar()
            bsup = Checkbutton(bFrame, bd=1, text=self.GLOBALS['TRANSLATION']['OVERLAP_SUPRESS'],
                               variable=nowarn, bg=BG, font=self.GLOBALS['SMALLBUTTONFONT'], command=self._switchWARN)
            bsup.pack(side='left')
        bFrame.grid(row=1, column=0, sticky=E)
        mainWindow.pack()
        self.wait_window(self)

    def _DONE(self, Event=None):
        self.destroy()

    def _switchWARN(self, Event=None):
        self.noWARN = not self.noWARN

    def _NULL(self):
        pass

class OutputOptions(Toplevel):  # Output Options dialog before processing stage
    def __init__(self, parent, PARAMETERDICT, columns, rows, dump=False, valid_gps=1):
        self.GLOBALS = PARAMETERDICT[0]
        self.TRANSLATION = PARAMETERDICT[1]
        self.parent = parent
        self.rows = rows
        self.dump = dump
        self.columns = columns
        self.out = []

        #self.cols = []
        self.cols = [[0] * len(self.columns) for x in range(len(self.rows))]
        self.check = [[0] * len(self.columns) for x in range(len(self.rows))]
        self.IMG_OUT = BooleanVar()
        self.IMG_OUT.set(False)
        self.CSV_OUT = BooleanVar()
        self.CSV_OUT.set(True)
        self.KML_OUT = BooleanVar()
        self.KML_OUT.set(False)
        self.SQL_OUT = BooleanVar()
        self.SQL_OUT.set(False)
        self.CSV_SEP = StringVar()
        self.CSV_SEP.set(';')
        self.initUI()

    def initUI(self):
        Toplevel.__init__(self, self.parent)
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.attributes('-topmost', True)
        self.protocol("WM_DELETE_WINDOW", self._NULL)  # we need to include a check again...
        self.mainWindow = Frame(self)
        self.headFrame = Frame(self.mainWindow, bd=2, relief=FLAT)
        l = Label(self.headFrame, text=self.TRANSLATION['SES_OPT'], relief=FLAT)
        l.pack(fill=X, side=LEFT)
        self.headFrame.grid(row=0, column=0, sticky=E)

        ### confirm button frame
        self.bFrame = Frame(self.mainWindow, bd=2, relief=FLAT)
        self.bContinue = Button(self.bFrame, text='Process Data', command=self.Confirm, anchor=E)
        self.bContinue.pack(side=RIGHT)
        self.bFrame.grid(row=3, column=0)
        self.mainWindow.pack(fill=BOTH, expand=1)

        ### columns selector frame
        self.colFrame = Frame(self.mainWindow, bd=2, relief=RAISED)
        for i in range(0, len(self.rows)):
            l = Label(self.colFrame, text=self.rows[i], anchor="center", relief=GROOVE)
            l.grid(row=i + 1, column=0, sticky=W + E)
            for j in range(0, len(self.columns)):
                self.check[i][j] = Checkbutton(self.colFrame, bd=1, command=lambda i=i, j=j: self.toggle(i, j),
                                               relief=GROOVE)
                self.check[i][j].invoke()  # makes them selected, fills self.cols
                self.check[i][j].grid(row=i + 1, column=j + 1, sticky=W + E)
        self.b = []
        for j in range(0, len(self.columns)):  # column labels
            self.b.append(Button(self.colFrame, text=self.columns[j], anchor="center", relief=SUNKEN,
                                 command=lambda j=j: self.toggle_column(j)))
            self.b[j].grid(row=0, column=j + 1, sticky=W + E)
        self.colFrame.grid(row=1, column=0, sticky=E)

        self.outFrame = Frame(self.mainWindow, bd=2, relief=RAISED)
        Label(self.outFrame, text='process Images: ', relief=FLAT).grid(row=0, column=0)
        checkImage = Checkbutton(self.outFrame, bd=1, variable=self.IMG_OUT, onvalue=True, offvalue=False, relief=FLAT)
        checkImage.grid(row=0, column=1)
        Label(self.outFrame, text='create CSV files: ', relief=FLAT).grid(row=1, column=0)
        checkCSV = Checkbutton(self.outFrame, bd=1, variable=self.CSV_OUT, onvalue=True, offvalue=False, relief=FLAT)
        checkCSV.grid(row=1, column=1)
        Label(self.outFrame, text='CSV Separator: ', relief=FLAT).grid(row=1, column=2)
        self.e_CSV_sep = OptionMenu(self.outFrame, self.CSV_SEP, ";", "\\t", ",")
        self.e_CSV_sep.grid(row=1, column=3)
        Label(self.outFrame, text='create GoogleEarth KML file: ', relief=FLAT).grid(row=2, column=0)
        checkKML = Checkbutton(self.outFrame, bd=1, variable=self.KML_OUT, onvalue=True, offvalue=False, relief=FLAT)
        checkKML.grid(row=2, column=1)
        Label(self.outFrame, text='create SQL file: ', relief=FLAT).grid(row=3, column=0)
        checkSQL = Checkbutton(self.outFrame, bd=1, variable=self.SQL_OUT, onvalue=True, offvalue=False, relief=FLAT,
                               state=DISABLED)
        checkSQL.grid(row=3, column=1)
        self.outFrame.grid(row=2, column=0, sticky=E)

        ### any other output options??

        if self.dump:
            self.IMG_OUT.set(False)
            self.SQL_OUT.set(False)
            self.KML_OUT.set(False)
            checkImage.config(state=DISABLED)
            checkKML.config(state=DISABLED)
            checkSQL.config(state=DISABLED)

        ### set min / max window size
        self.resizable(0, 0)

    def toggle_column(self, j):
        status = self.b[j].configure('relief')[4]
        if status == 'sunken':
            for i in range(0, len(self.rows)):
                self.toggle(i, j, set_value=0)
                self.check[i][j].deselect()
            self.b[j].configure(relief=RAISED)
            self.update()
        else:
            print('raised')
            for i in range(0, len(self.rows)):
                self.toggle(i, j, set_value=1)
                self.check[i][j].select()
            self.b[j].configure(relief=SUNKEN)

    def toggle(self, i, j, set_value=None):
        if set_value == None:
            if self.cols[i][j] == 0:
                self.cols[i][j] = self.columns[j] + ' ' + self.rows[i]
            else:
                self.cols[i][j] = 0
        elif set_value == 0:
            self.cols[i][j] = 0
        else:
            self.cols[i][j] = self.columns[j] + ' ' + self.rows[i]

    def Confirm(self):
        self.out = [x for x in self.out if x != 0]  # remove all elements that are not 0's
        self.out_clean = [re.sub('[:*.!,;\s]', '_', x) for x in self.out]  # remove evil characters
        self.out_IMG = self.IMG_OUT.get()
        self.out_CSV = self.CSV_OUT.get()
        self.out_KML = self.KML_OUT.get()
        self.out_SQL = self.SQL_OUT.get()
        if self.CSV_SEP.get() == '\\t': self.CSV_SEP.set('\t')
        self.out_CSV_SEP = self.CSV_SEP.get()
        self.destroy()

    def _NULL(self):
        pass

class ButtonFrame(Toplevel): #idea: allow user to set predefined columns per image?

    def __init__(self, cookie):#, wtext, supress=False):
        Toplevel.__init__(self)
        self.GLOBALS = cookie
        self.protocol("WM_DELETE_WINDOW", self._DONE)  # we need to include a check again...
        self.resizable(0, 0)
        self.title('ToolBox')
        self.attributes('-topmost', True)
        self.attributes('-toolwindow', True)
        self.transient()
        self.buttons = []

        mainWindow = Frame(self)
        Label(mainWindow, text='Username: {0}'.format(self.GLOBALS['user'])).pack(side=TOP, fill=X, anchor=W)
        bFrame = Frame(mainWindow, bd=5)
        for i in range(0,20):
            bg = '#000000'
            catname = 'Not defined{0}'.format(str(i))
            if i < len(self.GLOBALS['catnames']):
                bg = self.GLOBALS['colours'][i]
                catname = self.GLOBALS['catnames'][i]
            b = smartObjects.catButton(i, bFrame, bd=3, width=20, text = catname, bg = bg)
            self.buttons.append(b)
            COL = 1
            if i % 2 == 0:
                COL = 0
            b.grid( row = int(i/2), column=COL, padx=1, pady=1)
        bFrame.pack(side=TOP,fill=X)
        Label(mainWindow,text='Image Options').pack(side=TOP,fill=X,anchor=W)

        toolFrame = Frame(mainWindow, bd=5,relief=FLAT)
        for i in range(0,len(self.GLOBALS['params'])): #this should actually be shortened to what actually is inside (pop empties)
            l = self.GLOBALS['params'][i]
            Label(toolFrame,text=l+': ').grid(row=i+1,column=0)
            Entry(toolFrame,text='Default').grid(row=i+1,column=1)
        toolFrame.pack(side=BOTTOM,anchor=W,fill=BOTH)
        mainWindow.pack()

    def activate(self, index):
        print(index)
        for i in range(0,len(self.buttons)):
            self.buttons[i].configure(relief=RAISED)
        self.buttons[index].configure(relief=SUNKEN)

    def _DONE(self, Event=None):
        print('emitting shutdown request')
        self.event_generate('<<RequestShutdown>>')

    def _NULL(self):
        pass
