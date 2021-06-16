import os, glob,sqlite3
import re #regular expression; may need them in the future
import pickle
from Tkinter import *
from PIL import Image, ImageOps, ImageDraw, ImageTk
from tkFileDialog import askdirectory,asksaveasfilename,askopenfilename
import tkSimpleDialog, csv, tkMessageBox
from string import maketrans
from random import randint
from itertools import chain

class OutputOptions(Frame):
	
	def __init__(self,parent):
		self.parent=parent
		self.species=["adult","juvenile","swimming","dead"] # attributes of category
		self.alttext = ['Halichoerus Grypus','Phoca vitulina','Unknown'] ##later to be defined by User
		self.cols=[]
		self.cols = [[0]*len(self.alttext) for x in xrange(len(self.species))]
		Frame.__init__(self, parent)
		self.initUI()
		
	def initUI(self):
		#self.parent.title("checktest")
		self.mainWindow = Frame(self.parent)
		self.headFrame=Frame(self.mainWindow, bd=2, relief=SUNKEN)
		l=Label(self.headFrame, text='Columns to process',relief=FLAT)
		l.pack(fill=X,side=LEFT)
		self.headFrame.pack(side=TOP,fill=X,expand=0)
		
		### columns selector frame
		self.colFrame = Frame(self.mainWindow, bd=2, relief=SUNKEN)		
		for i in range(0,len(self.species)):
			l=Label(self.colFrame, text=self.species[i],anchor="center",relief=SUNKEN)
			l.grid(row=0,column=i+1,sticky=W+E)
			for j in range(0,len(self.alttext)):
				check=Checkbutton(self.colFrame,bd=1,command=lambda i=i,j=j: self.fire(i,j),relief=SUNKEN)
				check.invoke() # makes them selected, fills self.cols
				check.grid(row=j+1,column=i+1,sticky=W+E)
		for j in range(0,len(self.alttext)):
			l=Label(self.colFrame, text=self.alttext[j],anchor="center",relief=SUNKEN)
			l.grid(row=j+1,column=0,sticky=W+E)
		self.colFrame.pack(side=TOP,fill=BOTH)
		
		### any other output options??
		
		### confirm button frame
		self.bFrame = Frame(self.mainWindow, bd=2, relief=SUNKEN)
		self.bContinue=Button(self.bFrame,text='Continue',command=self.Confirm,anchor=E)		
		self.bContinue.pack(side=RIGHT)	
		self.bFrame.pack(side=BOTTOM,fill=X)
		self.mainWindow.pack(fill=BOTH,expand=1)
		
		### set min / max window size
		self.update()
		self.parent.minsize(self.parent.winfo_width(),self.parent.winfo_height())
		self.parent.maxsize(self.parent.winfo_width(),self.parent.winfo_height())


	def fire(self,i,j):
		if self.cols[i][j]==0:
			new=self.alttext[j]+' '+self.species[i]
			self.cols[i][j]=new
		else:
			self.cols[i][j]=0
	
	def Confirm(self):
		out = list(chain.from_iterable(self.cols)) #flatten list
		out = [x for x in out if x != 0] #remove all elements that are not 0's
		self.columns2process = out
		self.parent.destroy()
		
def main():
	root=Tk()
	app = OutputOptions(root)
	app.mainloop()
	print app.columns2process # list of columns to process in the output files

if __name__ == "__main__":
	main()
				

