# -*- coding: UTF-8 -*-
# this is wip to bring up to python 3.5
# csv export and buttons are wrong, amongst other things
import os
import pickle
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
from tkinter import messagebox

#user files
from lib import globalFunctions

#self.catnames needs to be 20,  first are as defined, remaining ones are generic
# idea: change first slide so that user can edit up to 9 extra columns per image, ut add a notes field for generic stuff!

class Wizard(Toplevel):  # clean up
    def __init__(self, parent, PARAMETERDICT, wiztitle='', suffix='jpg'):
        self.NoParams = 12
        self.GLOBALS=PARAMETERDICT[0]
        self.TRANSLATION = PARAMETERDICT[1]
        self.smallfont = self.GLOBALS['SMALLFONT']  # adapt for different OS
        self.parent = parent
        self.BTN1Names = 'Cancel'
        self.BTN2Names = 'Back'
        self.BTN3Names = [None, 'Start', 'Next', 'Next', 'Next', 'Done']
        self.right_side = []  # empty slide list
        self.suffix = suffix
        self.data_col = '#DBDBDB'
        # self.data_col='red'
        self.text_col = '#F2F2F2'
        self.title_button_col = '#D6D6D6'

        # defaults
        self.odir = self.GLOBALS['PROGDIR']
        self.initVars()
        self.restore_opt(type=1)  # restore default options
        self.initUI(wiztitle)

    def initUI(self,wiztitle):
        Toplevel.__init__(self, self.parent)
        self.title(wiztitle)
        self.iconbitmap(self.GLOBALS['ICONPATH'])
        self.grab_set()
        self.initial_focus = self
        self.initial_focus.focus_set()
        self.protocol("WM_DELETE_WINDOW", self._CANCEL)
        self.geometry("650x385")  # later - 9 cats take up 301 pix
        self.geometry("900x700")  # later - 9 cats take up 301 pix
        self.resizable(0, 0)

        self.cImage = [os.path.join(self.GLOBALS['RESPATH'], 'wiz1.png'),
                       os.path.join(self.GLOBALS['RESPATH'], 'wiz2.png'),
                       os.path.join(self.GLOBALS['RESPATH'], 'wiz3.png'),
                       os.path.join(self.GLOBALS['RESPATH'], 'wiz4.png'),
                       os.path.join(self.GLOBALS['RESPATH'], 'wiz5.png')]
        self.img = ImageTk.PhotoImage(Image.open(self.cImage[0]))  # open the first image!
        self.w, self.h = Image.open(self.cImage[0]).size
        self.h2 = self.winfo_height() - self.w
        self.w2 = self.winfo_width() - self.w

        self.slide = Frame(self, relief=SUNKEN, bd=1, bg=self.text_col, width=self.winfo_width(),
                           height=self.winfo_height() - 30)
        self.bg = self.slide["bg"]  # get that neutral grey

        self.slide_name = Label(self, text=self.slidenames[1], anchor="e", relief=FLAT, bg=self.title_button_col)
        self.font = self.slide_name.cget('font')

        self.leftside = Frame(self.slide, relief=FLAT, bd=1, width=self.w, height=self.h,
                              bg=self.title_button_col)  # need to resize all images to 355
        self.canvas = Canvas(self.leftside, bd=0, bg=self.bg)
        self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.canvas.pack(side=LEFT, fill=BOTH, anchor='nw')

        self.bFrame = Frame(self, bd=2, relief=FLAT, bg=self.title_button_col, height=30)
        self.bBTN1 = Button(self.bFrame, text='Cancel', command=self._BTN1, anchor=W, relief=GROOVE,
                            bg=self.title_button_col)
        self.bBTN2 = Button(self.bFrame, text='Back', command=self._BTN2, anchor=E, relief=GROOVE,
                            bg=self.title_button_col, state=DISABLED)
        self.bBTN3 = Button(self.bFrame, text='Next', command=self._BTN3, anchor=E, relief=GROOVE,
                            bg=self.title_button_col)
        self.bBTN1.pack(side=LEFT)
        self.bBTN3.pack(side=RIGHT)
        self.bBTN2.pack(side=RIGHT)

        for i in range(1, 6):
            self.init_slide(i)  # sets up dummy references

        self.slide_name.pack(side=TOP, fill=X)
        self.leftside.pack(side=LEFT)
        self.leftside.pack_propagate(0)

        self.right_side = self.init_slide(1)
        self.right_side.pack(side=LEFT, fill=X)
        self.bFrame.pack(side=BOTTOM, fill=X)
        self.slide.pack(fill=X)
        self.right_side.pack_propagate(0)

    def init_slide(self, index=0):
        if index == 0:
            print("why?")
        elif index == 1:
            return self.init1st()
        elif index == 2:
            return self.init2nd()
        elif index == 3:
            return self.init3rd()
        elif index == 4:
            return self.init4th()
        elif index == 5:
            return self.init5th()

    def init1st(self):
        rightside = Frame(self.slide, bd=0, bg=self.data_col, relief=GROOVE, width=self.winfo_width(),
                          height=self.winfo_height() - 30)
        textFrame = Frame(rightside, bd=0, relief=FLAT)

        t = Text(textFrame, bd=0, wrap=WORD, background=self.bg, font=self.font)
        t.insert(END,
                 'Welcome to iTAG!\n\nThis Session Wizard will guide you through the setup of your tagging session. You will be able to define all the properties of your session. In order to produce usable output, you will have to provide information on your user name and the tags you wish to use. If you want to, you can also supply additional info on your survey such as random comments like the weather situation etc.\n\nAs long as your images are compliant with EXIF standards, the output will contain detailed spatial and temporal information.\n\nYou can also define your default session and save it for latter uses, setting it as the default for iTAG on loadup.')
        t.configure(state=DISABLED)
        t.pack(side=TOP, fill=X)

        bB = Button(rightside, text='load factory defaults', command=lambda type='defaults': self.restore_opt(type),
                    anchor=E, state=ACTIVE, relief=GROOVE)
        bBl = Button(rightside, text='load options...', command=self.restore_opt, anchor=E, state=ACTIVE, relief=GROOVE)
        bB.pack(side=BOTTOM, anchor='e')
        bBl.pack(side=BOTTOM, anchor='e')

        textFrame.pack(side=TOP, anchor=W, fill=BOTH)
        return rightside

    def init2nd(self):
        rightside = Frame(self.slide, bd=0, relief=GROOVE, bg=self.data_col, width=self.winfo_width(),
                          height=self.winfo_height() - 30)

        userFrame = Frame(rightside, bd=0, bg=self.data_col,relief=RAISED)
        t = Text(userFrame, wrap=WORD, background=self.bg, font=self.font, height=10)
        t.insert(INSERT,'Please provide a valid Username that will be used throughout your session.\nValid characters '
                      'are a-z äöü _ 0-9, both upper and lower case letters are accepted. \n\nRemember: iTAG is most useful when multiple people '
                      'analyse the same set of images. Providing meaningful usernames can help you sort out '
                      'differences once you have produced your output.')
        t.configure(state=DISABLED)
        t.pack(side=TOP, fill=X)
        UserEntry = Frame(userFrame,bd=0, bg=self.data_col,relief=RAISED)
        ul = Label(UserEntry, text="Username: ", justify="left", bg=self.data_col,height=2)
        self.user_e = Entry(UserEntry, textvariable=self.user, width=32)
        ul.grid(row=0, column=0)
        self.user_e.grid(row=0, column=1)
        UserEntry.pack(side=LEFT,fill=X)

        paraFrame = Frame(rightside, bd=5, bg=self.data_col)
        t = Text(paraFrame, wrap=WORD, background=self.bg, font=self.font, relief=FLAT,height=2)
        t.insert(END,'You can add up to {0} additional columns that you might wish to edit per image.'.format(str(self.NoParams)))

        t.configure(state=DISABLED)
        t.pack(side=TOP, fill=X)

        ParaEntry=Frame(paraFrame)
        self.para_e = []
        print(self.NoParams)
        for i in range(0, self.NoParams):
            print(self.para[i])
            ll = Label(ParaEntry, text="Extra Column " + str(i + 1) + ": ", relief="flat", justify="left",
                       bg=self.data_col)
            self.para_e.append(Entry(ParaEntry, width=40))
            ll.grid(row=i + 1, column=0)
            self.para_e[i].grid(row=i + 1, column=1)
            self.para_e[i].insert(END, self.para[i])
        ParaEntry.pack(side=TOP,fill=X)
        userFrame.pack(side=TOP,fill=X)
        paraFrame.pack(side=TOP,fill=BOTH)

        return rightside

    def init3rd(self, type=0):
        # get image directory
        rightside = Frame(self.slide, bd=0, bg=self.data_col, relief=GROOVE, width=self.winfo_width(),
                          height=self.winfo_height() - 30)
        textFrame = Frame(rightside, relief=FLAT, bd=0)
        userFrame = Frame(rightside, bd=0, bg=self.data_col)

        t = Text(textFrame, wrap=WORD, background=self.bg, font=self.font, relief=FLAT)
        t.insert(END,
                 "Please select the directory that contains the images you would like to analyse.\nOnce the session setup is complete, iTAG will create a subfolder in that specific directory where all the output will be stored. Special characters such as ä's, ö's and ü's are neither allowed in pathnames nor in filenames.\n\nIt is good practice to organize your images in sets and copy these into a seperate folder for each survey.\n\nThe maximum width / height per image that iTAG will try to open is set to " + str(
                     self.GLOBALS['MAXSIZE']) + ". You can increase or decrease this value by invoking iTAG with the -m command line parameter, e.g.:\nitag.exe -m2000 \nThis would set the maximum width / height of images to 2000 pixel. iTAG will try to resize any image (preserving the aspect ratio) to comply with that limit.")
        t.configure(state=DISABLED)
        t.pack(side=TOP, fill=X)

        oB = Button(userFrame, text='Choose Directory', command=self.openDir, relief=GROOVE)
        oB.pack(side=BOTTOM, anchor=E)

        paraFrame = Frame(userFrame, relief=FLAT, bd=0, bg=self.data_col)
        i = 0
        for name in sorted(self.fparameter):
            ll = Label(paraFrame, text=name, relief=FLAT, justify="left", bg=self.data_col)
            ll.grid(row=i, column=0, sticky=NW)
            ll = Label(paraFrame, text=self.fparameter[name], relief=FLAT, justify="left", bg=self.data_col)
            ll.grid(row=i, column=1, sticky=NW)
            i += 1
        paraFrame.pack(side=BOTTOM, fill=X)
        userFrame.pack(side=BOTTOM, fill=BOTH)
        textFrame.pack(side=TOP, fill=X)
        return rightside

    def init4th(self):
        rightside = Frame(self.slide, bd=0, bg=self.data_col, relief=GROOVE, width=self.winfo_width(),
                          height=self.winfo_height() - 30)
        centerFrame = Frame(rightside, relief=GROOVE, bd=2, width=460, height=self.winfo_height() - 30,
                            bg=self.data_col)
        textFrame = Frame(rightside, relief=FLAT, bd=0)
        t = Label(textFrame,
                  text='Please provide information about the Tags you are going to use.\nYou can specify up to 9 different Tags and assign individual colours to them.\nYou can also change the names for the modifier keys.',
                  relief=FLAT, justify='left')
        t.pack(side=LEFT, fill=BOTH, anchor='w')

        countFrame = Frame(centerFrame, bg=self.data_col)
        tagFrame = Frame(centerFrame, bg=self.data_col)
        catFrame = Frame(tagFrame, relief=GROOVE, bd=0, bg=self.data_col)
        altFrame = Frame(tagFrame, relief=GROOVE, bd=0, bg=self.data_col)

        # tag & colour picker
        self.cats = []  # category names
        self.cat_e = []  # category entries
        self.bCol = []  # color picker buttons
        self.key = []  # numerical keys
        self.no_cats = StringVar()  # number of categories
        self.no_cats.set(len(self.catnames))

        self.catcounter = Spinbox(countFrame, from_=1, to=9, width=3, textvariable=self.no_cats)

        self.lCat = Label(countFrame, text='Number of categories: ', bg=self.data_col)
        self.catcounter.pack(side=RIGHT)
        self.lCat.pack(side=RIGHT)

        names = ['Key', 'Colour', 'Name']
        for i in range(0, 3):
            Label(catFrame, text=names[i], bg=self.data_col).grid(row=2, column=i, sticky=NW + SE)
        for i in range(0, len(self.catnames)):
            self.cats.append(StringVar())
            self.cats[i].set(self.catnames[i])
            self.key.append(Label(catFrame, text=str(i + 1) + ": ", relief=FLAT, justify="left", bg=self.data_col))
            self.bCol.append(
                Button(catFrame, bg=self.colours_palette[i], command=lambda i=i: self.colCHOOSE(index=i), relief=SUNKEN,
                       width=5))
            self.cat_e.append(Entry(catFrame, textvariable=self.cats[i], bg=self.data_col, width=34))
            self.key[i].grid(row=i + 5, column=0, sticky=W)
            self.bCol[i].grid(row=i + 5, column=1, sticky=W)
            self.cat_e[i].grid(row=i + 5, column=2, sticky=W + E)

        self.alts = []  # alt names
        self.alt_e = []  # alt entries
        modifier = ['None', 'Shift', 'Control', 'Alt']
        self.alt_key = []  # numerical keys
        Label(altFrame, text='Modifier key', bg=self.data_col).grid(row=0, column=0)
        Label(altFrame, text='Subcategory', bg=self.data_col).grid(row=0, column=1)

        for i in range(0, len(modifier)):
            self.alts.append(StringVar())
            self.alts[i].set(self.modnames[i])
            self.alt_key.append(
                Label(altFrame, text=str(modifier[i]) + ": ", relief=GROOVE, justify="left", bg=self.data_col))
            self.alt_e.append(Entry(altFrame, textvariable=self.alts[i]))
            self.alt_key[i].grid(row=i + 1, column=0, sticky=NW + SE)
            self.alt_e[i].grid(row=i + 1, column=1, sticky=NW + SE)
        altFrame.grid(row=1, column=0, sticky=N)
        catFrame.grid(row=1, column=1, sticky=N)

        textFrame.pack(side=TOP, fill=BOTH, expand=0)
        countFrame.pack(side=TOP, fill=X, anchor='e')
        tagFrame.pack(side=TOP, fill=X, anchor='n')
        centerFrame.pack(fill=BOTH)
        centerFrame.pack_propagate(0)
        self.updateValues()  # we should use self.out

        return rightside

    def init5th(self):
        self.updateValues()
        rightside = Frame(self.slide, bd=0, relief=GROOVE, width=self.winfo_width(), height=self.winfo_height() - 30)

        # check for duplicate cat names
        wrn = ''
        catnames = [x.lower() for x in self.catnames]
        dups = [i for i, x in enumerate(catnames) if catnames.count(x) > 1]
        if len(dups) > 0:
            for i in range(1, len(dups)):
                if len(self.catnames[dups[i]]) > 32:
                    self.catnames[dups[i]] = self.catnames[dups[i]][:-2]
                self.catnames[dups[i]] = self.catnames[dups[i]] + '_' + str(i)
                self.cat_e[dups[i]].delete(0, END)
                self.cat_e[dups[i]].insert(0, self.catnames[dups[i]])

            wrn = "\n\nWARNING: There were duplicate category names that have been amended for (see below). If you wish to make changes to these categories yourself, please go back to the previous slide and change the categories accoridngly. Otherwise, the categories will be set up as shown below.\n\n"
        textFrame = Frame(rightside, relief=FLAT, bd=0)
        t = Text(textFrame, wrap=WORD, background=self.bg, font=self.font)
        t.insert(END,
                 'Congratulations, you have finished setting up your session!\nYou will find all the relevant info on your session set up below.' + wrn)
        t.configure(state=DISABLED)
        t.pack(side=LEFT, fill=BOTH, anchor='w')

        centerFrame = Frame(rightside, relief=FLAT, bd=0, bg=self.data_col)
        ll = Label(centerFrame, text="Username: " + self.user.get(), relief="flat", justify="left", bg=self.data_col)
        ll.grid(row=0, column=0, columnspan=2, sticky=S + W)
        i = 0
        for (name, value) in self.fparameter.items():
            ll = Label(centerFrame, text=name + str(value), relief=FLAT, justify="left", bg=self.data_col)
            ll.grid(row=i + 1, column=0, columnspan=2, sticky=S + W)
            i += 1
        for j in range(0, len(self.catnames)):  # this should "wrap" labels at widget border
            ll = Label(centerFrame, text=self.catnames[j], font=self.smallfont, relief=GROOVE, justify="left",
                       bg=self.colours_palette[j], fg=globalFunctions.col_invert(self.colours_palette[j]))
            ll.grid(row=j, column=2, sticky=S + W + E)
        ll = Label(centerFrame, text="Modifiers: " + ', '.join(self.modnames), relief="flat", justify="left",
                   bg=self.data_col)
        ll.grid(row=i + 1, column=0, columnspan=2, sticky=S + W)

        optFrame = Frame(rightside, bg=self.data_col)

        Button(optFrame, text='Save settings...', command=lambda i=1: self.save_opt(i), relief=GROOVE).grid(row=0,
                                                                                                            column=0,
                                                                                                            sticky=W)

        Button(optFrame, text='Save as default settings', command=self.save_opt, relief=GROOVE).grid(row=0, column=1,
                                                                                                     sticky=W)
        optFrame.pack(side=BOTTOM, fill=X, anchor=E)
        centerFrame.pack(side=BOTTOM, fill=BOTH)
        textFrame.pack(side=TOP, fill=X, anchor=E)
        return rightside

    def set_new_rightside(self, type, rightside):
        if type == 0:
            self.right_side.append(rightside)
        else:
            self.right_side[type - 1] = rightside

    def catnumbers(self, why, now, new):
        self.updateValues()
        pattern = r'[0-9]'  # allowed characters
        if re.search(pattern, new):
            now = int(now)
            new = int(new)
            if (new > now and new < 10):
                self.newobj += 1
                self.catnames.append('new Object ' + str(self.newobj))  # add new object
            # self.colours.append("#FFAAFF") #add new colour
            elif (now > 1 and new < now):
                self.newobj -= 1
                self.catnames.pop()  # remove last object
            # self.colours.pop() #remove last colour

            # ugly workaround:
            self.right_side.pack_forget()
            self.right_side = self.init_slide(self.count)
            self.right_side.pack(side=LEFT, fill=X)
            self.redraw()
            return True
        else:
            return False

    def redraw(self):  # redraw specific slide
        self.title(self.wintitles[self.count])
        self.slide_name.configure(text=self.slidenames[self.count])
        self.bBTN2.configure(state=NORMAL)
        self.bBTN3.configure(text=self.BTN3Names[self.count], command=self._BTN3, state=NORMAL)
        self.img = ImageTk.PhotoImage(Image.open(self.cImage[self.count - 1]))  # open the next image!
        self.canvas.itemconfig(1, image=self.img)
        self.updateValues()  # we should use self.out
        self.right_side.pack_forget()
        self.right_side = self.init_slide(self.count)
        self.right_side.pack(side=LEFT, fill=X)
        self.right_side.pack_propagate(0)

        if self.count == 1:
            self.slide_name.configure(text='Welcome to iTAG')
            self.bBTN2.configure(state=DISABLED)

        elif self.count == 2:  # username slide
            if len(self.user_e.get()) <= 0: self.bBTN3.config(state=DISABLED)
            self.okayUser = self.register(self.check_username)
            self.user_e.configure(validate='key', validatecommand=(
            self.okayUser, '%i', '%S', '%P'))  # $i is why %S is the new character, %P the new var

        elif self.count == 3:  # file open slide
            if not self.files_good:
                self.bBTN3.config(state=DISABLED)
            else:
                self.bBTN3.config(state=NORMAL)

        elif self.count == 4:  # tag slide
            for i in range(0, len(self.catnames)):
                if len(self.cat_e[i].get()) <= 0: self.bBTN3.config(state=DISABLED)
            for i in range(0, len(self.modnames)):
                if len(self.alt_e[i].get()) <= 0: self.bBTN3.config(state=DISABLED)
            self.okayCat = self.register(self.check_catname)
            self.change_cats = self.register(self.catnumbers)
            self.okayUser = self.register(self.check_username)
            self.catcounter.configure(validate='key', validatecommand=(
            self.change_cats, '%i', '%s', '%P'))  # $i is why %S is the new character, %P the new var
            for i in range(0, len(self.catnames)):
                self.cat_e[i].configure(validate='key', validatecommand=(
                self.okayCat, '%i', '%S', '%P'))  # $i is why %S is the new character, %P the new var
            for i in range(0, len(self.modnames)):
                self.alt_e[i].configure(validate='key', validatecommand=(
                self.okayUser, '%i', '%S', '%P'))  # $i is why %S is the new character, %P the new var
        elif self.count == 5:  # final slide
            self.bBTN3.configure(command=self._done)

    def _BTN1(self):  # cancel button
        self.destroy()

    def _BTN2(self):  # back button
        self.updateValues()  # we should use self.out
        self.count -= 1
        self.redraw()

    def _BTN3(self):  # what happens when you click button 3?
        self.updateValues()  # we should use self.out
        Proceed = True
        if self.count == 4:
            if any(len(t) == 0 for t in self.modnames) or any(len(t) == 0 for t in self.catnames):
                print(self.modnames)
                print(self.catnames)
                try:
                    pos1 = self.catnames.index('')
                # self.cat_e[pos1].config(bg='red')
                except:
                    pass
                try:
                    pos2 = self.modnames.index('')
                # self.alt_key[pos2].config(bg='red')
                except:
                    pass
                messagebox.showwarning("Warning", 'Please make sure that there are no empty modifiers or categories')
                Proceed = False
        if Proceed:
            self.count += 1
            self.redraw()

    def check_username(self, why, new, now, limit=32):
        pattern = r'[.a-z0-9_]'  # allowed characters
        print(now)
        print(new)
        if len(now) == 0:
            self.bBTN3.configure(state=DISABLED)
            return True
        elif len(now) > limit:  # limit to 13 characters (for now)
            self.bBTN3.configure(state=NORMAL)
            return False
        elif re.search(pattern, new.lower()):
            self.bBTN3.configure(state=NORMAL)
            return True
        else:
            self.bBTN3.configure(state=DISABLED)
            return False

    def check_catname(self, why, new, now):
        pattern = r'[.üöäa-z0-9\ ]'  # allowed characters
        if len(now) == 0:  # there is a weird bug in here; gets overridden if cat changes
            self.bBTN3.configure(state=DISABLED)
            return True
        elif len(now) > 34:  # limit to 21 characters (for now)
            self.bBTN3.configure(state=NORMAL)
            return False
        elif re.search(pattern, new.lower()):
            self.bBTN3.configure(state=NORMAL)
            return True
        else:
            self.bBTN3.configure(state=DISABLED)
            return False

    def _done(self):
        self.updateValues()
        # print (self.dirList)
        self.result = True
        self.destroy()

    def _CANCEL(self):
        self.result = False
        os.chdir(self.odir)
        self.destroy()

    def _NULL(self):
        pass

    def openDir(self):  # okish - needs support for different suffixes of jpg... doesn't allow special chars in path
        dirname = askdirectory(parent=self.leftside, initialdir=os.getcwd(), title='Choose directory')
        if len(dirname) > 0:
            dirname = os.path.normpath(dirname)
            self.dirList = [dirname + os.sep + f for f in os.listdir(dirname) if
                            re.search(r'.*\.(jpg|JPG|bmp|BMP)$', f)]
            if len(self.dirList) <= 0:
                self.files_good = False
                messagebox.showinfo("Info", 'No files found')
            else:
                # sort by filename
                self.dirList = sorted(self.dirList, key=lambda x: (int(re.sub('\D', '', x)), x))
                try:
                    self.basename = os.path.normpath(os.path.split(str(self.dirList[0]))[0])  # change cwd
                except:
                    messagebox.showinfo("Error",
                                        'Please stick to the range of allowed characters in your path / filename')
                    return
                self.fname = os.path.split(str(self.dirList[0]))[1]
                os.chdir(self.basename)
                path = self.basename.split(os.path.sep)
                m = len(path)
                if m > 3:
                    self.shortpath = os.path.join('...',path[m - 4] ,path[m - 3] ,path[m - 2] ,path[m - 1])+os.path.sep
                else:
                    self.shortpath = self.basename
                self.updateValues()
                self.fparameter['Directory: '] = self.shortpath
                suffix = ['*' + os.path.splitext(f)[1].lower() for f in self.dirList]
                suffix = list(set(suffix))
                suffix = ', '.join(map(str, suffix))
                self.fparameter['File type: '] = suffix  # this should be a list of all found extensions!
                # self.fparameter['File type: '] = '*.'+self.suffix #this should be a list of all found extensions!
                self.fparameter['File Count: '] = len(self.dirList)
                self.fparameter['First File: '] = self.out['filenames'][0]
                self.fparameter['Last File: '] = self.out['filenames'][-1]
                self.files_good = True
                self.redraw()

    def updateValues(self):
        self.para = []
        for i in range(0, self.NoParams):
            self.para.append(self.para_e[i].get())
        self.out = {}
        self.catnames = [x.get() for x in self.cat_e]
        self.modnames = [x.get() for x in self.alt_e]
        self.out['user'] = self.user.get()  # username
        self.out['catnames'] = self.catnames  # categories
        self.out['modnames'] = self.modnames  # modnames
        self.out['params'] = [var for var in self.para if var] #self.para # extra parameters
        self.out['params_value'] = [None for var in self.para] #self.para # extra parameters
        self.out['colours_palette'] = self.colours_palette
        self.out['colours'] = self.colours_palette[0:len(self.catnames)]  # extra parameters
        self.out['basename'] = self.basename  # extra parameters
        self.out['dirList'] = self.dirList  # extra parameters
        self.out['filenames'] = [os.path.split(str(x.lower()))[1] for x in self.dirList]  # file names
        self.out['dirList'] = [os.path.join(self.out['basename'], x) for x in self.out['filenames']]
        self.out['newdir'] = os.path.join(self.basename,self.user.get())
        self.out['tagsize'] = 6
        self.out['os_name'] = self.GLOBALS['OS']
        self.out['shortpath'] = self.shortpath

    def restore_opt(self, type=None):
        success = False
        out = ''
        if type == 'defaults':
            self.initVars()
            for i in range(2, 6):
                self.init_slide(i)
        if type == 1:
            out = os.path.normpath(os.path.join(self.odir, "RES", 'default_setup.TiO'))
        if type == None:
            out = askopenfilename(parent=self, title=self.TRANSLATION['CHOOSE_FILE'], initialdir=self.odir,
                                  filetypes=[('Image Tag Options', '.TiO'),
                                             ('all files', '.*')])  # gets covered / too large
        if out != '':
            try:
                with open(out) as f:
                    data = pickle.load(f)
                success = True
            except:
                messagebox.showinfo("Info", 'Could not load Options from: ' + out)
                success = False
            if success:
                self.out = data
                self.para = self.out['params']  # extra parameters
                self.catnames = self.out['catnames']
                self.modnames = self.out['modnames']
                self.user.set(self.out['user'])
                self.colours_palette = self.out['colours_palette']  # extra parameters
                self.tagsize = 1
                if type == None:
                    for i in range(2, 6):
                        self.init_slide(i)
                    messagebox.showinfo("Info", 'Loaded Options from: ' + out)

    def initVars(self):
        self.shortpath = ''
        self.user = StringVar()
        self.user.set('Username')
        self.para = ['' for x in range(0, self.NoParams)]
        self.count = 1  # slide counter
        self.colours_palette = ["#FFFF00", "#09FF09", "#FF00FF", '#6E44E3', '#C9E87B', '#69E0C7', '#D19B1D', '#000000',
                                '#FFFFFF']
        self.catnames = ['Halichoerus Grypus', 'Phoca vitulina', 'Unknown']  # def species names
        self.modnames = ["adult", "juvenile", "swimming", "dead"]  # def modifier names
        self.result = True  # def result of wizard
        self.newobj = 1  # new object counter
        self.wintitles = [None, 'Setup Wizard', 'Username', 'Image acquisition', 'Session Options', 'Session Summary']
        self.result = False
        self.files_good = False
        self.dirList = []
        self.basename = ''
        self.fparameter = {'Directory: ': "", 'File type: ': "", 'File Count: ': 0, 'First File: ': "",
                           'Last File: ': ""}
        self.tagsize = 1
        self.slidenames = [None, 'Welcome to iTAG', 'Username & Extra Columns', 'Retrieve image directory',
                           'Definition of tags', 'Session Summary']

    def save_opt(self, type=None):
        self.updateValues()
        if type == None:
            out = os.path.normpath(os.path.join(self.GLOBALS['RESPATH'], 'default_setup.TiO'))
            messagebox.showinfo("Info", 'This session setup has been set as default setup')
        else:
            out = asksaveasfilename(parent=self.parent, title='save option file as: ', initialdir=self.odir,
                                    defaultextension="TiO",
                                    filetypes=[('Image Tag options', '.TiO'), ('all files', '.*')])
            messagebox.showinfo('Info', 'This specific session setup has been saved at: ' + out)
        try:
            with open(out, 'wb') as f:
                pickle.dump(self.out, f)
        except:
            messagebox.showerror('Error', 'Could not save Options at: ' + out)

    def colCHOOSE(self, index):
        from tkinter.colorchooser import askcolor
        out = askcolor(parent=self, initialcolor=self.colours_palette[index])  # title??
        print(out[1])
        if out != (None, None):
            test = True
            for i in self.colours_palette:
                test = test and globalFunctions.same_cols(out[1], i)
            if not test:
                messagebox.showwarning('Warning', 'Colours may be very similar and thus difficult to distinguish')
            self.colours_palette[index] = out[1]
            self.bCol[index].configure(bg=self.colours_palette[index])
