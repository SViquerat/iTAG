# -*- coding: UTF-8 -*-
# this is wip to bring up to python 3.5
# csv export and buttons are wrong, amongst other things
from PIL import ImageDraw

# user files
from lib.dialogWindows import *


class MultiPanel(Toplevel):  # maybe pass opened image, its faster?

    def __init__(self, parent, GLOBALS, cookie, gpsdict, ptitle, image=None):
        Toplevel.__init__(self, parent)
        self.cookie = cookie
        self.GLOBALS = GLOBALS
        self.gpsdict = gpsdict
        self.parent = parent
        self.title(ptitle)
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", self._CLOSE)
        self.resizable(0, 0)
        self.gpsvisible = False
        self.infovisible = False
        filename = os.path.join(self.cookie['basename'], self.cookie['current_file'])

        self.PANEL = Frame(self)
        self.PANEL.pack(fill=BOTH, expand=1)

        self.nFrame = Frame(self.PANEL)
        self.Navi = NaviPanel(self.nFrame, imgpth=filename, cookie=self.cookie, image=image)
        self.Navi.pack()
        self.nFrame.grid(row=0, column=0)

        self.p1 = Button(self.PANEL, text='File Info Panel', relief=RAISED, anchor='e',
                         command=lambda i=1: self.toggle_vis(index=i))
        self.p1.grid(row=1, column=0, sticky=E + W)
        self.p2 = Button(self.PANEL, text='Tag summary panel', relief=RAISED, anchor='e',
                         command=lambda i=2: self.toggle_vis(index=i))
        self.p2.grid(row=3, column=0, sticky=E + W)

        self.bottoms = [None] * 3

        self.infoFrame = Frame(self.PANEL)
        self.summary = InfoPanel(self.infoFrame, self.GLOBALS, self.cookie)
        self.summary.pack(side=RIGHT, fill=X)
        self.bottoms[2] = self.infoFrame

        self.exifFrame = Frame(self.PANEL)
        self.exifInfo = exifPanel(self.exifFrame, gpsdict)
        self.exifInfo.pack(side=LEFT, fill=X)
        self.bottoms[1] = self.exifFrame

        self.nFrame.grid(row=0, column=0)

    def _CLOSE(self):
        self.parent.viewmenu.invoke(
            0)  # why is this working? I don't know and I don't care. probably this is not safe, but who cares?

    def _NULL(self):
        pass

    def toggle_vis(self, index):
        if index == 1:
            self.gpsvisible = not self.gpsvisible
            if not self.gpsvisible:
                self.bottoms[index].grid_forget()
            else:
                self.bottoms[index].grid(row=2, column=0, sticky=W + E)
        elif index == 2:
            self.infovisible = not self.infovisible
            if not self.infovisible:
                self.bottoms[index].grid_forget()
            else:
                self.bottoms[index].grid(row=4, column=0, sticky=W + E)

    def update(self, cookie, i=None, j=None, index=0, gpsdict={}, image=None):
        self.cookie = cookie
        self.gpsdict = gpsdict
        # self.lName=Label(self,text=cookie['shortpath']+os.sep+cookie['current_file'])
        if index == 0:  # redraw
            self.Navi.redraw(self.cookie, image)
            self.exifInfo.update(self.gpsdict)
        elif index == 1:  # tag add /remove
            self.summary.update(self.cookie, i=i, j=j)
        else:
            self.summary.update(self.cookie, i=i, j=j)
            self.Navi.redraw(self.cookie, image)
            self.exifInfo.update(self.gpsdict)


