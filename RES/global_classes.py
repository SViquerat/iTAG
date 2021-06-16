class OKCANCEL(Toplevel): #ok / cancel dialog
	def __init__(self,parent,mtext,ICON='info',dim=62,BTN1=BTN_OK,BTN2=BTN_CANCEL):
		Toplevel.__init__(self,parent)
		self.parent=parent
		self.grab_set()
		self.initial_focus = self
		self.initial_focus.focus_set()
		self.protocol("WM_DELETE_WINDOW",self._CANCEL) #we need to include a check again...
		self.geometry("+"+str(self.winfo_screenwidth()/4)+"+"+str(self.winfo_screenheight()/4))
		self.resizable(0,0)
		self.iconbitmap(ICONPATH)
		self.transient(self.parent)

		fname=os.path.join(progdir,'RES','Icons',ICON + '.png')
		img=Image.open(fname).resize((dim,dim),Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		BG=lightgrey
		BG2=white

		mainWindow=Frame(self,bg=BG)
		tFrame=Frame(mainWindow,bg=BG2)
		tCanvas=Canvas(tFrame,width=dim,height=dim,highlightthickness=0,bg=BG2)
		tCanvas.create_image(0,0,image=img,anchor="nw")
		tLabel=Label(tFrame,text=mtext,height=3,bg=BG2,font=labelfont,bd=10)
		tCanvas.pack(side='left')
		tLabel.pack(side='right')
		tFrame.grid(row=0,column=0)

		bFrame=Frame(mainWindow,bg=BG,bd=5)
		bOK=Button(bFrame,bd=1,text=BTN1,command=self._OK,bg=BG,font=buttonfont)
		bCANCEL=Button(bFrame,bd=1,text=BTN2,command=self._CANCEL,bg=BG,font=buttonfont)
		bOK.pack(side='left')
		bCANCEL.pack(side='right')
		bFrame.grid(row=1,column=0,sticky=E)
		mainWindow.pack()
		self.wait_window(self)

	def _OK(self,Event=None):
		self.result=True
		self.destroy()

	def _CANCEL(self,Event=None):
		self.result=False
		self.destroy()

class WARNING(Toplevel): #ok only dialog

	def __init__(self,parent,wtext,wtitle=WARNING_TITLE,ICON='warning',dim=62):
		Toplevel.__init__(self,parent)
		self.parent=parent
		self.grab_set()
		self.initial_focus = self
		self.initial_focus.focus_set()
		self.protocol("WM_DELETE_WINDOW",_NULL) #we need to include a check again...
		self.geometry("+"+str(self.winfo_screenwidth()/4)+"+"+str(self.winfo_screenheight()/4))
		self.resizable(0,0)
		self.title(wtitle)
		self.iconbitmap(ICONPATH)
		self.transient(self.parent)


		fname=os.path.join(progdir,'RES','Icons',ICON + '.png')
		img = Image.open(fname).resize((dim,dim),Image.ANTIALIAS)
		img = ImageTk.PhotoImage(img)
		BG=lightgrey #lower color
		BG2=white #messagebox color

		mainWindow=Frame(self,bg=BG)
		tFrame=Frame(mainWindow,bg=BG2)
		tCanvas=Canvas(tFrame,width=dim,bg=BG2,height=dim,highlightthickness=0)
		tCanvas.create_image(0,0,image=img,anchor="nw")
		tLabel=Label(tFrame,text=wtext,bg=BG2,height=3,font=labelfont,bd=10)
		tCanvas.pack(side='left')
		tLabel.pack(side='right')
		tFrame.grid(row=0,column=0)

		bFrame=Frame(mainWindow,bg=BG,bd=5)
		bOK=Button(bFrame,bd=1,text=BTN_OK,command=self._DONE,bg=BG,font=buttonfont)
		bOK.pack(side='left')
		bFrame.grid(row=1,column=0,sticky=E)
		mainWindow.pack()
		self.parent.wait_window(self)

	def _DONE(self,Event=None):
		self.destroy()
		
def _NULL():
	pass
