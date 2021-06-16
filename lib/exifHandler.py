import os
from PIL import Image
from tkinter import messagebox

class exifHandler():
    def __init__(self,GLOBALS,TRANSLATION):
        self.GLOBALS = GLOBALS
        self.TRANSLATION = TRANSLATION
        self.data={}

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
        D['FocalLength'] = ''
        D['Model'] = ''
        D['Make'] = ''
        D['Valid_Exif'] = False
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo is not None:
                D['GPSInfo'] = exifinfo.get(34853)  # gpsinfo
                D['ISOSpeedRatings'] = exifinfo.get(34855)  # gpsinfo
                D['ExifVersion'] = exifinfo.get(36864)  # gpsinfo
                D['DateTime'] = str(exifinfo.get(306))  # gpsinfo
                D['DateTimeOriginal'] = str(exifinfo.get(36867))  # gpsinfo
                D['DateTimeDigitized'] = str(exifinfo.get(36868))  # gpsinfo
                D['FocalLength'] = exifinfo.get(37386)  # gpsinfo
                D['Model'] = exifinfo.get(272)  # gpsinfo
                D['Make'] = exifinfo.get(271)  # gpsinfo
                D['Valid_Exif'] = True
                DateTime = D['DateTimeOriginal']
        ok = False
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
            ok = True
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

    def files_browse_exif(self, dirList):
        i = 0
        for f in dirList:
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
                print(i)
                # print (self.cookie['dirList'])
                self.cookie['dirList'].pop(i - 1)
                next
            D = self.get_exif(img)
            x, y = img.size
            mode = img.mode
            cscale = 1
            if max(x, y) > self.GLOBALS['MAXSIZE']:
                cscale = float(self.GLOBALS['MAXSIZE']) / float(max(x, y))
            tag = dict(ID=i, basename=basename, filename=filename, xsize=x, ysize=y, image_mode=mode, file_scale=cscale,
                       zoom_scale=1, Valid_GPS=D['Valid_GPS'], ISOSpeedRatings=D['ISOSpeedRatings'],
                       ExifVersion=D['ExifVersion'], coord_ref=D['coord_ref'], lat=D['lat'], lon=D['lon'],
                       altitude=D['altitude'], gps_date=D['gpsTime'], DateTime=D['DateTime'],
                       DateTimeOriginal=D['DateTimeOriginal'], DateTimeDigitized=D['DateTimeDigitized'],
                       FocalLength=D['FocalLength'], Model=D['Model'], Make=D['Make'], Valid_Exif=D['Valid_Exif'],
                       file_tagsize = cookie['tagsize'], skip_file=0, global_FX=0)
            self.sqlite_add_file_entry(tag, conn=self.sqlite_conn)