class NaviPanel(Frame):  # navigation panel
    def __init__(self, parent, imgpth, cookie, image=None):
        Frame.__init__(self, parent)
        self.lName = Label(self, text=os.path.join(cookie['shortpath'], cookie['current_file']))
        self.lName.pack(side=TOP, anchor='w')
        self.parent = parent
        self.cFrame = Frame(self, width=cookie['panel_canvas_size'], height=cookie['panel_canvas_size'], bg='black')

        if image == None:
            self.openImage(imgpth, cookie)
        else:
            self.image_panel = image
            self.image_size_panel = cookie['panel_image_size']
            self.scale = cookie['panel_image_scale']
            self.image_size_original = cookie['current_image_original_size']

        self.canvas_bg = Canvas(self.cFrame, bd=3)
        self.canvas_bg.configure(width=cookie['panel_canvas_size'], height=cookie['panel_canvas_size'])
        self.canvas_bg.pack(anchor=NW, expand=1, fill=BOTH)
        self.canvas_bg.create_rectangle((0, 0, cookie['panel_canvas_size'], cookie['panel_canvas_size']), fill='red',
                                        tags=("panel_bg", 0))  # in the panel

        self.canvas = Canvas(self.canvas_bg, bd=2, bg='black')
        self.canvas.configure(width=self.image_size_panel[0], height=self.image_size_panel[1])
        self.canvas.create_image(0, 0, image=self.image_panel, anchor=NW, tags=("panel_image", 0))
        self.draw_rect(cookie)
        self.canvas.pack(anchor=CENTER, expand=1, fill=BOTH)
        self.cFrame.pack(fill=BOTH, expand=1)
        self.lSize = Label(self, text='Image size: ' + str(self.image_size_original[0]) + ' x ' + str(
            self.image_size_original[1]))
        self.lSize.pack(side=RIGHT)

    def openImage(self, imgpth, cookie):
        img = Image.open(os.path.normpath(imgpth))
        if cookie['file_scale'] != 1:
            width, height = img.size
            newsize = int(width * cookie['file_scale']), int(height * cookie['file_scale'])
            img = img.resize(newsize)
        size = cookie['panel_canvas_size']
        self.scale = float(max(img.size)) / size
        width, height = img.size
        self.image_size_original = cookie['current_image_original_size']
        newsize = int(width / self.scale), int(height / self.scale)
        try:
            img = img.resize(newsize)
        except:
            img = Image.new("RGB", newsize, 'black')
            draw = ImageDraw.Draw(img)
            textx = int(newsize[0] / 2)
            texty = int(newsize[1] / 2)
            draw.text((textx, texty),
                      "You seem to have run into memory issues. Please consider either increasing your system Memory or switching to the 64bit Version of iTAG to make more Memory available. You can still use the navigational panel for navigation.",
                      'white')
            print("load failure")
        self.image_size_panel = img.size
        self.image_panel = ImageTk.PhotoImage(img)

    def redraw(self, cookie, image=None):
        col = 'white'
        if cookie['currentSpecIndex'] != None:
            col = cookie['colours'][cookie['currentSpecIndex']]
        imgpth = cookie['basename'] + os.sep + cookie['current_file']

        if image == None:
            self.openImage(imgpth, cookie)
        else:
            self.image_panel = image
            self.image_size_panel = cookie['panel_image_size']
            self.scale = cookie['panel_image_scale']
            self.image_size_original = cookie['current_image_original_size']
        self.canvas.create_image(0, 0, image=self.image_panel, anchor=NW, tags=("panel_image", 0))  # in the panel
        self.canvas.configure(width=self.image_size_panel[0], height=self.image_size_panel[1])
        self.scale = cookie['panel_image_scale']  # update the scale value
        self.draw_rect(cookie)
        self.lName.config(text=cookie['shortpath'] + os.sep + cookie['current_file'])
        self.lSize.configure(
            text='Image size: ' + str(self.image_size_original[0]) + ' x ' + str(self.image_size_original[1]))

    def draw_rect(self, cookie, type=None):
        col = 'white'
        if cookie['currentSpecIndex'] != None:
            col = cookie['colours'][cookie['currentSpecIndex']]
        cextent = cookie['cextent']
        rect = [int(float(i / self.scale)) for i in cextent]  # rectangle coordinates
        self.canvas.create_rectangle(rect, outline=col, tags=("panel_rect", 0))  # in the panel

    def moveview(self, cookie):
        self.canvas.delete('panel_rect')  # destroy rectangle
        self.draw_rect(cookie)

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

    def toggle(self, Event=None):
        self.visible = not self.visible
        if self.visible:
            self.hide()
        else:
            self.show()

    def _NULL(self):
        pass


