# -*- coding: UTF-8 -*-
# this is wip to bring up to python 3.5
# csv export and buttons are wrong, amongst other things
import simplekml
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
# user files
from lib.wizClass import *
from lib import newsClass, progressClass
from lib.panelDialogClass import *
from lib.dialogWindows import *
from lib.imageProc import *
from lib.SQLiteHandler import *
import lib.globalFunctions


class iTag(Frame):

    def cookie_create(self): #this should be combined in GLOBALS!!!
        names = ["catcounter", "catnames", "modnames", "user", "params", "colours", "basename", "dirList", "newdir",
                 "tagsize", "Sitems", "ID", "current_cat", "currentSpec", "currentSpecIndex", "scale", "cextent",
                 "version", 'dbFile']
        cookie = {}
        for key in names:
            cookie[key] = None
        cookie['version'] = self.GLOBALS['VERSIONSTRING']
        cookie['full_version_string'] = self.GLOBALS['LONGVERSION']
        cookie['ARCH'] = self.GLOBALS['ARCH']
        cookie['OS'] = self.GLOBALS['OS']
        cookie['maxsize'] = self.GLOBALS['MAXSIZE']
        cookie['panel_canvas_size'] = 500
        cookie['file_scale'] = 1
        cookie['zoom_scale'] = 1
        cookie['current_group_ID'] = 1
        return cookie

    def cookie_update(self, dict2):
        for key in dict2.keys():
            self.cookie[key] = dict2[key]

    def __init__(self, parent, PARAMETERDICT):
        gc.enable()
        self.PARAMETER = PARAMETERDICT
        self.GLOBALS = self.PARAMETER[0]
        self.TRANSLATION = self.PARAMETER[1]

        self.LANGUAGE = self.GLOBALS['LANGUAGE']  # maybe replace throughout doc
        self.user = StringVar()  # later to be set by User during new session setup
        self.enable = False  # This will later enable all the controls
        self.i = 1  # it's always good to have it!
        self.item = 0  # item identifier for the canvas method
        self.ID = 0  # unique object identifier, needed for tag_remove_entry
        self.spec_index = 0  # legend item index
        self.cat = 0  # starting category (def 0 as empty)
        self.basename = os.getcwd()  # os.path.dirname(sys.argv[0])
        # firstscreen = 'itag_splash.TkT'  # Fyeah
        self.fullname = os.path.join(self.GLOBALS['RESPATH'], 'itag_splash.TkT')
        self.fname = os.path.split(self.fullname)[1]  # get filename
        self.img = Image.open(self.fullname)
        self.cImage = ImageTk.PhotoImage(self.img)  # open the first image!
        self.suffix = '*.jpg'  # we are looking for jpg's, maybe later set by user?
        self.parent = parent  # obviously...

        self.zoomcycle = 0  # starting zoomcycle
        self.FX = None  # no fx on magnifier
        self.zimg_id = None  # no zoom image to load
        self.magnifier = False  # no magnifier mode
        self.noWarnings = False
        self.tag_remove_entrymode = False
        # self.tagsize=6 #default tagsize

        # dynamic variables
        self.currentSpec = StringVar()  # dynamic,holds the name of currently selected species
        self.currentMod = StringVar()  # dynamic,holds the name of currently selected species
        self.currentFilePos = IntVar()  # this is self.i
        self.currentFilePos.set(0)
        self.currentFilePosHR = StringVar()  # this is self.i
        self.currentFilePosHR.set('0')
        self.currentFilename = StringVar()  # this holds self.fullname
        self.currentGroupID = IntVar()
        self.currentGroupID.set(1)
        self.showGroupIDS = BooleanVar()
        self.showGroupIDS.set(False)
        self.Sitems = IntVar()  # count of all objects
        self.Sitems.set(0)
        self.tags_hidden = BooleanVar()
        self.tags_hidden.set(False)
        self.pop = BooleanVar()  # no popup visible
        self.pop.set(False)
        self.skip_files_flag = BooleanVar()  # should we skip files the user has marked as such?
        self.skip_files_flag.set(False)
        self.hide_skip_files = BooleanVar()  # should we skip files the user has marked as such?
        self.hide_skip_files.set(False)
        self.magnifier_visible = BooleanVar()  # should we skip files the user has marked as such?
        self.magnifier_visible.set(False)
        self.global_zoom_var = IntVar()
        self.global_zoom_var.set(100)
        self.full_screen = BooleanVar()
        self.full_screen.set(False)
        self.cookie = self.cookie_create()  # initialize self.cookie with default values
        self.initUI()

    def initUI(self):
        Frame.__init__(self, self.parent)
        self.parent.title(self.GLOBALS['TITLE'])
        self.parent.geometry(str(self.img.size[0]) + "x" + str(self.img.size[1]))
        self.parent.minsize(self.img.size[0], self.img.size[1])
        self.mainWindow = Frame(self.parent)

        self.menubar = Menu(self.parent)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Session (Ctrl-N)", command=self.session_newWiz, state=NORMAL)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save Session (Ctrl-S)", command=self.session_save, state=DISABLED)
        self.filemenu.add_command(label="Resume Session (Ctrl-O)", command=self.session_load, state=NORMAL)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit (Ctrl-Q)", command=self.session_end)

        self.viewmenu = Menu(self.menubar, tearoff=0)
        self.viewmenu.add_checkbutton(label="Show General Panel (F9)", command=self.toggle_MultiPanel,
                                      variable=self.pop, onvalue=True, offvalue=False)
        self.viewmenu.add_checkbutton(label="Switch to full screen (F11)", command=self.toggle_fs,
                                      variable=self.full_screen, onvalue=True, offvalue=False)
        # self.viewmenu.add_checkbutton(label="Show group identifier on tags (F12)", command=self.redraw_tags,variable=self.showGroupIDS,onvalue = True,offvalue = False)
        self.viewmenu.add_checkbutton(label="Show group identifier on tags (F12)", command=self.toggle_group_ID_display,
                                      variable=self.showGroupIDS, onvalue=True, offvalue=False)

        self.optionmenu = Menu(self.menubar, tearoff=0)
        self.optionmenu.add_checkbutton(label="Hide all Tags (F8)", command=self.toggle_tags, variable=self.tags_hidden,
                                        onvalue=True, offvalue=False, foreground='red')
        # self.optionmenu.add_checkbutton(label="Do not show Images flagged with skip", variable=self.hide_skip_files,onvalue = True,offvalue = False,foreground='red') #not yet
        self.optionmenu.add_checkbutton(label="Supress Warnings", command=self.toggle_WARN, foreground='red')
        self.tagsizeMenu = Menu(self.optionmenu, tearoff=0)
        self.tagsizeMenu.add_command(label='increase tagsize (+)',
                                     command=lambda direction='+': self.set_tagsize(direction), foreground='red')
        self.tagsizeMenu.add_command(label='decrease tagsize (-)',
                                     command=lambda direction='-': self.set_tagsize(direction), foreground='red')
        self.groupIDMenu = Menu(self.optionmenu, tearoff=0)
        self.groupIDMenu.add_command(label='increase group counter (e or Up Arrow)', command=self.inc_groupID,
                                     foreground='red')
        self.groupIDMenu.add_command(label='decrease group counter (d or Down Arrow)', command=self.dec_groupID,
                                     foreground='red')
        self.optionmenu.add_cascade(label="Tag size", menu=self.tagsizeMenu)
        self.optionmenu.add_cascade(label="Group counter", menu=self.groupIDMenu)

        self.aboutmenu = Menu(self.menubar, tearoff=0)
        self.aboutmenu.add_command(label="iTAG Manual", command=lambda page='man': self.showPage(page))
        self.webLinks = Menu(self.aboutmenu, tearoff=0)
        self.webLinks.add_command(label="iTAG Homepage", command=lambda page='sf': self.showPage(page))
        self.webLinks.add_command(label="ITAW Büsum", command=lambda page='itaw_de': self.showPage(page))
        self.aboutmenu.add_cascade(label="Weblinks", menu=self.webLinks)
        self.aboutmenu.add_command(label="About", command=self.show_help)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="View", menu=self.viewmenu, state=DISABLED)
        self.menubar.add_cascade(label="Options", menu=self.optionmenu, state=DISABLED)
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)
        self.parent.config(menu=self.menubar)

        # Top Bar
        self.bar = Frame(self.mainWindow)

        self.tnav = Frame(self.bar)
        self.bFIRST = Button(self.tnav, text='<<', command=lambda INDX=-1: self.image_GOTO(INDX),
                             font=self.GLOBALS['BUTTONFONT'])
        self.bPREV = Button(self.tnav, text='<', command=self.prevImage, font=self.GLOBALS['BUTTONFONT'])
        self.tGOTO = Entry(self.tnav, width=4, textvariable=self.currentFilePosHR)
        self.bGOTO = Button(self.tnav, text=self.TRANSLATION['BTN_GOTO'], command=self.getGOTO,
                            font=self.GLOBALS['BUTTONFONT'])
        self.bNEXT = Button(self.tnav, text='>', command=self.nextImage, font=self.GLOBALS['BUTTONFONT'])
        self.bLAST = Button(self.tnav, text='>>', command=lambda INDX=0: self.image_GOTO(INDX),
                            font=self.GLOBALS['BUTTONFONT'])

        self.statusFrame = Frame(self.bar, bd=1, relief='flat')
        self.lC = Label(self.statusFrame, bd=1, anchor=W, width=8,
                        text=self.TRANSLATION['CATEGORY'] + ': ')  # category text
        self.lC.grid(row=0, column=0, sticky=W)
        self.modL = Label(self.statusFrame, bd=1, anchor=E, width=8, textvariable=self.currentMod, bg='#C0C0C0',
                          fg=globalFunctions.col_invert('#C0C0C0'))  # category text
        self.modL.grid(row=0, column=1, sticky=W)
        self.lCat = Label(self.statusFrame, bd=1, anchor=W, width=20, textvariable=self.currentSpec)
        self.lCat.grid(row=0, column=2, sticky=W)
        self.lG = Label(self.statusFrame, bd=1, anchor=E, text='Group: ')  # Groups text
        self.lG.grid(row=0, column=3, sticky=E)
        self.lGcount = Label(self.statusFrame, bd=1, anchor=E, textvariable=self.currentGroupID)  # Groups text
        self.lGcount.grid(row=0, column=4, sticky=E)
        self.lfname = Label(self.statusFrame, bd=1, anchor=E, text='')  # file counter
        self.lfname.grid(row=0, column=5, sticky=E)
        self.lCo = Label(self.statusFrame, bd=1, anchor=E,
                         text=self.TRANSLATION['STAT_OBJ'] + ': ')  # object text
        self.lCo.grid(row=0, column=6, sticky=E)
        self.lCount = Label(self.statusFrame, bd=1, anchor=E, textvariable=self.Sitems)  # object counter
        self.lCount.grid(row=0, column=7, sticky=E)

        self.bar.pack(side=TOP, fill=X, expand=1)

        # image canvas
        self.cFrame = Frame(self.mainWindow, bd=0, relief=FLAT)
        self.cFrame.grid_rowconfigure(0, weight=1)
        self.cFrame.grid_columnconfigure(0, weight=1)
        self.canvas = Canvas(self.cFrame, bd=0, relief=FLAT, width=self.img.size[0], height=self.img.size[1],
                             bg='black')
        self.canvas.create_image(0, 0, image=self.cImage, anchor="nw")
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.canvas.config(cursor='heart')
        # self.cFrame.pack(side=TOP,fill=BOTH,expand=1) #canvas and menu

        # lower frame
        self.f_lower = Frame(self.mainWindow)  # lower frame
        self.fcat = Frame(self.f_lower, bd=1)
        self.global_zoom = Frame(self.f_lower, bd=1, relief=GROOVE)
        self.image_flagging = Frame(self.f_lower, bd=1, relief='flat')
        # self.fcat.grid(row=0,column=0,sticky=W+E)
        # self.global_zoom.grid(row=0,column=1,sticky=E)
        # self.image_flagging.grid(row=0,column=2,sticky=E)
        self.fcat.pack(side=LEFT)
        self.global_zoom.pack(side=RIGHT)
        self.image_flagging.pack(side=RIGHT)
        self.f_lower.pack(side=BOTTOM, fill=X)
        self.cFrame.pack(side=BOTTOM, fill=BOTH, expand=1)  # canvas and menu

        self.mainWindow.pack(fill=BOTH, expand=0)

        self.parent.resizable(0, 0)  # prevents resizing of window
        self.parent.protocol("WM_DELETE_WINDOW", self.session_end)  # we need to include a check again...
        self.parent.iconbitmap(self.GLOBALS['ICONPATH'])

        # various keybindings
        self.parent.bind("<F1>", self.show_help)  # we need it...
        self.parent.bind("<Control-n>", self.session_newWiz)  # :D
        self.parent.bind("<Control-o>", self.session_load)  # :D
        self.parent.bind("<Control-q>", self.session_end)  # :D

    def showPage(self, page='sf'):  # more pages?
        import webbrowser
        if page == 'man':
            url = os.path.join(self.GLOBALS['PROGDIR'], "Manual", "iTAG User Manual.pdf")
            try:
                os.startfile(url)
            except:
                messagebox.showwarning("Warning",
                                       'No default pdf browser fround.\nYou can access the user manual at:\n' + url)
        else:
            if page == 'sf':
                url = 'http://sourceforge.net/projects/itagbiology/'
            elif page == 'itaw_de':
                url = 'http://www.tiho-hannover.de/kliniken-institute/institute/institut-fuer-terrestrische-und-aquatische-wildtierforschung/'
            try:
                webbrowser.open(url, new=0, autoraise=True)
            except:
                messagebox.showerror("Error", 'No default webbrowser found.\nYou can visit us at:\n' + url)

    def getGOTO(self):
        text = self.tGOTO.get()
        if (text.isdigit()):
            self.image_GOTO(INDX=text)
        else:
            self.tGOTO.delete(0, END)
            messagebox.showerror("Warning", self.TRANSLATION['NOT_A_NUMBER'] + ": " + text)

    def image_GOTO(self, INDX=1):
        text = int(INDX)
        if (text > len(self.cookie['dirList']) or text == 0):
            text = len(self.cookie['dirList']) - 1
        elif text == -1:
            text = 0
        self.currentFilePos.set(int(text))
        self.redraw()

    def toggle_WARN(self, event=None):  # change to booleanvar
        self.noWarnings = not self.noWarnings

    def toggle_magnifier(self, event=None):
        if self.enable:
            if self.magnifier:
                self.magnifier = False
                self.zoomcycle = 0
                self.magnifier_crop(event)
                self.Mode = False
                if self.GLOBALS['OS'] == "posix":
                    self.parent.unbind("<Button-4>")
                    self.parent.unbind("<Button-5>")
                else:
                    self.parent.unbind("<MouseWheel>")
                self.canvas.unbind("<Motion>")

                for i in ("<g>", "<h>", "<j>", "<k>", "<u>", "<s>"):
                    self.parent.unbind(str(i))
                if self.zimg_id:
                    self.canvas.delete(self.zimg_id)
                    self.canvas.delete(self.zimg_rect)
                    self.canvas.delete(self.zimg_rect2)
            else:
                self.magnifier = True
                self.zoomcycle = 1
                self.magnifier_crop(event)
                if self.GLOBALS['OS'] == "posix":  # unix systems
                    self.parent.bind("<Button-4>", self.zoomer)
                    self.parent.bind("<Button-5>", self.zoomer)
                else:  # mac and win systems
                    self.parent.bind("<MouseWheel>", self.zoomer)
                self.canvas.bind("<Motion>", self.magnifier_crop)
                for i in ("<g>", "<h>", "<j>", "<k>", "<l>", "<u>", "<s>"):
                    self.parent.bind(str(i), self.toggle_FX)

    def toggle_FX(self, event):
        if self.FX == event.char:
            self.FX = None
        else:
            self.FX = event.char
        self.magnifier_crop(event)

    def zoomer(self, event):
        if self.enable and self.magnifier:
            if (event.delta > 0 or event.num == 4):
                if self.zoomcycle < 11: self.zoomcycle += 1
            elif (event.delta < 0 or event.num == 5):
                if self.zoomcycle > 1: self.zoomcycle -= 1
            self.magnifier_crop(event)

    def magnifier_crop(self, event, mode=None):
        size = 300, 300  # maybe increase? maybe dynamic?
        zsize = int(size[0] / 2), int(size[1] / 2)
        if self.zimg_id:
            self.canvas.delete(self.zimg_id)
            self.canvas.delete(self.zimg_rect)
            self.canvas.delete(self.zimg_rect2)
            self.canvas.delete(self.mtext)
        if (self.zoomcycle) != 0:
            x, y = int(self.canvas.canvasx(0) + event.x), int(self.canvas.canvasy(0) + event.y)
            tmp = self.img.crop((x - int(zsize[0] / self.zoomcycle), y - int(zsize[1] / self.zoomcycle),
                                 x + int(zsize[0] / self.zoomcycle),
                                 y + int(zsize[1] / self.zoomcycle)))  # is that correct?
            tmp = tmp.resize(size)
            Mode = "normal"
            if self.FX != None:
                tmp = imgFilter(tmp, self.FX, self.TRANSLATION)
                Mode = tmp[1]
                tmp = tmp[0]
                # if self.FX == "k":  # kontrast...
                #     tmp = ImageOps.autocontrast(tmp)  # autocontrast version of 200x200 tmp...
                #     Mode = self.TRANSLATION['MODE_AUTO']
                # if self.FX == "h":
                #     tmp = ImageOps.equalize(tmp)  # hist equalized version of 200x200 tmp...
                #     Mode = self.TRANSLATION['MODE_EQH']
                # if self.FX == "j":
                #     tmp = ImageOps.invert(tmp)  # inverted version of 200x200 tmp...
                #     Mode = self.TRANSLATION['MODE_INV']
                # if self.FX == "g":
                #     tmp = ImageOps.solarize(tmp, 128)  # solarized version of 200x200 tmp...
                #     Mode = self.TRANSLATION['MODE_SOL']
                # if self.FX == "l":
                #     tmp = ImageOps.posterize(tmp, 2)  # solarized version of 200x200 tmp...
                #     Mode = self.TRANSLATION['MODE_POS']
                # if self.FX == 'u':  # unsharp mask
                #     from PIL import ImageFilter
                #     tmp = tmp.filter(ImageFilter.UnsharpMask)
                #     Mode = self.TRANSLATION['MODE_UNSHARP']
                # if self.FX == 's':  # smart sharpen
                #     from PIL import ImageFilter
                #     tmp = ImageOps.autocontrast(tmp)  # autocontrast version of 200x200 tmp...
                #     tmp1 = tmp.filter(ImageFilter.DETAIL)
                #     tmp2 = tmp.filter(ImageFilter.CONTOUR)
                #     tmp12 = Image.blend(tmp1, tmp2, .5)
                #     tmp3 = ImageOps.equalize(tmp12)
                #     tmp4 = tmp.filter(ImageFilter.UnsharpMask)
                #     tmp4 = tmp4.filter(ImageFilter.BLUR)
                #     tmp = Image.blend(tmp3, tmp4, .7)
                #     Mode = self.TRANSLATION['MODE_SMARTSHARP']
            self.zimg = ImageTk.PhotoImage(tmp)
            self.zimg_id = self.canvas.create_image(x, y, image=self.zimg, tags=("bg", 0, 'magnifier'))
            self.zimg_rect = self.canvas.create_rectangle(((x + zsize[0], y + zsize[1]), (x - zsize[0], y - zsize[1])),
                                                          outline="#808080", tags=("bg-mag", 0, 'magnifier'))
            self.zimg_rect2 = self.canvas.create_rectangle(
                ((x + zsize[0] + 1, y + zsize[1] + 1), (x - zsize[0] - 1, y - zsize[1] - 1)), outline="#FFFFFF",
                tags=("bg-mag", 0, 'magnifier'))
            self.mtext = self.canvas.create_text(self.canvas.canvasx(self.canvas.winfo_width() - 10),
                                                 self.canvas.canvasy(0), text=Mode, fill="#FFFFFF", anchor="ne",
                                                 font=self.GLOBALS['HELPFONT'])

    def toggle_tag_edit_mode(self, event=None):
        self.tags_locked = not self.tags_locked
        if not self.tags_locked:
            print("modifiying tags")
            self.canvas.tag_unbind('bg', "<Button 3>")  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Shift-Button 3>")  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Control-Button 3>")  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Alt-Button 3>")  # paint, save coordinates
            self.parent.unbind("w")  # grab and...
            self.parent.unbind("q")  # grab and...
            tags = self.canvas.find_withtag("tag")
            self.canvas.tag_bind('tag', "<ButtonPress-3>", self.tag_grab)  # grab and...
            self.canvas.tag_bind('tag', "<ButtonRelease-3>", self.tag_release)  # grab and...
        else:
            print("not modifiying tags")
            self.canvas.tag_bind('bg', "<Button 3>",
                                 lambda event, alt_i=0: self.tag_add_entry(event, alt_i))  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Shift-Button 3>",
                                 lambda event, alt_i=1: self.tag_add_entry(event, alt_i))  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Control-Button 3>",
                                 lambda event, alt_i=2: self.tag_add_entry(event, alt_i))  # paint, save coordinates
            self.canvas.tag_bind('bg', "<Alt-Button 3>",
                                 lambda event, alt_i=3: self.tag_add_entry(event, alt_i))  # paint, save coordinates
            self.parent.bind("w")  # grab and...
            self.parent.bind("q")  # grab and...
            self.canvas.tag_unbind('tag', "<ButtonPress-3>")  # grab and...
            self.canvas.tag_unbind('tag', "<ButtonRelease-3>")  # grab and...

    def tag_grab(self, event):
        item = self.canvas.find_closest(self.canvas.canvasx(0) + event.x,
                                        self.canvas.canvasy(0) + event.y)  # get item number
        cTAGS = self.canvas.gettags(item[0])
        self._tID = cTAGS[3]
        self.loc = 1
        event.widget.bind("<Motion>", self.tag_move)

    # def tag_move(self, event):
    #     import copy
    #     cnv = event.widget
    #     xy = cnv.canvasx(event.x), cnv.canvasy(event.y)
    #     points = event.widget.coords(CURRENT)
    #     anchors = copy.copy(points[:2])
    #     print(points)
    #     for idx in range(len(points)):
    #         mouse = xy[idx % 2]
    #         zone = anchors[idx % 2]
    #         points[idx] = points[idx] - zone + mouse
    #         print(points)
    #         apply(event.widget.coords, [CURRENT] + points)

    # def tag_release(self, event):
    #     event.widget.unbind("<Motion>")
    #     x, y = self.canvas.canvasx(0) + event.x, self.canvas.canvasy(0) + event.y
    #     sql = "select * from detailed where ID=" + self._tID
    #     for row in self.sqlite_conn.execute(sql):
    #         print(row)
    #     sql = "update detailed set xpos=" + str(x) + ",ypos=" + str(y) + " where ID =" + str(self._tID)
    #     self.sqlite_conn.execute(sql)
    #     self.sqlite_conn.commit()

    # def tag_drag(self, event=None):
    #     item = self.canvas.find_closest(self.canvas.canvasx(0) + event.x,
    #                                     self.canvas.canvasy(0) + event.y)  # get item number
    #     cTAGS = self.canvas.gettags(item[0])
    #     print(cTAGS)
    #     if cTAGS[0] == 'tag':
    #         self._tx, self._ty = self.canvas.coords(t)
    #         dify = self._ty - event.y
    #         difx = self._tx - event.x
    #         self.canvas.move(item[0], difx, dify)

    def toggle_fs(self, event=None):  # toggles between fullscreen on / off
        if event is not None:
            self.viewmenu.invoke(1)
        else:
            fs = self.full_screen.get()
            self.master.attributes("-fullscreen", fs)  # does not switch off!

    def toggle_group_ID_display(self, event=None):  # toggles between fullscreen on / off
        if self.tags_hidden.get():
            messagebox.showinfo("Info", 'While tags are hidden, groups will not be displayed')
            return
        else:
            if event is not None:
                self.viewmenu.invoke(2)  # show group ids on tags
            else:
                self.redraw_tags(size=self.tagsize)

    def toggle_MultiPanel(self, event=None):  # toggles MultiPanel on / off
        if event is not None:
            self.viewmenu.invoke(0)
        else:
            if self.pop.get():
                self.panel = MultiPanel(self, self.GLOBALS, cookie=self.cookie, gpsdict=self.IMAGEDATA,
                                        ptitle='iTAG General Panel', image=self.pImage)
                self.panel.Navi.canvas.tag_bind('panel_image', '<Button-1>', self.set_view)
            else:
                self.panel.Navi.canvas.tag_unbind('panel_image', '<Button-1>')
                self.panel.unbind('<Button-1>')  # is that neccesary?
                self.panel.destroy()

    def toggle_tags(self, event=None):
        if event is not None:
            self.optionmenu.invoke(0)
        if self.tags_hidden.get():
            self.canvas.itemconfigure('tag', state='hidden')
        else:
            self.canvas.itemconfigure('tag', state=NORMAL)

    def toggle_skip_files_flag(self):
        print(self.skip_files_flag.get())
        if self.skip_files_flag.get():
            sql = 'update files set skip_file=1 where filename = "%s"' % self.cookie['current_file']
            self.sqlite_conn.execute(sql)
        else:
            sql = 'update files set skip_file=0 where filename = "%s"' % self.cookie['current_file']
            self.sqlite_conn.execute(sql)

    def dataDUMP(self, filename, row):  # debug, optimize
        self.cookie['basename'] = str(os.path.dirname(filename))
        self.deactivate_all()
        self.user.set(self.user.get() + '_FAILDUMP')
        so = OutputOptions(self.mainWindow, self.PARAMETER, rows=self.cookie['catnames'],
                           columns=self.cookie['modnames'], dump=True)
        self.wait_window(so)  # will resume after so is destroyed
        try:
            newdir = os.path.normpath(self.cookie['basename'] + os.sep + self.user.get())
            fname = os.path.normpath(os.path.join(newdir, self.user.get()))
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            print(fname)
            self.sqlite_db_creation(fname=fname)
            conn = sqlite3.connect(fname)
        except:
            newdir = os.path.normpath(self.cookie['basename'] + os.sep + self.user.get())
            fname = os.path.normpath(os.path.join(newdir, self.user.get()))
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            self.sqlite_db_creation(fname=fname)
            conn = sqlite3.connect(fname)  # fallback connection
        # self.pb = self.Progress(self.mainWindow, dump=True)
        self.pb = progressClass.Progress(self.mainWindow, self.GLOBALS, dump=True)
        self.get_sqlite_from_row(row, conn=conn)
        self.sqlite_create_summary_table(conn=conn, so=so)
        try:
            self.save_output(connection=conn, so=so)
            self.pb.DONE()
            messagebox.showinfo("Info", 'Tag data succesfully dumped under: ' + fname + '\nOnly csv and sqlite export!')
        except:
            self.pb.DONE()
            messagebox.showwarning("Warning", 'some elements might not have been saved!')

    def deactivate_all(self):
        self.parent.withdraw()

    def show_help(self, event=None):
        newsClass.News(self.mainWindow, self.GLOBALS)

    def tag_paint_entry(self, x1, y1, alt_i, l_index, ID, size, col, group=0):
        objectID = 'object_ID: ' + str(ID)
        if alt_i == 0:
            self.canvas.create_oval((x1 - size), (y1 - size), (x1 + size), (y1 + size), fill=col,
                                    outline=globalFunctions.col_invert(col),
                                    tags=('tag', 'bg', l_index, ID, alt_i, objectID),
                                    activefill=globalFunctions.col_invert(col))
        elif alt_i == 1:
            self.canvas.create_rectangle((x1 - size), (y1 - size), (x1 + size), (y1 + size), fill=col,
                                         outline=globalFunctions.col_invert(col),
                                         tags=('tag', 'bg', l_index, ID, alt_i, objectID),
                                         activefill=globalFunctions.col_invert(col))
        elif (alt_i == 2):
            self.canvas.create_rectangle((x1 - size), (y1 - size), (x1 + size), (y1 + size), outline=col, width=4,
                                         tags=('tag', 'bg', l_index, ID, alt_i, objectID),
                                         activefill=globalFunctions.col_invert(col))
        elif alt_i == 3:
            self.canvas.create_rectangle(x1 - size * 2, y1 - size, x1 + size * 2, y1 + size, fill=col,
                                         outline=globalFunctions.col_invert(col),
                                         tags=('tag', 'bg', l_index, ID, alt_i, objectID),
                                         activefill=globalFunctions.col_invert(col))
        if self.showGroupIDS.get():
            font = "Verdana " + str(size)
            canvas_id = self.canvas.create_text(x1, y1, anchor="center",
                                                tags=('tag', 'bg', l_index, ID, alt_i, objectID),
                                                fill=globalFunctions.col_invert(col),
                                                font=font)
            self.canvas.itemconfig(canvas_id, text=group)

    def redraw_tags(self, size=3, override=False, use_file_tagsize=False):
        self.canvas.delete('tag')
        # self.canvas.delete('group')
        if self.Sitems.get() != 0:
            if use_file_tagsize:
                sql = "select filename,file_tagsize from files where filename = '%s'" % (self.fname.lower())
                for row in self.sqlite_conn.execute(sql):
                    size = row[1]
            sql = "select ID, xpos,ypos,category_index,modifier,species_index,group_ID,tagsize from detailed where filename = '%s'" % (
                self.fname)
            for row in self.sqlite_conn.execute(sql):
                ID, x1, y1, cat, alt_i, l_index, group, tagsize = row
                x1 *= (self.cookie['file_scale'] * self.cookie['zoom_scale'])
                y1 *= (self.cookie['file_scale'] * self.cookie['zoom_scale'])
                col = self.cookie['colours'][cat]
                if override:
                    size = tagsize
                self.tag_paint_entry(x1, y1, alt_i, l_index, ID, size, col, group)
            sql = "update files set file_tagsize =%s where filename = '%s'" % (size, self.fname.lower())
            self.sqlite_conn.execute(sql)
            self.sqlite_conn.commit()

    # def image_FX(self, img, FX=None):
    #     if FX == 0:
    #         return img
    #     elif FX == 1:
    #         return ImageOps.autocontrast(img)
    #     elif FX == 2:
    #         return ImageOps.invert(img)
    #     elif FX == 3:
    #         return ImageOps.equalize(img)  # hist equalized version of 200x200 tmp...
    #     elif FX == 4:
    #         return ImageOps.invert(img)  # inverted version of 200x200 tmp...
    #     elif FX == 5:
    #         return ImageOps.solarize(img, 128)  # solarized version of 200x200 tmp...
    #     elif FX == 6:
    #         return ImageOps.posterize(img, 2)  # solarized version of 200x200 tmp...
    #     elif FX == 7:  # unsharp mask
    #         from PIL import ImageFilter
    #         return img.filter(ImageFilter.UnsharpMask)
    #     elif FX == 8:  # smart sharpen
    #         from PIL import ImageFilter
    #         img = ImageOps.autocontrast(img)  # autocontrast version of 200x200 tmp...
    #         tmp1 = img.filter(ImageFilter.DETAIL)
    #         tmp2 = img.filter(ImageFilter.CONTOUR)
    #         tmp12 = Image.blend(tmp1, tmp2, .5)
    #         tmp3 = ImageOps.equalize(tmp12)
    #         tmp4 = img.filter(ImageFilter.UnsharpMask)
    #         tmp4 = tmp4.filter(ImageFilter.BLUR)
    #         return Image.blend(tmp3, tmp4, .7)

    def redraw(self, size=3):  # clean up
        # should deactivate all controls as long as its loading!
        self.fname = os.path.split(self.cookie['dirList'][self.currentFilePos.get()])[1]  # get filename
        self.IMAGEDATA = self.conn.getDataFromImage(self.fname)
        self.skip_files_flag.set(self.IMAGEDATA['skip_file'])

        if self.IMAGEDATA['skip_file'] == 1 and self.hide_skip_files.get():
            print('Will skip this file')
            return
        else:
            fullname = os.path.join(self.IMAGEDATA['basename'], self.IMAGEDATA['filename'])
            try:
                self.img = Image.open(fullname)
                orig_x, orig_y = self.img.size
                skip_image_badfile = False
            except:
                skip_image_badfile = True
            if skip_image_badfile:
                self.cookie['dirList'].pop(self.currentFilePos.get() - 1)
                self.conn.deleteFromFiles(self.IMAGEDATA['filename'])
                # self.currentFilePos.set(self.currentFilePos.get()-1)
                messagebox.showinfo("Info", self.TRANSLATION['REDRAW_WARN'] + " " + self.fullname)
                self.lfname.configure(
                    text=self.TRANSLATION['FILENAME'] + ": " + self.fname + " [" + str(
                        self.currentFilePosHR.get()) + os.path.sep + str(
                        len(self.cookie['dirList'])) + "]")  # new picture count
            else:
                if self.magnifier:
                    self.toggle_magnifier()
                self.tags_hidden.set(False)
                self.currentFilePosHR.set(str(self.currentFilePos.get() + 1))
                self.fullname = fullname
                self.noWarnings = False  # this resets the display options for each new image
                self.canvas.delete()
                self.cookie['current_file'] = self.IMAGEDATA['filename']
                self.cookie['zoom_scale'] = self.IMAGEDATA['zoom_scale']
                try:
                    self.global_zoom_var.trace_vdelete('w', self.global_zoom_watcher)
                    self.global_zoom_var.set(int(self.IMAGEDATA['zoom_scale'] * 100))
                    self.global_zoom_watcher = self.global_zoom_var.trace('w', self.zoom_global)
                except:
                    print('first start')
                if self.IMAGEDATA['file_scale'] < 1 | self.global_zoom_var.get() < 100:  # file scale is applied when near maxsize, zoom_scale is global zooming
                    self.cookie['file_scale'] = self.IMAGEDATA['file_scale']
                    a = int(self.IMAGEDATA['xsize'] * self.cookie['file_scale'] * self.cookie['zoom_scale'])
                    b = int(self.IMAGEDATA['ysize'] * self.cookie['file_scale'] * self.cookie['zoom_scale'])
                    try:
                        self.img = self.img.resize((a, b), Image.NEAREST)
                    except:
                        messagebox.showerror("Error",
                                             "There seems to be a problem with the free available memory in your computer. Please consider either using the 64bit Version of iTAG or increasing your machines RAM. If you are working with very large files, try to work with one file per session. iTAG will now shut down cleanly, so that you will receive output from your current session")
                        self.session_end()
                self.img = image_FX(self.img, FX=self.IMAGEDATA['global_FX'])
                self.img = image_FX(self.img, FX=self.IMAGEDATA['global_FX'])

                try:
                    self.cImage = ImageTk.PhotoImage(self.img)  # open the first image!
                except:
                    messagebox.showerror("Error",
                                         "There seems to be a problem with the free available memory in your computer. Please consider either using the 64bit Version of iTAG or increasing your machines RAM. If you are working with very large files, try to work with one file per session. iTAG will now shut down cleanly, so that you will receive output from your current session")
                    self.session_end()
                x, y = self.img.size
                self.cookie['current_image_original_size'] = self.img.size

                # this is the panel image / panel loads much faster that way
                scale = float(max(self.img.size)) / self.cookie['panel_canvas_size']
                width, height = self.img.size
                newsize = int(width / scale), int(height / scale)
                try:
                    self.pImage = ImageTk.PhotoImage(self.img.resize(newsize))
                except:
                    img = Image.new("RGB", newsize, 'black')
                    draw = ImageDraw.Draw(img)
                    textx = int(newsize[0] / 2)
                    texty = int(newsize[1] / 2)
                    self.pImage = ImageTk.PhotoImage(img)
                    draw.text((textx, texty),
                              "You seem to have run into memory issues. Please consider either increasing your system Memory or switching to the 64bit Version of iTAG to make more Memory available. You can still use the navigational panel for navigation.",
                              'white')
                    print("load failure")
                self.cookie['panel_image_size'] = newsize
                self.cookie['panel_image_scale'] = scale

                # from here on, ugly hotfix
                xscroll = Scrollbar(self.cFrame, orient=HORIZONTAL)
                xscroll.grid(row=1, column=0, sticky=E + W)
                yscroll = Scrollbar(self.cFrame, orient=VERTICAL)
                yscroll.grid(row=0, column=1, sticky=N + S)
                self.canvas = Canvas(self.cFrame, bd=0, relief=FLAT, width=x, height=y, bg='black')
                self.canvas.create_image(0, 0, image=self.cImage, anchor="nw", tags=("bg", 0, 'None'))
                self.canvas.grid(row=0, column=0, sticky=N + S + W + E)
                self.canvas.config(scrollregion=self.canvas.bbox(ALL), xscrollincrement=1,
                                   yscrollincrement=1)  # scrolling needs tweaking
                self.canvas.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
                xscroll.config(command=self.canvas.xview)
                yscroll.config(command=self.canvas.yview)

                # binds
                for i in range(1, len(self.cookie['catnames']) + 1):
                    self.parent.bind(str(i), lambda event: self.setcat(event))  # switch cat to legend item 1

                self.parent.bind("<Shift_L>",
                                 lambda event, alt_i=1: self.showSub(event, alt_i))  # paint, save coordinates
                self.parent.bind("<KeyRelease-Shift_L>", lambda event, flag=False, alt_i=1: self.showSub(event, alt_i,
                                                                                                         flag))  # paint, save coordinates
                self.parent.bind("<Control_L>",
                                 lambda event, alt_i=2: self.showSub(event, alt_i))  # paint, save coordinates
                self.parent.bind("<KeyRelease-Control_L>", lambda event, flag=False, alt_i=2: self.showSub(event, alt_i,
                                                                                                           flag))  # paint, save coordinates
                self.parent.bind("<Alt_L>",
                                 lambda event, alt_i=3: self.showSub(event, alt_i))  # paint, save coordinates
                self.parent.bind("<KeyRelease-Alt_L>", lambda event, flag=False, alt_i=3: self.showSub(event, alt_i,
                                                                                                       flag))  # paint, save coordinates
                self.parent.bind("<x>", lambda event: self.setcat(event))  # paint, save coordinates

                self.canvas.tag_bind('bg', "<Enter>", lambda event: self.canvas.focus_set())
                self.canvas.tag_bind('bg', "<Button 3>",
                                     lambda event, alt_i=0: self.tag_add_entry(event, alt_i))  # paint, save coordinates
                self.canvas.tag_bind('bg', "<Shift-Button 3>",
                                     lambda event, alt_i=1: self.tag_add_entry(event, alt_i))  # paint, save coordinates
                self.canvas.tag_bind('bg', "<Control-Button 3>",
                                     lambda event, alt_i=2: self.tag_add_entry(event, alt_i))  # paint, save coordinates
                self.canvas.tag_bind('bg', "<Alt-Button 3>",
                                     lambda event, alt_i=3: self.tag_add_entry(event, alt_i))  # paint, save coordinates
                self.canvas.bind("<Button 1>", self.grab)  # grab and...
                self.canvas.bind("<B1-Motion>", self.drag)  # drag!
                self.canvas.bind("<ButtonRelease 1>", self.re_view)  # release!
                # done hotfixing

                self.cextent = (self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.winfo_width(),
                                self.canvas.winfo_height())  # current canvas extent
                self.cookie['cextent'] = (self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.winfo_width(),
                                          self.canvas.winfo_height())  # current canvas extent

                title = 'iTAG {0} {1} {2} {3}'.format(self.GLOBALS['ARCH'], self.GLOBALS['MAJOR'], self.user.get(),
                                                      self.fname)
                if self.cookie['file_scale'] != 1 or self.cookie['zoom_scale'] != 1:
                    title += ' ({0})'.format(str(int(self.cookie['file_scale'] * self.cookie['zoom_scale'] * 100)))
                title += ' [{0}/{1}]'.format(str(self.currentFilePos.get() + 1), str(len(self.cookie['dirList'])))
                self.parent.title(title)
                self.lfname.configure(
                    text=self.IMAGEDATA['filename'] + " [" + str(self.currentFilePosHR.get()) + os.path.sep + str(
                        len(self.cookie['dirList'])) + "]")
                self.redraw_tags(size, use_file_tagsize=True)
                self._y = 0
                self._x = 0
        self.cookie['current_file'] = self.fname
        self.cookie['current_file_index'] = self.currentFilePos.get()
        self.cookie['cextent'] = (self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.winfo_width(),
                                  self.canvas.winfo_height())  # current canvas extent #possible dup
        if self.pop.get():
            self.panel.update(self.cookie, index=0, gpsdict=self.IMAGEDATA)
        self.mainWindow.pack(fill=BOTH, expand=1)

    def showSub(self, event, alt_i, flag=True):
        if not self.tag_remove_entrymode:
            if flag:
                self.currentMod.set(self.cookie['modnames'][alt_i])
            else:
                self.currentMod.set(self.cookie['modnames'][0])

    def nextImage(self, event=None):  # ok!
        if self.currentFilePos.get() < len(self.cookie['dirList']) - 1:
            if self.noWarnings: self.toggle_WARN()
            self.currentFilePos.set(self.currentFilePos.get() + 1)
            self.redraw(size=self.tagsize)
        else:
            messagebox.showinfo("Warning", self.TRANSLATION['DIRLIST_FINISHED'])

    def prevImage(self, event=None):  # ok!
        if self.currentFilePos.get() > 0:
            self.currentFilePos.set(self.currentFilePos.get() - 1)
            self.redraw(size=self.tagsize)
        else:
            messagebox.showinfo("Warning", self.TRANSLATION['DIRLIST_FINISHED'])

    def grab(self, event):  # ok!
        self.DEF_CURSOR = self.canvas.cget('cursor')
        self.canvas.config(cursor='fleur')
        if self.enable:
            self._y = event.y
            self._x = event.x

    def re_view(self, event=None):  # hmm, ugly but alright
        if self.enable:
            x = self.canvas.winfo_width()
            y = self.canvas.winfo_height()
            self.cextent = (
                self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.canvasx(x), self.canvas.canvasy(y))
            self.cookie['cextent'] = (
                self.canvas.canvasx(0), self.canvas.canvasy(0), self.canvas.canvasx(x), self.canvas.canvasy(y))
            self.canvas.config(cursor=self.DEF_CURSOR)
            if self.pop.get():
                self.panel.Navi.moveview(self.cookie)

    def drag(self, event):  # ok!
        if self.enable:
            dify = self._y - event.y
            difx = self._x - event.x
            self.canvas.yview("scroll", dify, "units")  # "exponential" panning
            self.canvas.xview("scroll", difx, "units")
            self.magnifier_crop(event)
            self._x = event.x
            self._y = event.y

    def set_view(self, event):  # hah! nailed it!
        if self.enable:
            scale = self.panel.Navi.scale
            xp, yp = int(event.x * scale), int(event.y * scale)
            # xc, yc = self.img.size
            xc, yc = self.cookie['current_image_original_size']
            self.canvas.yview("moveto", float(yp) / yc)
            self.canvas.xview("moveto", float(xp) / xc)
            self.re_view()

    # def sqlite_add_tag_entry(self, tag, conn):
    #     placeholders = ', '.join(['%s'] * len(tag))
    #     for i, j in tag.items():
    #         try:
    #             tag[i] = tag[i].decode('string-escape')
    #         except:
    #             pass
    #         if j is None:
    #             tag[i] = 'None'
    #     values = tuple(tag[key] for key in tag.keys())
    #     columns = ', '.join(tag.keys())
    #     sql = "INSERT into detailed ( %s ) VALUES %s" % (columns, values)
    #     conn.execute(sql)
    #     conn.commit()

    # def sqlite_create_summary_table(self, conn, so):
    #     sql = "DROP TABLE IF EXISTS 'summary';"
    #     conn.execute(sql)
    #     sql = "CREATE TABLE 'summary' AS SELECT * FROM files;"
    #     conn.execute(sql)
    #     for c in so.out_clean:
    #         sql = "ALTER TABLE 'summary' ADD COLUMN '" + c + "' INT;"  # create clean columns
    #         conn.execute(sql)
    #     files = []
    #     sql = "SELECT filename FROM files;"
    #     for row in conn.execute(sql):
    #         files.append(row[0])
    #     for f in files:  # maybe group by files and then iterate?
    #         for c in so.out:
    #             sql = "SELECT sum(count),category FROM detailed WHERE filename = '" + f + "' AND category = '" + c + "';"
    #             val = conn.execute(sql).fetchone()[0]
    #             if val is None:
    #                 val = 0
    #             c2 = re.sub('[:*.!,;\s]', '_', c)  # remove evil characters
    #             sql = "UPDATE summary SET '" + c2 + "' = " + str(val) + " WHERE filename = '" + f + "';"
    #             conn.execute(sql)
    #             try:
    #                 self.pb.STEP()  # maybe remove if we include progress bar on dump
    #             except:
    #                 pass
    #     conn.commit()

    # def sqlite_add_file_entry(self, tag, conn):
    #     placeholders = ', '.join(['%s'] * len(tag))
    #     for i, j in tag.items():
    #         if j is None:
    #             tag[i] = 'None'
    #     values = tuple(str(tag[key]) for key in tag.keys())
    #     columns = ', '.join(tag.keys())
    #     sql = "INSERT into files ( %s ) VALUES %s" % (columns, values)
    #     conn.execute(sql)
    #     conn.commit()

    # def sqlite_remove_tag_entry(self, ID, conn):
    #     sql = "DELETE from detailed where ID = %s" % ID
    #     conn.execute(sql)
    #     conn.commit()

    def tag_add_entry(self, event, alt_i):  # ok, uses extended alttext
        if self.tags_hidden.get():
            messagebox.showinfo("Info", 'While tags are hidden, the creation or deletion of tags is disabled')
            return
        if self.tag_remove_entrymode:
            self.tag_remove_entry(event)
            return
        else:
            if (self.cat != 0 and self.enable):
                item = self.canvas.find_closest(self.canvas.canvasx(0) + event.x,
                                                self.canvas.canvasy(0) + event.y)  # find possible overlaps?
                cTAGS = self.canvas.gettags(item[0])  # get tags for overlap check
                if cTAGS[0] == "tag":
                    if self.noWarnings is False:
                        messagebox.showwarning("Warning",
                                               self.TRANSLATION['TAG_OVERLAP'] + " " + self.cookie['modnames'][
                                                   int(cTAGS[4])] + " " +
                                               self.cookie['catnames'][int(cTAGS[2])])
                self.category_text = self.cookie['modnames'][alt_i] + ' ' + self.cookie['catnames'][self.spec_index]
                x = (self.canvas.canvasx(0) + event.x) / self.cookie['file_scale']  # some images may be reduced!!
                y = (self.canvas.canvasy(0) + event.y) / self.cookie['file_scale']
                x = x / self.cookie['zoom_scale']
                y = y / self.cookie['zoom_scale']
                tag = {'username': self.user.get(), 'filename': str(self.fname), 'xpos': int(x), 'ypos': int(y),
                       'category': self.category_text, 'category_index': self.spec_index, 'modifier': alt_i, 'count': 1,
                       'colour': self.cookie['colours'][self.spec_index], 'species_index': self.spec_index,
                       'ID': self.ID, 'lat': self.IMAGEDATA['lat'], 'lon': self.IMAGEDATA['lon'],
                       'altitude': self.IMAGEDATA['altitude'], 'gps_date': self.IMAGEDATA['gpsTime'],
                       'cam_date': self.IMAGEDATA['DateTimeOriginal'],
                       'save_date': str(datetime.datetime.utcnow().time()), 'group_ID': self.currentGroupID.get(),
                       'tagsize': self.cookie['tagsize']}
                self.conn.insertRow('detailed',tag)
                self.paint(event, alt_i, size=self.cookie['tagsize'])  # added size
                self.cookie['catcounter'][self.spec_index][alt_i] += 1
                if self.pop.get(): self.panel.update(cookie=self.cookie, i=self.cookie['currentSpecIndex'], j=alt_i,
                                                     index=1)

    def paint(self, event, alt_i, size=3):  # clean up
        x1, y1 = (self.canvas.canvasx(0) + event.x), (self.canvas.canvasy(0) + event.y)
        if (x1 <= self.canvas.bbox('bg')[2] and y1 <= self.canvas.bbox('bg')[3]):  # check if coord are on canvas image
            col = self.cookie['colours'][self.spec_index]
            group = self.currentGroupID.get()
            l_index = self.spec_index
            ID = self.ID
            self.tag_paint_entry(x1, y1, alt_i, l_index, ID, size, col, group)
            self.item = self.canvas.find_closest(self.canvas.canvasx(0) + event.x, self.canvas.canvasy(0) + event.y)[
                0]  # why do we need this
            self.Sitems.set(self.Sitems.get() + 1)
            self.cookie['Sitems'] = self.Sitems.get()
            self.ID += 1
            self.cookie['ID'] = self.ID
        else:
            print('outside')

    def inc_tagsize(self, event=None):
        self.set_tagsize(direction='+')

    def dec_tagsize(self, event=None):
        self.set_tagsize(direction='-')

    def inc_groupID(self, event=None):
        indx = self.cookie['currentSpecIndex']
        self.groupc[indx] += 1
        self.currentGroupID.set(self.groupc[indx])

    def dec_groupID(self, event=None):
        indx = self.cookie['currentSpecIndex']
        if self.groupc[indx] > 1:
            self.groupc[indx] -= 1
            self.currentGroupID.set(self.groupc[indx])

    def set_tagsize(self, direction, event=None):
        maxtagsize = max(self.cookie['current_image_original_size'])
        if self.tagsize > maxtagsize: self.tagsize = maxtagsize
        if (direction == '+' and self.tagsize < int(maxtagsize * .1)):  # max tagsize now 10% of longest image size
            self.tagsize += 1
            self.cookie['tagsize'] = self.tagsize
            self.redraw_tags(size=self.tagsize)
        if (direction == '-' and self.tagsize > 1):
            self.tagsize -= 1
            self.cookie['tagsize'] = self.tagsize
            self.redraw_tags(size=self.tagsize)

    def tag_remove_entry(self, event):  # somethings weird... removed tags are not removed from sql????
        if self.tags_hidden.get():
            messagebox.showinfo("Info", 'While tags are hidden, the creation or deletion of tags is disabled')
            return
        if (self.cat != 0):
            item = self.canvas.find_closest(self.canvas.canvasx(0) + event.x,
                                            self.canvas.canvasy(0) + event.y)  # get item number
            cTAGS = self.canvas.gettags(item[0])  # find the closest item and assign tags to cTAGS
            if (self.canvas.gettags(item[0])[2] == str(self.spec_index)):  # all canvas are created with bg tag!
                self.sqlite_remove_tag_entry(ID=cTAGS[3], conn=self.sqlite_conn)  # this is superb!!!
                objectID = 'object_ID: ' + str(cTAGS[3])
                self.canvas.delete(objectID)
                self.Sitems.set(self.Sitems.get() - 1)
                self.cookie['Sitems'] = self.Sitems.get()
                alt_i = int(cTAGS[4])
                self.cookie['catcounter'][self.spec_index][alt_i] -= 1
                if self.pop.get(): self.panel.update(self.cookie, i=self.cookie['currentSpecIndex'], j=alt_i, index=1)

    def session_newWiz(self, event=None):  # clean up
        self.parent.protocol("WM_DELETE_WINDOW", self._NULL)
        wiz = Wizard(self.mainWindow, self.PARAMETER)
        self.wait_window(wiz)
        self.parent.protocol("WM_DELETE_WINDOW", self.session_end)
        if wiz.result:
            self.cookie_update(wiz.out)  # updates cookie keys with new values from wiz.out dict
            self.cookie['catcounter'] = [[0] * len(self.cookie['modnames']) for x in
                                         range(len(self.cookie['catnames']))]
            self.species = self.cookie['catnames']
            self.alttext = self.cookie['modnames']
            self.user.set(self.cookie['user'])
            self.params = self.cookie['params']
            self.colours = self.cookie['colours']
            self.basename = self.cookie['basename']
            self.dirList = self.cookie['dirList']
            newdir = self.cookie['newdir']
            self.tagsize = self.cookie['tagsize']
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            self.catc = []  # new category counter...
            self.groupc = []
            for i in range(0, len(self.cookie['catnames'])):
                self.catc.append([0, 0, 0, 0])
                self.groupc.append(1)
            self.cookie['groupc'] = self.groupc
            self.parent.title(self.GLOBALS['VERSIONSTRING'] + ": " + self.user.get())

            self.conn = SQLiteHandler(
                SQLiteFileName=os.path.join(self.cookie['basename'], self.user.get(), self.user.get() + '_DB.db'))
            self.files_browse_exif(self.cookie)  # get and store all exif data in sqlite db

            self.redraw(size=self.cookie['tagsize'])
            self.session_on()
            #self.sqlite_session_fill()
        else:
            messagebox.showinfo("Info", 'Cancelled new session Wizard')

    def files_browse_exif(self, cookie):
        dirlist = cookie['dirList']
        i = 0
        for f in dirlist:
            basename = str(os.path.dirname(f))
            filename = str(os.path.basename(f))
            suffix = str(os.path.splitext(f)[1])
            i += 1
            try:
                img = Image.open(f)
                skip_image_badfile = False
            except IOError:
                skip_image_badfile = True
                sql = 'delete from files where filename ="%s"' % (filename)
                self.sqlite_conn.execute(sql)
                messagebox.showinfo("Info", self.TRANSLATION['REDRAW_WARN'] + " " + f)
                self.cookie['dirList'].pop(i - 1)
                next
            D = self.get_exif(img)
            x, y = img.size
            mode = img.mode
            cscale = 1
            if max(x, y) > self.GLOBALS['MAXSIZE']:cscale = float(self.GLOBALS['MAXSIZE']) / float(max(x, y))
            tag = dict(ID=i, basename=basename, filename=filename, xsize=x, ysize=y, image_mode=mode, file_scale=cscale,
                       zoom_scale=1, Valid_GPS=D['Valid_GPS'], ISOSpeedRatings=D['ISOSpeedRatings'],
                       ExifVersion=D['ExifVersion'], coord_ref=D['coord_ref'], lat=D['lat'], lon=D['lon'],
                       altitude=D['altitude'], gpsTime=D['gpsTime'], DateTime=D['DateTime'],
                       DateTimeOriginal=D['DateTimeOriginal'], DateTimeDigitized=D['DateTimeDigitized'],
                       FocalLength=D['FocalLength'], Model=D['Model'], Make=D['Make'], Valid_Exif=D['Valid_Exif'],
                       skip_file=0, global_FX=0)
            self.conn.insertRow(tableName='files', dictionary=tag)

    def write_CSV(self, conn, so):  # rewrite as sql based export
        cols = so.out
        sep = so.out_CSV_SEP
        cols = [x.replace(' ', '_') for x in cols]
        summary_cols = self.TRANSLATION[
                           'SUMMARY_COLS'] + cols  # SUMMARY_COLS is actually from language file!!!! change that!!!!
        detail_cols = self.TRANSLATION['DETAIL_COLS']
        newdir = os.path.normpath(os.path.join(self.cookie['basename'], self.user.get(), 'Tables'))
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        filename = os.path.join(self.cookie['basename'], self.user.get(), 'Tables',
                                self.user.get() + '-' + "_detailed_results.csv")
        detailed_csvfile = open(filename, 'wb')
        detailed_CSV = csv.writer(detailed_csvfile, delimiter=sep)
        detailed_CSV.writerow(detail_cols)
        sql = "SELECT ID,username,filename,xpos,ypos,category,count,lat,lon,altitude,gps_date,cam_date,save_date from detailed;"
        for row in conn.execute(sql):
            detailed_CSV.writerow(row)
            self.pb.STEP()
        detailed_csvfile.close()

        filename = os.path.join(self.cookie['basename'], self.user.get(), 'Tables',
                                self.user.get() + '-' + "_summary_results.csv")
        summary_csvfile = open(filename, 'wb')
        summary_CSV = csv.writer(summary_csvfile, delimiter=sep)
        summary_CSV.writerow(summary_cols)

        # sql="SELECT * from summary;"
        summary_cols = ', '.join(map(str, summary_cols))
        sql = "SELECT '" + self.user.get() + "' as %s from summary;" % (summary_cols)
        for row in conn.execute(sql):
            summary_CSV.writerow(row)
            self.pb.STEP()
        summary_csvfile.close()

        filename = os.path.join(self.cookie['basename'], self.user.get(), 'Tables',
                                self.user.get() + '-' + "_legend.csv")
        legend_csvfile = open(filename, 'wb')
        legend_text = self.TRANSLATION['LEGEND_TEXT']
        legend_CSV = csv.writer(legend_csvfile, delimiter=sep)
        legend_CSV.writerow(["Category", "Color"])
        for i in range(0, len(self.cookie['catnames'])):
            col = [self.cookie['catnames'][i], self.cookie['colours'][i]]
            legend_CSV.writerow(col)
            self.pb.STEP()

        legend_CSV.writerow(["", ""])
        legend_CSV.writerow(["Category", "Color"])
        for i in range(0, len(self.cookie['modnames'])):
            col = [self.cookie['modnames'][i], legend_text[i]]
            legend_CSV.writerow(col)
            self.pb.STEP()
        legend_csvfile.close()

    def write_SQL(self, conn):  # error?
        print(self.cookie['basename'] + os.path.sep + self.user.get() + os.path.sep + self.user.get() + '_dump.sql')
        try:
            with open(self.cookie[
                          'basename'] + os.path.sep + self.user.get() + os.path.sep + self.user.get() + '_dump.sql',
                      'w') as f:
                for line in conn.iterdump():  # summary is missing??
                    f.write('%s\n' % line)
        except:
            pass

    def get_exif(self, img):  # ok! #returns list with filename, lat, lon, altitde and datetime #maybe add focal length?
        from PIL.ExifTags import TAGS, GPSTAGS
        TAGS.update(GPSTAGS)  # merge the two dicts
        img = img
        D = {}
        lat = None
        lon = None
        altitude = None
        DateTime = None
        coordref = None
        D['GPSInfo'] = ''
        D['ISOSpeedRatings'] = ''
        D['ExifVersion'] = ''
        D['DateTime'] = ''
        D['DateTimeOriginal'] = ''
        D['DateTimeDigitized'] = ''
        D['FocalLength'] = 1.0
        D['Model'] = ''
        D['Make'] = ''
        D['Valid_Exif'] = 0
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                D['GPSInfo'] = exifinfo.get(34853)  # gpsinfo
                D['ISOSpeedRatings'] = exifinfo.get(34855)  # gpsinfo
                D['ExifVersion'] = exifinfo.get(36864).decode('utf-8')  # gpsinfo
                D['DateTime'] = str(exifinfo.get(306))  # gpsinfo
                D['DateTimeOriginal'] = str(exifinfo.get(36867))  # gpsinfo
                D['DateTimeDigitized'] = str(exifinfo.get(36868))  # gpsinfo
                D['FocalLength'] = exifinfo.get(37386)[0] / exifinfo.get(37386)[1]  # x:y result is mm
                D['Model'] = exifinfo.get(272)  # gpsinfo
                D['Make'] = exifinfo.get(271)  # gpsinfo
                D['Valid_Exif'] = 1
                DateTime = D['DateTimeOriginal']
        ok = 0
        try:
            lat = [float(x) / float(y) for x, y in D['GPSInfo'][2]]
            latref = D['GPSInfo'][1]
            lon = [float(x) / float(y) for x, y in D['GPSInfo'][4]]
            lonref = D['GPSInfo'][3]
            lat = lat[0] + lat[1] / 60 + lat[2] / 3600
            lon = lon[0] + lon[1] / 60 + lon[2] / 3600
            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon
            altitude = D.get('GPSInfo')[6][0]
            DateTime = str(D.get('GPSInfo')[29])
            coordref = D.get('GPSInfo')[18]
            ok = 1
        except:
            pass
        D['lat'] = lat
        D['lon'] = lon
        D['altitude'] = altitude
        D['Valid_GPS'] = ok
        D['coord_ref'] = coordref
        D['gpsTime'] = DateTime
        if ok: del D['GPSInfo']
        return D

    def write_KML(self, conn, so):
        cols = so.out_clean
        cols = ', '.join(map(str, cols))

        # simple points
        DATA = []
        sql = "select basename,filename,lat,lon,altitude,gps_date,Valid_GPS, %s from summary where Valid_GPS='True' order by gps_date asc" % (
            cols)
        for row in conn.execute(sql):
            if any(t > 0 for t in row[7:]):
                DATA.append((row))
        kml_point = simplekml.Kml(open=1)  # the folder will be open in the table of contents
        for i in range(0, len(DATA)):
            self.pb.STEP()
            basename = DATA[i][0]
            filename = DATA[i][1]
            fullname = os.path.normpath(os.path.join(basename, filename.lower()))
            lat = DATA[i][2]
            lon = DATA[i][3]
            alt = DATA[i][4]
            gpsdate = DATA[i][5]
            summary = zip(so.out, [x for x in DATA[i][6:len(DATA[i])]])
            counts = {}
            for k, v in summary:
                if v > 0:
                    counts[k] = v
            counts = ', '.join("%s=%r" % (key, val) for (key, val) in counts.items())
            pnt = kml_point.newpoint()
            pnt.name = filename
            path = os.path.normpath(os.path.join(self.cookie['basename'], self.user.get(), 'Images',
                                                 self.user.get() + '-' + filename.lower()))
            if os.path.isfile(path):
                picpath = os.path.normpath(os.path.join('Images',
                                                        self.user.get() + '-' + filename.lower()))  # currently only shows tagged images
            else:
                picpath = ''
            desc = "taken on %s at %s m\n%s\ntagged by %s" % (gpsdate, alt, str(counts), self.user.get())
            pnt.description = '<a href>' + picpath + '<img src="' + picpath + '" width=800 alt="picture" align="center" /></a> ' + desc
            pnt.altitudemode = simplekml.AltitudeMode.relativetoground
            pnt.coords = [(lon, lat, alt)]
        filename = self.cookie['basename'] + os.sep + self.user.get() + os.sep + self.user.get() + '_points_KML.kml'
        kml_point.save(filename)

        # simple lines
        kml_line = simplekml.Kml(open=1)  # the folder will be open in the table of contents
        DATA = []
        sql = "select lat,lon,altitude,gps_date,Valid_GPS from summary where Valid_GPS='True' order by gps_date asc"
        time = []
        coords = []
        for row in conn.execute(sql):
            DATA.append((row))
        for i in range(0, len(DATA)):
            coords.append([DATA[i][1], DATA[i][0], DATA[i][2]])  # its lon,lat,altitude
            time.append(DATA[i][3])
        linestring = kml_line.newlinestring(name="course plot from images with valid GPS sections")
        linestring.coords = coords
        linestring.altitudemode = simplekml.AltitudeMode.relativetoground
        linestring.extrude = 1
        linestring.tesselate = 1
        filename = self.cookie['basename'] + os.sep + self.user.get() + os.sep + self.user.get() + '_lines_KML.kml'
        kml_line.save(filename)

    def write_IMG(self, conn):  # ok should be optimized (generator?)
        from PIL import ImageFont
        skip = 0
        size = self.cookie['tagsize']
        if self.Sitems.get() != 0:
            newdir = os.path.normpath(os.path.join(self.cookie['basename'], self.user.get(), 'Images'))
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            sql = "SELECT filename from files;"
            files = []
            for row in conn.execute(sql):
                files.append(row[0])
            for fname in files:
                sql = "select count(*) from detailed where filename = '%s'" % (fname)  # and count(*)>0
                empty = conn.execute(sql).fetchone()[0]
                if empty != 0:
                    try:
                        img = Image.open(fname)  # if file does not exist, skip!
                    except:
                        skip += 1
                        self.pb.STEP()
                        continue
                    draw = ImageDraw.Draw(img)
                    sql = "select xpos,ypos,category_index,modifier,group_ID,tagsize from detailed where filename = '%s'" % (
                        fname)
                    save = False
                    first = True
                    for row in conn.execute(sql):
                        x1, y1, cat, alt_i, group, tagsize = row
                        col = self.cookie['colours'][cat]
                        if (alt_i == 0):
                            draw.ellipse((x1 - 3 * size, y1 - 3 * size, x1 + size, y1 + size), fill=col)
                        elif (alt_i == 1):
                            draw.rectangle([x1 - 3 * size, y1 - 3 * size, x1 + size, y1 + size], fill=col)
                        elif (alt_i == 2):
                            draw.rectangle([x1 - 3 * size, y1 - 3 * size, x1 - 2 * size, y1 + size], fill=col)
                            draw.rectangle([x1 - 2 * size, y1 + size, x1 + size, y1], fill=col)
                            draw.rectangle([x1, y1, x1 + size, y1 - 3 * size], fill=col)
                            draw.rectangle([x1 - 3 * size, y1 - 3 * size, x1 + size, y1 - 2 * size], fill=col)
                        elif (alt_i == 3):
                            draw.rectangle([x1 - 2 * size, y1 - size, x1 + 2 * size, y1 + size], fill=col)
                        font = ImageFont.truetype("arial.ttf", size * 5)
                        draw.text((x1, y1), text=str(group), fill=globalFunctions.col_invert(col), anchor='center',
                                  font=font)
                    filename = os.path.join(self.cookie['basename'], self.user.get(), 'Images',
                                            self.user.get() + '-' + fname.lower())
                    img.save(filename)
                self.pb.STEP()

            ### legend creation #UUUUGLY!
            leg = Image.new('RGB', (300, (len(self.cookie['catnames']) + 1) * 50), color="#FFFFFF")
            draw = ImageDraw.Draw(leg)
            x = 10
            y = 15
            for i in range(0, len(self.cookie['catnames'])):
                draw.rectangle([x, y, x + 190, y + 25],
                               fill=globalFunctions.col_invert(self.cookie['colours'][i - 1]))  # obvious?
                draw.ellipse([x, y, x + 25, y + 25], fill=self.cookie['colours'][i - 1])
                draw.text((x + 30, y + 5), text=self.cookie['catnames'][i - 1],
                          fill=self.cookie['colours'][i - 1])  # uglyyyyy......
                y += 35
            x = 200
            y = 15
            draw.ellipse([x, y, x + 25, y + 25], fill="#000000")  # adult
            draw.text((x + 30, y + 5), self.cookie['modnames'][0], fill="#000000")  # needs for i in 1:len(alttext)
            y += 35
            draw.rectangle([x, y, x + 20, y + 20], fill="#000000")  # juvenile
            draw.text((x + 30, y + 5), self.cookie['modnames'][1], fill="#000000")  # needs for i in 1:len(alttext)

            y += 35
            draw.rectangle([x, y, x + 5, y + 20], fill="#000000")  # swimming
            draw.rectangle([x + 5, y + 20, x + 20, y + 15], fill="#000000")
            draw.rectangle([x + 20, y + 15, x + 15, y], fill="#000000")
            draw.rectangle([x + 15, y, x, y + 5], fill="#000000")
            draw.text((x + 30, y + 5), self.cookie['modnames'][2], fill="#000000")  # needs for i in 1:len(alttext)

            y += 35
            draw.rectangle([x, y + 10, x + 20, y + 15], fill="#000000")
            draw.text((x + 30, y + 5), self.cookie['modnames'][3], fill="#000000")  # needs for i in 1:len(alttext)
            filename = os.path.join(self.cookie['basename'], self.user.get(), 'Images',
                                    self.user.get() + '-' + 'legend.jpg')
            leg.save(filename)
            self.pb.STEP()
        else:
            messagebox.showinfo("Info", self.TRANSLATION['NO_OBJECTS_TAGGED'])
        if skip > 0: messagebox.showwarning("Warning", 'Some images were skipped as they were not available anymore')

    def get_row_from_sqlite(self, conn):
        sql = "select * from detailed"
        out = []
        for row in conn.execute(sql):
            out.append(row)
        return (out)

    def get_sqlite_from_row(self, data, conn):
        # self.createDB(fname=self.cookie['basename'] + '/' + self.user.get() + '/'+self.user.get()+'_DB.db')
        self.row_test = []
        for row in data:
            tag = {'ID': str(row[0]), 'username': str(row[1]), 'filename': str(row[2]), 'xpos': str(row[3]),
                   'ypos': str(row[4]), 'category': str(row[5]), 'category_index': str(row[6]), 'modifier': str(row[7]),
                   'count': str(row[8]), 'colour': str(row[9]), 'species_index': str(row[10]), 'group_ID': str(row[11]),
                   'lat': str(row[12]), 'lon': str(row[13]), 'altitude': str(row[14]), 'gps_date': str(row[15]),
                   'cam_date': str(row[16]), 'save_date': str(row[17]), 'tagsize': str(self.cookie['tagsize'])}
            self.sqlite_add_tag_entry(tag, conn=conn)

    def session_end(self, event=None):  # okish
        if self.Sitems.get() != 0:
            self.parent.attributes("-disabled", True)
            o = OKCANCEL(self.mainWindow, self.PARAMETER, mtext=self.TRANSLATION['QUERY_SAVE'])
            self.save_ok = False
            if o.result:
                # self.deactivate_all()
                self.parent.attributes("-disabled", False)
                self.session_save()  # this also creates a self.row file
                if self.save_ok:
                    sql = 'select count(*) as count,Valid_GPS from files where Valid_GPS = "True"'
                    valid_gps = self.sqlite_conn.execute(sql).fetchone()[0]  # later
                    so = OutputOptions(self.mainWindow, self.PARAMETER, rows=self.cookie['catnames'],
                                       columns=self.cookie['modnames'])
                    self.wait_window(so)  # will resume after so is destroyed
                    # self.pb = self.Progress(self.mainWindow)
                    self.pb = progressClass.Progress(self.mainWindow, self.PARAMETER)
                    self.update()
                    self.sqlite_create_summary_table(conn=self.sqlite_conn, so=so)
                    self.save_output(connection=self.sqlite_conn, so=so)  # create output
                    try:
                        self.sqlite_conn.commit()
                    except:
                        pass
                    self.pb.DONE()
                    messagebox.showinfo("Session exported",
                                        'All data has been exported. Thank you for using iTAG ' + self.GLOBALS[
                                            'VERSIONSTRING'] + '!')
                    self.quit()
                else:
                    messagebox.showwarning("Warning", 'No data has been saved. Returning to session')
                    self.save_ok = False
                    return
            else:
                o = OKCANCEL(self.mainWindow, self.PARAMETER, mtext='Are you sure you want to quit without saving?')
                self.parent.attributes("-disabled", False)
                if o.result:
                    self.quit()
        else:
            self.parent.attributes("-disabled", True)
            o = OKCANCEL(self.mainWindow, self.PARAMETER,
                         mtext='No tags are present. Would you like to quit without saving?')
            self.parent.attributes("-disabled", False)
            if o.result:
                self.quit()
            else:
                pass

    def check_files(self, dirlist, fname):  # not yet awesome
        basedir = dirlist.get('basename')
        if basedir is None or basedir == '':
            basedir = os.path.split(fname)[0]
        ofiles = [x.lower() for x in dirlist['filenames']]
        dirok = False
        newdir = basedir
        while not dirok:  # extend to files?
            try:
                os.chdir(newdir)  # we will need to check whether that dir still exists, ask for it if not?
                dirok = True
                dirname = newdir
            except:
                messagebox.showerror("Error", "Could not find directory" + " " + basedir + "\n" + FILES_NEWLOC)
                dirname = askdirectory(parent=self.parent, initialdir=os.getcwd(),
                                       title="Please provide the new location for: " + basedir)
                dirok = False
                newdir = dirname
                if dirname == '':  # if user clicks cancel
                    self.cookie['basename'] = basedir
                    return False  # maybe return something else, so we can start recovery mode, dump shit and exit!?
                    break
        # check if files are there
        dirList = [os.path.normpath(dirname + os.sep + f) for f in os.listdir(dirname) if
                   re.search(r'.*\.(jpg|JPG|bmp|BMP)$', f)]
        newFileList = [os.path.split(str(x))[1].lower() for x in dirList]  # file names
        n = set(newFileList)
        o = set(ofiles)
        was = str(len(o))
        found = str(len(n))
        lost = str(len(o - n))
        remain = str(len(o) - len(o - n))
        if len(o - n) == 0:
            self.cookie['basename'] = dirname
            self.cookie['dirList'] = [os.path.normpath(self.cookie['basename'] + os.sep + x) for x in
                                      sorted(list(n & o))]
            self.cookie['filenames'] = [os.path.split(str(x))[1] for x in self.cookie['dirList']]
            return True
        elif len(o - n) < len(o):
            messagebox.showwarning("Warning", 'File(s): ' + ','.join(
                o - n) + ' is(are) missing (' + remain + ' of ' + was + ')!\nIf missing Image contained Tags, these will still appear within the summary files. However, they will not appear as exported images!')
            self.cookie['basename'] = dirname
            self.cookie['dirList'] = [os.path.normpath(self.cookie['basename'] + os.sep + x) for x in
                                      sorted(list(n & o))]
            self.cookie['filenames'] = [os.path.split(str(x))[1] for x in self.cookie['dirList']]
            return True
        else:
            self.cookie['basename'] = basedir
            messagebox.showerror("Error",
                                 'No files were found (0 of ' + was + ')!\n\nIn case the original directory still exists, locate the missing files and copy them back into the original folder: ' +
                                 self.cookie['basename'] + '.')
            return False

    def session_reset(self, data, fname):  # debug
        data = self.recover_old_save(data)
        self.cookie_update(data['cookie'])
        self.cookie['tagsize'] = 3
        self.cookie['version'] = self.GLOBALS['VERSIONSTRING']
        if self.cookie['tagsize'] is not None:
            self.tagsize = self.cookie['tagsize']
        else:
            self.tagsize = 3  # fallback value
        self.user.set(self.cookie['user'])
        self.Sitems.set(self.cookie['Sitems'])
        self.currentSpec.set(self.cookie['currentSpec'])
        self.currentFilePos.set(self.cookie['current_file_index'])
        self.catc = self.cookie['catcounter']
        self.groupc = self.cookie['groupc']
        self.cookie['files_good'] = self.check_files(self.cookie, fname)
        if self.cookie['files_good']:
            self.dirList = []
            # self.user.set(self.cookie['user'])
            # self.Sitems.set(self.cookie['Sitems'])
            # self.currentSpec.set(self.cookie['currentSpec'])
            # self.currentFilePos.set(self.cookie['current_file_index'])
            # self.catc=self.cookie['catcounter']
            newdir = self.cookie['basename'] + os.path.sep + self.user.get()
            if not os.path.exists(newdir):
                os.makedirs(newdir)
            self.fname = os.path.split(str(self.cookie['dirList'][0]))[1]  # get filename
            self.cookie['current_file'] = self.fname
            self.cookie['current_file_index'] = self.currentFilePos.get()
            # self.groupc=self.cookie['groupc']
            # confusing from this point on!

            self.sqlite_db_creation(fname=self.cookie['dbFile'])
            self.get_sqlite_from_row(data['row'], conn=self.sqlite_conn)
            self.files_browse_exif(self.cookie)  # get and store all exif data in sqlite db
            self.redraw(size=self.cookie['tagsize'])
            self.session_on()
            self.sqlite_session_fill(conn=self.sqlite_conn)

        else:  # recovery
            answer = messagebox.askyesno("Error",
                                         'Could not restore session!\n Would you like to enter recovery mode of tag data?')
            if answer:
                self.dataDUMP(filename=fname, row=data['row'])
            else:
                messagebox.showwarning('Warning', 'Recovery mode not selected, iTAG shutting down!')
            self.quit()

    def setcat(self, event=None, INDX=None):
        key = INDX
        if INDX is None:
            key = event.char
        if self.enable:
            if key == 'x':
                self.tag_remove_entrymode = not self.tag_remove_entrymode
                if self.tag_remove_entrymode:
                    self.canvas.config(cursor=self.GLOBALS['ERASE_CURSOR'])
                    self.DEF_CURSOR = self.GLOBALS['ERASE_CURSOR']
                    print('Eraser mode on')
                    self.currentMod.set('ERASE ')
                    self.modL.configure(bg='#FF0000', fg=globalFunctions.col_invert('#FF0000'))
                else:
                    self.DEF_CURSOR = self.GLOBALS['TAG_CURSOR']
                    self.canvas.config(cursor=self.GLOBALS['TAG_CURSOR'])
                    print('Eraser mode off')
                    self.currentMod.set(self.cookie['modnames'][0])
                    self.modL.configure(bg='#C0C0C0', fg=globalFunctions.col_invert('#C0C0C0'))
            elif int(key) <= len(self.cookie['catnames']):
                self.Toolbox.activate(index=int(key)-1)
                self.spec_index = int(key) - 1
                self.cat = self.cookie['catnames'][self.spec_index]  # this should be self.category_text
                self.cookie['current_cat'] = self.cat
                self.cookie['currentSpecIndex'] = self.spec_index
                self.currentSpec.set(self.cookie['catnames'][self.spec_index])
                self.currentGroupID.set(self.groupc[self.spec_index])
                self.lG.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                                  bg=self.cookie['colours'][self.spec_index])
                self.lGcount.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                                       bg=self.cookie['colours'][self.spec_index])
                self.lCat.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                                    bg=self.cookie['colours'][self.spec_index])
                self.re_view()

    def save_output(self, connection, so=None):
        if self.Sitems.get() != 0:
            if so.out_CSV:    self.write_CSV(conn=connection, so=so)
            if so.out_SQL: self.write_SQL(conn=connection)  # switched off for now...
            if so.out_IMG: self.write_IMG(conn=connection)  # create modified pictures from self.row
            if so.out_KML:    self.write_KML(conn=connection, so=so)  # export to google earth layer
        else:
            messagebox.showwarning("Warning", self.TRANSLATION['NO_OBS'])

    def session_save(self, event=None):
        if self.Sitems.get() != 0:
            self.cookie['groupc'] = self.groupc
            out = asksaveasfilename(parent=self.mainWindow,
                                    title=self.TRANSLATION['SES_SAVE_AS'] + ": " + self.user.get(),
                                    initialdir=self.cookie['basename'],
                                    initialfile=self.user.get() + '.iT' + str(self.GLOBALS['SAVEVERSION']),
                                    defaultextension="iT" + str(self.GLOBALS['SAVEVERSION']),
                                    filetypes=[('iTAG 0.7 sessions', '.iT' + str(self.GLOBALS['SAVEVERSION'])),
                                               ('all files', '.*')])
            if out is not None and out != "":  # test for acceptable chars!
                self.cookie['endtime'] = str(datetime.datetime.utcnow())
                sql = "update session set enddate= '%s'" % (self.cookie['endtime'])
                self.sqlite_conn.execute(sql)
                self.sqlite_conn.commit()
                tag_data = self.get_row_from_sqlite(self.sqlite_conn)  # artificially create tag_data
                save = dict(row=tag_data, cookie=self.cookie)
                with open(out, 'wb') as f: pickle.dump(save, f)
                messagebox.showinfo("Info", self.TRANSLATION['SES_SAVED'] + ": " + out)
                self.save_ok = True
        else:
            messagebox.showwarning("Warning", self.TRANSLATION['OBS_EMPTY'])

    def session_load(self, event=None):  # nothing is dead that eternal lies....
        import pickle
        fname = askopenfilename(parent=self.mainWindow, title=self.TRANSLATION['CHOOSE_FILE'], initialdir=self.basename,
                                initialfile=str(self.user.get()) + '.iT' + str(self.GLOBALS['SAVEVERSION']),
                                filetypes=[('iTAG 0.7 sessions', '.iT7'), ('previous iTAG sessions', '.TiD'),
                                           ('all files', '.*')])
        if fname is not None and fname != '':
            messagebox.showinfo("Info", self.TRANSLATION['SES_RELOAD'] + " " + fname)
            try:
                with open(fname) as f:
                    data = pickle.load(f)
                loaded = True
            except:
                loaded = False
            if loaded:
                self.savename = fname
                self.session_reset(data, fname)  # boom! its gone, and boom! its back!

    def session_on(self):  # clean up
        self.canvas.config(cursor=self.GLOBALS['TAG_CURSOR'])
        self.DEF_CURSOR = self.canvas.cget('cursor')  # sets the default cursor for fallbacks

        self.filemenu.entryconfig(0, state=DISABLED)  # new session
        self.parent.unbind('<Control-n>')
        self.filemenu.entryconfig(2, state=NORMAL)  # save session
        self.parent.bind("<Control-s>", self.session_save)
        self.filemenu.entryconfig(3, state=DISABLED)  # resume session
        self.parent.unbind("<Control-o>")
        self.filemenu.entryconfig(self.filemenu.index("Exit (Ctrl-Q)"), label='End Session (Ctrl-Q)')
        self.menubar.entryconfig('View', state=NORMAL)  # switch on view menu
        self.menubar.entryconfig('Options', state=NORMAL)  # switch on view menu
        self.parent.resizable(self.parent.winfo_screenwidth(), self.parent.winfo_screenheight())

        # binds
        # view related
        self.parent.bind("<Right>", self.nextImage)
        self.parent.bind("w", self.nextImage)  # qwerty layout
        self.parent.bind("z", self.nextImage)  # azerty layout

        self.parent.bind("<Left>", self.prevImage)
        self.parent.bind("q", self.prevImage)  # qwerty layout
        self.parent.bind("a", self.prevImage)  # azerty layout

        self.parent.bind('<Up>', self.inc_groupID)
        self.parent.bind("e", self.inc_groupID)

        self.parent.bind('<Down>', self.dec_groupID)
        self.parent.bind("d", self.dec_groupID)

        self.parent.bind("m", self.toggle_magnifier)
        self.parent.bind('<Caps_Lock>', self.bypass_CAPS_LOCK)

        self.parent.bind("+", self.inc_tagsize)  # increase tagsize
        self.parent.bind("-", self.dec_tagsize)  # decrease tagsize

        # self.parent.bind("t",self.toggle_tag_edit_mode) #later... make it rectangular selection, find all tags within that rectangle find_enclosed, open window with edit options etc...

        self.master.bind("<F8>", self.toggle_tags)  # toggles tag display
        self.master.bind("<F9>", self.toggle_MultiPanel)  # toggles multi panel!!!
        # <F10> reserved for menu
        self.master.bind("<F11>", self.toggle_fs)  # toggles full screen!!!
        self.master.bind("<F12>", self.toggle_group_ID_display)  # toggles group id display!!!

        # navigational frame
        self.bFIRST.grid(row=0, column=1, padx=1, pady=1)
        self.bPREV.grid(row=0, column=2, padx=1, pady=1)
        self.bGOTO.grid(row=0, column=3, padx=1, pady=1)
        self.tGOTO.grid(row=0, column=4, padx=1, pady=1)
        self.bNEXT.grid(row=0, column=5, padx=1, pady=1)
        self.bLAST.grid(row=0, column=6, padx=1, pady=1)
        self.statusFrame.pack(side=LEFT, anchor=W, fill=X)
        self.tnav.pack(side=RIGHT, anchor=E)

        #self.SpecBtn = []
        self.Toolbox = ButtonFrame(self.cookie)
        self.Toolbox.bind('<<Event_CatSelected>>', lambda e: self.setcat(INDX = e.widget.getAttributes('index')+1))
        self.Toolbox.bind('<<RequestShutdown>>', self.session_end)
        #self.Toolbox.bind('<<Event_CatNameChange>>', lambda e: self.setcat(INDX=e.widget.getAttributes('index') + 1))
        #self.Toolbox.bind('<<Event_CatColourChange>>', lambda e: self.setcat(INDX=e.widget.getAttributes('index') + 1))

        self.skipBTN = Checkbutton(self.image_flagging, text="Skip this Image in this session",
                                   command=self.toggle_skip_files_flag, foreground='red', variable=self.skip_files_flag,
                                   onvalue=True, offvalue=False)
        # self.skipBTN.pack() #not yet

        zoom_Label = Label(self.global_zoom, text='Zoom to: ')
        self.global_zoom_select = OptionMenu(self.global_zoom, self.global_zoom_var, 100, 90, 80, 70, 60, 50, 40, 30,
                                             20, 10)
        self.global_zoom_watcher = self.global_zoom_var.trace('w', self.zoom_global)
        self.global_zoom_select['menu'].config(bg='grey')
        self.global_zoom_select.pack(side=RIGHT)
        zoom_Label.pack(side=RIGHT)

        self.fcat.pack(side=LEFT)
        self.global_zoom.pack(side=RIGHT)
        self.image_flagging.pack(side=RIGHT)

        self.f_lower.pack(side=BOTTOM, fill=X)
        self.cookie['starttime'] = str(datetime.datetime.utcnow())  # utc
        self.currentMod.set(self.cookie['modnames'][0])
        self.tags_locked = True
        #attention: self.cookie['params'] now dynamic length
        #includes self.cookie['params'] and self.cookie['params_values']
        tag = dict(username=self.cookie['user'], filecount=len(self.cookie['dirList']),
                   startdate=self.cookie['starttime'], enddate="", current_filename=str(self.cookie['current_file']),
                   maxsize=self.GLOBALS['MAXSIZE'],
                   #para1=self.cookie['params'][0], para2=self.cookie['params'][1],
                   #para3=self.cookie['params'][2], para4=self.cookie['params'][3], para5=self.cookie['params'][4],
                   #para6=self.cookie['params'][5], para7=self.cookie['params'][6], para8=self.cookie['params'][7],
                   #para9=self.cookie['params'][8],
                   Version=self.GLOBALS['VERSIONSTRING'])
        self.conn.insertRow(tableName='session', dictionary=tag)
        self.enable = True  # this important!
        #self.setcat(INDX=1)  # set first category

    def bypass_CAPS_LOCK(self, event=None):
        try:
            import SendKeys
            if event.state == 0:
                SendKeys.SendKeys("""{CAPSLOCK}""")
        except:
            messagebox.showerror("Error", 'library SendKeys was not loaded')

    def zoom_global(self, index=None, value=None, op=None):
        filename = self.cookie['current_file']
        zoom_scale = float(self.global_zoom_var.get()) / 100
        sql = 'update files set zoom_scale= %f where filename ="%s"' % (zoom_scale, filename)
        self.sqlite_conn.execute(sql)
        self.redraw(size=self.tagsize)
        if self.pop.get():
            self.panel.update(self.cookie, index=0, gpsdict=self.IMAGEDATA)

    # def sqlite_db_creation(self, fname):
    #     fname = os.path.normpath(fname)
    #     self.sqlite_conn = sqlite3.connect(fname)
    #     self.cookie['dbFile'] = fname
    #
    #     sql = "drop table if exists session"
    #     self.sqlite_conn.execute(sql)
    #     sql = "create table if not exists session('username' string,'filecount' string,'startdate' string,'enddate'  string,'current_filename' string,maxsize string,para1 string,para2 string,para3 string,para4 string,para5 string,para6 string,para7 string, para8 string,para9 string,version string)"
    #     self.sqlite_conn.execute(sql)
    #
    #     sql = "drop table if exists files"
    #     self.sqlite_conn.execute(sql)
    #     sql = "create table if not exists files('ID' BIGINT KEY UNIQUE,'basename' string, 'filename' string ,'xsize' string,'ysize'  string,'image_mode' string,'file_scale' string,  'zoom_scale' string,'global_FX' string,'file_tagsize' string,'skip_file' string,'Valid_Exif' string, 'ISOSpeedRatings' string, 'ExifVersion' string,'Valid_GPS' string,'coord_ref' string, 'lat' string,'lon' string,'altitude' string,'gps_date' string,'DateTime' string,'DateTimeOriginal' string, 'DateTimeDigitized' string, 'FocalLength' string, 'Model' string, 'Make' string,'comment' string DEFAULT '')"
    #     self.sqlite_conn.execute(sql)
    #
    #     sql = "drop table if exists detailed"
    #     self.sqlite_conn.execute(sql)
    #     sql = "create table if not exists detailed('ID' BIGINT,'username' string,'filename' string,'xpos' string,'ypos'  string,'category' string,'category_index' string,'modifier' int,'count' string,'colour' string,'species_index' string,'group_ID' string,'tagsize' string,'lat' string,'lon' string,'altitude' string,'gps_date' string,'cam_date' string,'save_date' string,'comment' string DEFAULT '')"
    #     self.sqlite_conn.execute(sql)
    #     self.sqlite_conn.commit()  # maybe not neccessary

    # def sqlite_session_fill(self):
    #     tag = dict(username=self.cookie['user'], filecount=len(self.cookie['dirList']),
    #                startdate=self.cookie['starttime'], enddate="", current_filename=str(self.cookie['current_file']),
    #                maxsize=self.GLOBALS['MAXSIZE'], para1=self.cookie['params'][0], para2=self.cookie['params'][1],
    #                para3=self.cookie['params'][2], para4=self.cookie['params'][3], para5=self.cookie['params'][4],
    #                para6=self.cookie['params'][5], para7=self.cookie['params'][6], para8=self.cookie['params'][7],
    #                para9=self.cookie['params'][8], Version=self.GLOBALS['VERSIONSTRING'])
    #     self.conn.insertRow(tableName='session', dictionary = tag)

    def bSetCat(self, INDX=1):
        INDX -= 1
        if int(INDX) <= len(self.cookie['catnames']):
            self.spec_index = int(INDX) - 1
            self.cat = self.cookie['catnames'][self.spec_index]  # this should be self.category_text
            for i in range(0, len(self.cookie['catnames'])):
                self.SpecBtn[i].configure(relief=RAISED)
            self.SpecBtn[INDX].configure(relief=SUNKEN)
            self.spec_index = int(INDX)
            self.cat = self.cookie['catnames'][self.spec_index]  # this should be self.category_text
            self.currentSpec.set(self.cookie['catnames'][self.spec_index])
            self.cookie['currentSpec'] = self.currentSpec.get()
            self.cookie['currentSpecIndex'] = self.spec_index
            self.currentGroupID.set(self.groupc[INDX])
            self.lG.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                              bg=self.cookie['colours'][self.spec_index])
            self.lCat.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                                bg=self.cookie['colours'][self.spec_index])
            self.lGcount.configure(fg=globalFunctions.col_invert(self.cookie['colours'][self.spec_index]),
                                   bg=self.cookie['colours'][self.spec_index])
            self.re_view()

    def fallback(self):
        self.species = self.cookie['catnames']
        self.alttext = self.cookie['modnames']
        self.user = self.cookie['user']
        self.params = self.cookie['params']
        self.colours = self.cookie['colours']
        self.basename = self.cookie['basename']
        self.dirList = self.cookie['dirList']

    def recover_old_save(self, data):
        # version 5 seems to be working!
        # 6 maybe as well..
        # check what happens when group_ID is needed
        version = 5
        out = {}
        try:
            version = data['cookie']['version']
        except:
            version = 5
        print(version)
        if version == 5:
            print('recovery of 0.5.x')
            out['basename'] = os.path.dirname(data['dirList'][0])
            out['cextent'] = ''
            out['currentSpec'] = data['cat']
            out['modnames'] = data['alttext']
            out['full_version_string'] = self.TRANSLATION['VERSIONSTRING']
            out['catcounter'] = data['catc_count']
            out['scale'] = 1
            out['catnames'] = data['leg']
            out['currentSpecIndex'] = 0
            out['current_file_index'] = data['position']
            out['current_cat'] = out['catnames'][out['currentSpecIndex']]
            out['colours'] = data['cols']
            out['maxsize'] = self.GLOBALS['MAXSIZE']
            out['params'] = ['' for x in range(0, 9)]
            out['Sitems'] = data['Sitems']
            # print data['Sitems']
            out['file_scale'] = 1
            out['dirList'] = [os.path.normpath(x) for x in data['dirList']]
            out['os_name'] = OS
            out['panel_canvas_size'] = 500
            out['user'] = data['User']  # maybe check for illegal chars?
            out['dbFile'] = out['basename'] + '/' + out['user'] + '/' + out['user'] + '_DB.db'
            out['filenames'] = [os.path.split(str(x.lower()))[1] for x in out['dirList']]  # file names
            out['filenames'] = sorted(out['filenames'])
            out['endtime'] = ''
            out['ID'] = data['ID']
            out['shortpath'] = ''
            out['newdir'] = ''  # whats that???
            out['starttime'] = ''
            out['current_file'] = str(os.path.basename(out['dirList'][out['current_file_index']]))
            self.groupc = []
            self.catc = []
            for i in range(0, len(out['catnames'])):
                self.catc.append([0, 0, 0, 0])
                self.groupc.append(1)
            out['catc'] = self.catc
            out['groupc'] = self.groupc

            # reorder row elements so it fits!
            r = data['row']
            row2 = []
            for row in r:
                row2.append(
                    [row[10], out['user'], str(row[1]).lower(), row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                     row[5], 1, row[13], row[14], '', row[16], row[15], 3])  # group_ID set to 1
            data = {}
            data['cookie'] = out
            data['row'] = row2
        elif version == 6 or isinstance(version, basestring):
            print('recovery of 0.6.x')
            out = data['cookie']
            out['dbFile'] = out['basename'] + '/' + out['user'] + '/' + out['user'] + '_DB.db'
            self.groupc = []
            self.catc = []
            for i in range(0, len(out['catnames'])):
                self.catc.append([0, 0, 0, 0])
                self.groupc.append(1)
            out['catc'] = self.catc
            out['groupc'] = self.groupc

            # reorder row elements so it fits!
            r = data['row']
            row2 = []
            for row in r:
                row2.append(
                    [row[10], out['user'], str(row[1]).lower(), row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                     row[5], 1, row[13], row[14], '', row[16], row[15], 3])  # sets group id automatically to 1
            data = {}
            data['row'] = row2
            data['cookie'] = out
        elif version == 7:
            print('recovery of 0.7.x')
        return data

    def _NULL(self):
        pass

    def buttonPress(self,Event = None):
        print(Event.widget.getAttributes())