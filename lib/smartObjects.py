from tkinter import Button
from tkinter import Menu
from tkinter.colorchooser import askcolor
from tkinter import simpledialog

from lib import globalFunctions


class catButton(Button):
    def __init__(self, index=0, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['state'] = 'disabled'
        self['fg'] = globalFunctions.col_invert(self['bg'])
        self['disabledforeground'] = self['fg']
        self.catname = self['text']
        self.index = index
        self['text'] = '{0}: {1}'.format(str(self.index+1),self.catname)
        self.locked = True
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Unlock",command = lambda: self.event_generate('<<lockToggle>>'))
        self.popup_menu.add_command(label="Change Colour",state='disabled',command = lambda: self.event_generate('<<ChangeColour>>'))
        self.popup_menu.add_command(label="Change Category Name",state='disabled', command = lambda: self.event_generate('<<ChangeLabel>>'))
        self.setBindings()

    def setBindings(self):
        self.bind('<Button-1>',lambda e: self.event_generate('<<Event_CatSelected>>'))
        self.bind("<Button-3>", self.popup)
        self.bind('<<lockToggle>>',self.toggleLock)
        self.bind('<<ChangeColour>>',self.setColour)
        self.bind('<<ChangeLabel>>',self.setLabel)

    def getAttributes(self,key = None):
        out = {'index' : self.index,'locked' : self.locked, 'fg' : self['fg'], 'bg' : self['bg'], 'label' : self['text'],'state' : self['state']}
        if key is not None:
            out = out[key]
        return out

    def popup(self, event = None):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def toggleLock(self, event = None):
        self.locked = not self.locked
        if self.locked:
            newState='disabled'
            self.popup_menu.entryconfig(0, label = 'Lock')
        else:
            newState = 'normal'
            self.popup_menu.entryconfig(0, label='Unlock')

        last = self.popup_menu.index("end")
        for i in range(1,last+1):
            self.popup_menu.entryconfig(i, state=newState)
        self['state'] = newState
        self.event_generate('<<Event_CatLockToggle>>')

    def toggleActive(self,Event=None):
        pass

    def setColour(self, event=None):
        out = askcolor(parent=self, initialcolor=self['bg'])  # title??
        self['bg'] = out[1]
        self['fg'] = globalFunctions.col_invert(out[1])
        self['disabledforeground'] = self['fg']
        self.event_generate("<<Event_CatColourChange>>")

    def setLabel(self,event = None):
        newLabel = simpledialog.askstring('New Label for category {0}'.format(str(self.index)),
                                          "Please enter a new category label")
        if newLabel is not None:
            self.catname = newLabel
            self['text'] = '{0}: {1}'.format(str(self.index + 1), self.catname)
            self.event_generate("<<Event_CatNameChange>>")
