class TopPanelW(Toplevel): #panel is now a seperate window

		def __init__(self,parent,spec,alt,catc,img,fname,ptitle):
			self.catc=catc
			Toplevel.__init__(self,parent)
			self.parent=parent
			self.title(ptitle)
			self.iconbitmap(ICONPATH)
			self.transient(self.parent)
			self.attributes('-topmost',True)
			self.visible=False
			self.protocol("WM_DELETE_WINDOW",self.toggle)
			self.resizable(0,0)
			self.panelFrame=Frame(self,relief="raised")
			self.infoFrame=Frame(self.panelFrame,relief="raised")
			self.countl=[] #
			self.sum=[] #
			self.categories=len(spec) # number of categories
			self.alts=len(alt) # number of modifiers
			pos=0
			# catc is a summary table
			for i in range(0,len(spec)):
				self.cat_label=Label(self.infoFrame,text=spec[i] + ": ",anchor='nw',relief='groove',font = labelfont)
				self.cat_label.grid(row=i+1,column=0,sticky=W+E)
				for j in range(0,len(alt)):
					self.countl.append(Label(self.infoFrame,text=str(catc[i][j]),relief='groove'))
					self.countl[pos].grid(row=i+1,column=j+1,sticky=NW+SE)
					pos+=1
			for i in range (0,len(alt)): #maybe superfluous
				# ind count
				label=Label(self.infoFrame,text=alt[i],relief='groove',font = labelfont)
				label.grid(row=0,column=i+1,sticky=W+E)
			for i in range (0,len(spec)): #maybe superfluous
				# species sums
				self.sum.append(Label(self.infoFrame,text=str(sum(catc[i])),anchor='nw',relief='groove',font = labelfont))
				self.sum[i].grid(row=i+1,column=len(alt)+1,sticky=W+E)
			size = 300,300
			img=img.resize(size)
			#img=img.thumbnail(size)
			label=Label(self.infoFrame,text="Sum",relief='groove',font = labelfont)
			label.grid(row=0,column=j+2,sticky=W+E)
			self.infoFrame.grid(row=1,column=0)
			self.canvFrame=Frame(self.panelFrame,relief="sunken",bd=1)
			self.popup = Canvas(self.canvFrame)
			self.popup.create_image(0,0,image=ImageTk.PhotoImage(img),anchor="ne")

			self.popup.configure(width=img.size[0],height=img.size[1])
			self.filename_label=Label(self.panelFrame,text=fname)
			self.filename_label.grid(row=11,column=1)
			self.popup.pack()
			self.canvFrame.grid(row=0,column=1,rowspan=10)
			self.panelFrame.grid()
			self.bind("<F9>",self.toggle) #grab and...

		def redraw(self,x,y,cextent,pImage,scale,col,fname):
			self.popup.create_image(0,0,image=pImage,anchor="nw",tags=("bg",0)) #in the panel
			self.popup.configure(width=x,height=y)
			self.filename_label.configure(text=fname)
			rect = [int(float(i)/scale) for i in cextent] #rectangle coordinates
			self.popup.create_rectangle(rect,outline=col,tags=("view",0)) #in the panel

		def moveview(self,x,y,cextent,scale,col):
			self.popup.delete('view') #destroy rectangle
			rect = [int(float(i)/scale) for i in cextent] #rectangle coordinates
			self.popup.create_rectangle(rect,outline=col,tags=("view",0)) #in the panel

		def update(self,index=None,alt_i=None):
			self.countl[index*4+alt_i].configure(text=self.catc[index][alt_i])
			self.sum[index].configure(text=str(sum(self.catc[index])))

		def hide(self):
			self.withdraw()

		def show(self):
			self.deiconify()

		def toggle(self,Event=None):
			self.visible = not self.visible
			if self.visible:
				self.hide()
			else:
				self.show()

		def _NULL():
			pass