class InfoPanel(Frame):  # tag counter panel
    def __init__(self, parent, GLOBALS,cookie):
        Frame.__init__(self, parent)
        self.parent = parent
        self.cookie = cookie
        self.GLOBALS=GLOBALS
        self.infoFrame = Frame(self, relief=RIDGE)
        spec = self.cookie['catnames']  # species names
        alt = self.cookie['modnames']  # alt names
        catc = self.cookie['catcounter']  # current count
        self.counts = [[_ for _ in range(len(alt))] for _ in range(len(spec))]  # empty count labels
        self.sum = []  # species sums
        for i in range(0, len(spec)):
            label = Label(self.infoFrame, text=spec[i] + ": ", anchor='nw', relief='groove', font=self.GLOBALS['LABELFONT'])
            label.grid(row=i + 1, column=0, sticky=W + E)
            for j in range(0, len(alt)):
                self.counts[i][j] = Label(self.infoFrame, text=catc[i][j], relief='groove')
                self.counts[i][j].grid(row=i + 1, column=j + 1, sticky=NW + SE)
        for j in range(0, len(alt)):  # maybe superfluous
            label = Label(self.infoFrame, text=alt[j], relief='groove', font=self.GLOBALS['LABELFONT'])
            label.grid(row=0, column=j + 1, sticky=W + E)
        for i in range(0, len(spec)):  # maybe superfluous
            # species sums
            self.sum.append(Label(self.infoFrame, text=str(sum(catc[i])), anchor='nw', relief='groove'))
            self.sum[i].grid(row=i + 1, column=len(alt) + 1, sticky=W + E)
        label = Label(self.infoFrame, text="Sum", relief='groove', font=self.GLOBALS['LABELFONT'])
        label.grid(row=0, column=j + 2, sticky=W + E)
        self.infoFrame.pack()

    def update(self, cookie, i=None, j=None):
        self.cookie = cookie
        spec = self.cookie['catnames']  # species names
        alt = self.cookie['modnames']  # alt names
        catc = self.cookie['catcounter']
        if i == None or j == None:
            for i in range(0, len(spec)):
                self.sum[i].configure(text=str(sum(catc[i])))
                for j in range(0, len(alt)):
                    self.counts[i][j].configure(text=catc[i][j])
        else:
            self.counts[i][j].configure(text=catc[i][j])
            self.sum[i].configure(text=str(sum(catc[i])))

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

    def toggle(self, Event=None):
        self.visible = not self.visible
        if self.visible:
            self.hide()
        else:
            self.show()

    def _NULL(self):
        pass


