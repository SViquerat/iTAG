from cx_Freeze import setup, Executable
from time import localtime, strftime
from os import getcwd

# Dependencies are automatically detected, but it might need
# fine tuning.
version_string = '0.7.0.5'

basedir=getcwd()+"\\RES\\"
resdir=getcwd()+"\\RES\\"
includefiles=[]

includefiles.append((basedir+'itag_splash.TkT',"RES\\itag_splash.TkT"))
for i in range(1,7): #wizard image counter
	includefiles.append((basedir+'wiz' + str(i)+'.png',"RES\\wiz"+str(i)+".png"))
[includefiles.append(i) for i in [(getcwd()+'\\Manual\\iTag User Manual.pdf',"Manual\\iTag User Manual.pdf"),(basedir+'helpfile_EN.TkT',"RES\\helpfile_EN.TkT"),
(basedir+'helpfile_DE.TkT',"RES\\helpfile_DE.TkT"),(basedir + 'default_setup.TiO','RES\\default_setup.TiO'),(basedir + 'lang_EN.TlT',"RES\\lang_EN.TlT"),
(basedir + 'lang_DE.TlT',"RES\\lang_DE.TlT"),(basedir + 'lang_FR.TlT',"RES\\lang_FR.TlT"),(basedir + 'processing_EN.TkT',"RES\\processing_EN.TkT"),(basedir + 'processing_DE.TkT',"RES\\processing_DE.TkT"),(basedir + 'dumping.TkT',"RES\\dumping.TkT"),(basedir + 'globalFunctions.py',"RES\\globalFunctions.py"),
(basedir + 'Icons\\info.png',"RES\\Icons\\info.png"),(basedir + 'Icons\\warning.png',"RES\\Icons\\warning.png"),(basedir + 'Icons\\logo.ico',"RES\\Icons\\logo.ico"),
(basedir+'helpfile_EN.TkT',"readme.txt"),(basedir + 'CLASSES.py',"RES\\CLASSES.py"),(basedir + 'SUPERPANEL.py',"RES\\SUPERPANEL.py"),(basedir + 'wizardDialog.py',"RES\\wizardDialog.py")]]

excludes = []
includes = []
packages = []
Target1 = Executable(
    script = getcwd() + '\\iTag.py',
    base = 'Win32GUI',
    targetName='iTAG.exe',
    compress = True,
    copyDependentFiles = True,
    icon = basedir + 'Icons\\logo.ico',
	shortcutName = "iTAG 0.7",
	shortcutDir = "DesktopFolder"
    )

setup(
	name='iTAG',
	author= 'Sacha Viquerat',
	author_email='sacha.viquerat@tiho-hannover.de',
	maintainer ='Sacha Viquerat',
	maintainer_email='itag.biology@yahoo.com',
	license='LGPL',
	version = version_string,
	description = 'Counting Objects in Images:\nAssessing Numbers and Categories ',
	options = {"build_exe": {"packages": packages,
	"excludes": excludes,
	"includes": includes,
	"silent" : True,
	"include_msvcr":True,
	"optimize":1,
	"include_files" : includefiles,
	"compressed" : True}}
	,executables = [Target1]
)