class InfoPanelW(Toplevel): #panel is now a seperate window

		def __init__(self,parent,spec,alt,catc):#,ptitle):
			self.catc=catc
			Toplevel.__init__(self,parent)
			self.parent=parent
			#self.title(ptitle)
			self.iconbitmap(ICONPATH)
			self.transient(self.parent)
			self.attributes('-topmost',True)
			self.visible=False
			self.protocol("WM_DELETE_WINDOW",self.toggle)
			self.resizable(0,0)
			self.panelFrame=Frame(self,relief="raised")
			self.infoFrame=Frame(self.panelFrame,relief="raised")
			self.countl=[] #
			self.sum=[] #
			self.categories=len(spec) # number of categories
			self.alts=len(alt) # number of modifiers
			pos=0
			# catc is a summary table
			for i in range(0,len(spec)):
				self.cat_label=Label(self.infoFrame,text=spec[i] + ": ",anchor='nw',relief='groove',font = labelfont)
				self.cat_label.grid(row=i+1,column=0,sticky=W+E)
				for j in range(0,len(alt)):
					self.countl.append(Label(self.infoFrame,text=str(catc[i][j]),relief='groove'))
					self.countl[pos].grid(row=i+1,column=j+1,sticky=NW+SE)
					pos+=1
			for i in range (0,len(alt)): #maybe superfluous
				# ind count
				label=Label(self.infoFrame,text=alt[i],relief='groove',font = labelfont)
				label.grid(row=0,column=i+1,sticky=W+E)
			for i in range (0,len(spec)): #maybe superfluous
				# species sums
				self.sum.append(Label(self.infoFrame,text=str(sum(catc[i])),anchor='nw',relief='groove',font = labelfont))
				self.sum[i].grid(row=i+1,column=len(alt)+1,sticky=W+E)
			label=Label(self.infoFrame,text="Sum",relief='groove',font = labelfont)
			label.grid(row=0,column=j+2,sticky=W+E)
			self.infoFrame.grid(row=1,column=0)
			self.panelFrame.grid()
			self.bind("<F9>",self.toggle) #grab and...

		def update(self,index=None,alt_i=None):
			self.countl[index*4+alt_i].configure(text=self.catc[index][alt_i])
			self.sum[index].configure(text=str(sum(self.catc[index])))

		def hide(self):
			self.withdraw()

		def show(self):
			self.deiconify()

		def toggle(self,Event=None):
			self.visible = not self.visible
			if self.visible:
				self.hide()
			else:
				self.show()

		def _NULL():
			pass

class NaviPanelW(Toplevel): #navigation panel

		def __init__(self,parent,img,fname,ptitle):
			Toplevel.__init__(self,parent)
			self.parent=parent
			self.title(ptitle)
			self.iconbitmap(ICONPATH)
			self.visible=False
			self.protocol("WM_DELETE_WINDOW",self.toggle)
			self.transient(self.parent)
			self.attributes('-topmost',True)
			self.resizable(0,0)
			self.panelFrame=Frame(self,relief="raised")
			size = 300,300
			img=img.resize(size)
			self.cFrame=Frame(self.panelFrame,bd=3,background='red')
			self.canvas = Canvas(self.cFrame)
			self.canvas.create_image(0,0,image=ImageTk.PhotoImage(img),anchor="ne")
			self.canvas.pack()
			self.cFrame.grid(row=0,column=0)
			self.filename_label=Label(self.panelFrame,text=fname)
			self.filename_label.grid(row=1,column=0)
			self.panelFrame.pack()
			self.bind("<F10>",self.toggle) #grab and...

		def redraw(self,x,y,cextent,pImage,scale,col,fname):
			self.canvas.create_image(0,0,image=pImage,anchor="nw",tags=("bg",0)) #in the panel
			self.canvas.configure(width=x,height=y)
			self.filename_label.configure(text=fname)
			rect = [int(float(i)/scale) for i in cextent] #rectangle coordinates
			self.canvas.create_rectangle(rect,outline=col,tags=("view",0)) #in the panel

		def moveview(self,x,y,cextent,scale,col):
			self.canvas.delete('view') #destroy rectangle
			rect = [int(float(i)/scale) for i in cextent] #rectangle coordinates
			self.canvas.create_rectangle(rect,outline=col,tags=("view",0)) #in the panel

		def hide(self):
			self.withdraw()

		def show(self):
			self.deiconify()

		def toggle(self,Event=None):
			self.visible = not self.visible
			if self.visible:
				self.hide()
			else:
				self.show()

		def _NULL():
			pass