class exifPanel(Frame):  # exif viewer panel
    def __init__(self, parent, gpsdict):
        Frame.__init__(self, parent)
        relief = RIDGE
        self.parent = parent
        self.gpsdict = gpsdict
        self.exifFrame = Frame(self)
        self.exifFrame.pack(fill=BOTH)
        # gps part
        lat = self.gpsdict.get('lat')
        lon = self.gpsdict.get('lon')
        coord_ref = str(self.gpsdict.get('coord_ref'))
        altitude = str(self.gpsdict.get('altitude'))
        datetime = str(self.gpsdict.get('DateTimeOriginal'))

        # file info part
        MAKE = str(self.gpsdict.get('Make'))
        MODEL = str(self.gpsdict.get('Model'))
        FLENGTH = str(self.gpsdict.get('FocalLength'))
        EXIFV = str(self.gpsdict.get('ExifVersion'))

        gps_col = 'red'
        state = 'disabled'

        if self.gpsdict.get('Valid_GPS') == 'True':
            gps_col = '#2F9E3E'
            state = 'normal'
            lat = round(float(lat), 4)
            lon = round(float(lon), 4)
        file_col = 'red'
        if self.gpsdict.get('Valid_Exif') == 'True':
            file_col = '#2F9E3E'

        # gps info
        pos = Label(self.exifFrame, text='Coordinates: ', relief=relief)
        pos.grid(row=0, column=0, sticky=W + E)
        alt = Label(self.exifFrame, text='Altitude: ', relief=relief)
        alt.grid(row=1, column=0, sticky=W + E)
        coref = Label(self.exifFrame, text='Reference: ', relief=relief)
        coref.grid(row=2, column=0, sticky=W + E)
        time = Label(self.exifFrame, text='Timestamp: ', relief=relief)
        time.grid(row=3, column=0, sticky=W + E)
        self.pos = Button(self.exifFrame, text=str(lat) + ', ' + str(lon), relief=relief, fg=gps_col,
                          command=lambda i=self.gpsdict: self.on_earth(i), state=state)
        self.pos.grid(row=0, column=1, sticky=W + E)
        self.alt = Label(self.exifFrame, text=altitude + ' m', fg=gps_col, relief=relief)
        self.alt.grid(row=1, column=1, sticky=W + E)
        self.coref = Label(self.exifFrame, text=coord_ref, fg=gps_col, relief=relief)
        self.coref.grid(row=2, column=1, sticky=W + E)
        self.time = Label(self.exifFrame, text=datetime, fg=gps_col, relief=relief)
        self.time.grid(row=3, column=1, sticky=W + E)
        # file info
        maker = Label(self.exifFrame, text='Cam maker: ', relief=relief)
        maker.grid(row=0, column=2, sticky=W + E)
        model = Label(self.exifFrame, text='Cam model: ', relief=relief)
        model.grid(row=1, column=2, sticky=W + E)
        flength = Label(self.exifFrame, text='Focal Length: ', relief=relief)
        flength.grid(row=2, column=2, sticky=W + E)
        exifv = Label(self.exifFrame, text='Exif Version: ', relief=relief)
        exifv.grid(row=3, column=2, sticky=W + E)
        self.maker = Label(self.exifFrame, text=MAKE, relief=relief, fg=file_col)
        self.maker.grid(row=0, column=3, sticky=W + E)
        self.model = Label(self.exifFrame, text=MODEL, fg=file_col, relief=relief)
        self.model.grid(row=1, column=3, sticky=W + E)
        self.focal = Label(self.exifFrame, text=FLENGTH, fg=file_col, relief=relief)
        self.focal.grid(row=2, column=3, sticky=W + E)
        self.exifV = Label(self.exifFrame, text=EXIFV, fg=file_col, relief=relief)
        self.exifV.grid(row=3, column=3, sticky=W + E)

    def update(self, gpsdict):
        self.gpsdict = gpsdict
        # gps part
        lat = self.gpsdict.get('lat')
        lon = self.gpsdict.get('lon')
        coord_ref = str(self.gpsdict.get('coord_ref'))
        altitude = str(self.gpsdict.get('altitude'))
        datetime = str(self.gpsdict.get('DateTimeOriginal'))

        # file info part
        MAKE = str(self.gpsdict.get('Make'))
        MODEL = str(self.gpsdict.get('Model'))
        FLENGTH = str(self.gpsdict.get('FocalLength'))
        EXIFV = str(self.gpsdict.get('ExifVersion'))

        gps_col = 'red'
        state = 'disabled'
        if self.gpsdict.get('Valid_GPS') == 'True':
            gps_col = '#2F9E3E'
            state = 'normal'
            lat = round(float(lat), 4)
            lon = round(float(lon), 4)
        file_col = 'red'
        if self.gpsdict.get('Valid_Exif') == 'True':
            file_col = '#2F9E3E'

        self.pos.config(text=str(lat) + ', ' + str(lon), fg=gps_col, state=state,
                        command=lambda i=self.gpsdict: self.on_earth(i))
        self.alt.config(text=altitude + ' m', fg=gps_col)
        self.coref.config(text=coord_ref, fg=gps_col)
        self.time.config(text=datetime, fg=gps_col)

        self.maker.config(text=MAKE, fg=file_col)
        self.model.config(text=MODEL, fg=file_col)
        self.focal.config(text=FLENGTH, fg=file_col)
        self.exifV.config(text=EXIFV, fg=file_col)

    def on_earth(self, gpsdict):
        import webbrowser
        lat = gpsdict['lat']  # float
        lon = gpsdict['lon']  # float
        url = 'https://www.google.com/maps/preview/@' + str(lat) + ',' + str(lon) + ',14z'  # optimize zoom level
        try:
            webbrowser.open(url, new=0, autoraise=True)
        except:
            print(url)

    def _NULL(self):
        pass
