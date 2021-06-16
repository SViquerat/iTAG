# -*- coding: UTF-8 -*-
# this is wip to bring up to python 3.5
import os, glob, sqlite3
import pickle
import datetime
import gc
import getopt
from tkinter import *
from PIL import Image, ImageOps, ImageFilter, ImageDraw, ImageTk, ImageFont
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename
import csv
from tkinter import messagebox, ttk, simpledialog
from platform import architecture
from collections import namedtuple


def image_FX(img, FX=0):
    if FX == 0:
        return img
    elif FX == 1:
        return ImageOps.autocontrast(img)
    elif FX == 2:
        return ImageOps.invert(img)
    elif FX == 3:
        return ImageOps.equalize(img)  # hist equalized version of 200x200 tmp...
    elif FX == 4:
        return ImageOps.invert(img)  # inverted version of 200x200 tmp...
    elif FX == 5:
        return ImageOps.solarize(img, 128)  # solarized version of 200x200 tmp...
    elif FX == 6:
        return ImageOps.posterize(img, 2)  # solarized version of 200x200 tmp...
    elif FX == 7:  # unsharp mask
        return img.filter(ImageFilter.UnsharpMask)
    elif FX == 8:  # smart sharpen
        img = ImageOps.autocontrast(img)  # autocontrast version of 200x200 tmp...
        tmp1 = img.filter(ImageFilter.DETAIL)
        tmp2 = img.filter(ImageFilter.CONTOUR)
        tmp12 = Image.blend(tmp1, tmp2, .5)
        tmp3 = ImageOps.equalize(tmp12)
        tmp4 = img.filter(ImageFilter.UnsharpMask)
        tmp4 = tmp4.filter(ImageFilter.BLUR)
        return Image.blend(tmp3, tmp4, .7)

def imgFilter(img, FX,TRANSLATION, Mode='normal' ):
    if FX == "k":  # kontrast...
        tmp = ImageOps.autocontrast(img)  # autocontrast version of 200x200 tmp...
        Mode = TRANSLATION['MODE_AUTO']
    if FX == "h":
        tmp = ImageOps.equalize(img)  # hist equalized version of 200x200 tmp...
        Mode = TRANSLATION['MODE_EQH']
    if FX == "j":
        tmp = ImageOps.invert(img)  # inverted version of 200x200 tmp...
        Mode = TRANSLATION['MODE_INV']
    if FX == "g":
        tmp = ImageOps.solarize(img, 128)  # solarized version of 200x200 tmp...
        Mode = TRANSLATION['MODE_SOL']
    if FX == "l":
        tmp = ImageOps.posterize(img, 2)  # solarized version of 200x200 tmp...
        Mode = TRANSLATION['MODE_POS']
    if FX == 'u':  # unsharp mask
        from PIL import ImageFilter
        tmp = tmp.filter(ImageFilter.UnsharpMask)
        Mode = TRANSLATION['MODE_UNSHARP']
    if FX == 's':  # smart sharpen
        from PIL import ImageFilter
        tmp = ImageOps.autocontrast(img)  # autocontrast version of 200x200 tmp...
        tmp1 = tmp.filter(ImageFilter.DETAIL)
        tmp2 = tmp.filter(ImageFilter.CONTOUR)
        tmp12 = Image.blend(tmp1, tmp2, .5)
        tmp3 = ImageOps.equalize(tmp12)
        tmp4 = tmp.filter(ImageFilter.UnsharpMask)
        tmp4 = tmp4.filter(ImageFilter.BLUR)
        tmp = Image.blend(tmp3, tmp4, .7)
        Mode = TRANSLATION['MODE_SMARTSHARP']
    return {img, Mode}
