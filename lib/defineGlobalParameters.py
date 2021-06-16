# -*- coding: UTF-8 -*-
import getopt
import os
import sys
from platform import architecture
from lib import globalFunctions


def setGLOBALS(MAJOR = 0.8, MINOR = 0, NAME = 'Unseen University'):
    ARCH = "32bit"
    if "64" in architecture()[0]: ARCH = "64bit"
    OS = os.name
    GLOBALS = {'MAJOR': MAJOR, 'SAVEVERSION': 8, 'MINOR': MINOR, 'MAJORNAME': NAME, 'OS': OS, 'ARCH': ARCH,
               'LANGUAGE': 'EN'}
    GLOBALS['VERSIONSTRING'] = str(GLOBALS['MAJOR']) + '.' + str(GLOBALS['MINOR'])
    GLOBALS['MAJORNAME'] = NAME
    GLOBALS['LONGVERSION'] = "iTAG Version: " + GLOBALS['VERSIONSTRING'] + " Codename: " + GLOBALS['MAJORNAME']
    GLOBALS['PROGDIR'] = os.getcwd()  # program directory]
    GLOBALS['SEP'] = os.path.sep
    GLOBALS['RESPATH'] = os.path.join(GLOBALS['PROGDIR'], 'RES')
    GLOBALS['ICONPATH'] = os.path.join(GLOBALS['RESPATH'], 'Icons', 'logo.ico')

    GLOBALS['THEMEBG'] = globalFunctions.black

    ##fonts get rid
    GLOBALS['LABELFONT'] = "Helvetica 10 italic"  # adapt for different OS
    GLOBALS['HELPFONT'] = "Arial 10 italic"  # adapt for different OS
    GLOBALS['BUTTONFONT'] = "Verdana 8"  # adapt for different OS
    GLOBALS['SMALLBUTTONFONT'] = "Verdana 6"  # adapt for different OS
    GLOBALS['SMALLFONT'] = "Verdana 8"

    # cursors
    GLOBALS['DEF_CURSOR'] = 'arrow'
    GLOBALS['TAG_CURSOR'] = 'tcross'
    GLOBALS['ERASE_CURSOR'] = 'dotbox'

    # load language file
    fileName = os.path.join(GLOBALS['RESPATH'], 'lang_EN.TlT')
    dict = {}
    with open(fileName) as file:
        for line in file:
            setting = line.split(' = ')  # This is assuming the text file is space-delimited.
            if (len(setting) < 2 or setting[0][0].strip() == '#' or setting[0][0].strip() == '\n'): continue
            key, value = setting[0], setting[1]
            dict[key] = eval(value.strip())
    _L = ''
    MAXSIZE = 10000

    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:", ['maxsize='])
    except getopt.GetoptError:
        _L = 'iTag --maxsize 7000\nwhere maxsize is maximum size of one length of image before reducing size'

    for opt, arg in opts:
        if opt in ['-m', '--maxsize']:
            try:
                MAXSIZE = int(arg)
            except:
                pass

    TRANSLATION = dict
    GLOBALS['MAXSIZE'] = MAXSIZE
    GLOBALS['HELPFILE'] = os.path.join(GLOBALS['RESPATH'], "helpfile_" + GLOBALS['LANGUAGE'] + ".TkT")
    GLOBALS['ABOUTTEXT'] = "\n\nIntellectual property of:\n\n\tSacha Viquerat & Abbo van Neer\n\tCarl-Petersen Strasse 118a\n\t20535 Hamburg\n\thttps://sourceforge.net/projects/itagbiology\n"
    GLOBALS['TITLE'] = "iTAG " + str(GLOBALS['VERSIONSTRING'] + " " + GLOBALS['ARCH'])
    return GLOBALS,TRANSLATION