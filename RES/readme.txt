Quick Overview:

Keys:
F1: display this message
Control + N: Start new session
Control + Q: end Session (thus saving results)
Control + S: save Session
Control + L: load Session

1 to 9: Choose Category
Left mouse click (hold and move): move canvas
Right mouse click: Add tag
Modifier Key (Shift, Alt or Control + Right mouse click: Add modified tag (see Options Menu for details)
Control + Shift + Right Click: erases Tags from Image

q / a / arrow key left: switch to previous Image
w / z / arrow key right: switch to next Image
e / arrow key up: increase group counter
d / arrow ky down: decrease group counter

+: increase display size of tags
-: decrease display size of tags
m: enables magnifier mode
	When in magnifying mode:
	Mouse Wheel zooms in / out
	k: switches automatic contrast enhancement on / off
	h: switches equalized histogram filter on / off
	j: switches invert filter on / off
	g: switches solarized filter on / off
	l: switches posterized filter on / off
	u: switches unsharp mask on / off
	s: switches smart sharpening on / off

F8: Toggles tag display on / off
F9: switches general panel on or off
	With panel active:
	Left mouse click on panel Image: move canvas to mouse position on panel image
	If Gps panel is visible and image contains spatial metadata, left click on coordinates leads to google maps
F11: switches full screen mode on / off
F12: toggles group ID display on / off

Summary:
iTag has been designed at the Institute for Terrestrial and Aquatic Wildlife Research (ITAW,Werftstr. 6 in 25761 Büsum, Germany) for researchers that rely on photographic census techniques of animals that are hard to detect via image recognition algorithms. It was originally developed for counting Grey Seals in the German wadden sea during March 2013. It has since then been further expanded and has now reached beta status.
iTag allows Users to define up to 9 different categories and name them accordingly. In addition, 4 modifiers are available to further increase the options during a tagging session. Users are able to load a series of Images into a session and add tags on objects on these images within previously defined categories and modifiers.
Upon ending the session, result files are produced including (if provided by the EXIF data) the gps information for each Picture, the number of objects in each category and a detailed result file that describes each individual object. In addition, all images that were tagged are saved as well as a legend, in a graphical as well as in a spreadsheet format. All output is written into a folder named after the user created below the image directory. The user can also save the current session and resume at the same point at a later time.

iTag is open Source under LGPL (due to the PIL Library Copyright 1997-2011 by Secret Labs AB and Copyright 1995-2011 by Fredrik Lundh) and may be freely distributed as long as the authors of the program are properly cited (information on how to cite will be made available as soon as possible).

iTag may not be changed in parts or as a whole without previous acknowledgement by the authors themselves.

Feel free to use it for your research and submit any suggestions to the authors!

Contact details:
	itag.biology@yahoo.com
	https://sourceforge.net/projects/itagbiology
	@itag.biology (twitter)
	
Citation:
	Viquerat 2015 (Conference Poster)
	An open source software facilitating the analysis of count data from still images
	29th Conference of the European Cetacean Society, Malta, 2015

New features & bugfixes:
	- added extended functionality for grouping tags
	- added shortcut key to decrease / increase tag size display
	- added command line option to set maximum width / height of image (itag.exe -m10000).	Defaults to 10000 in longest side. Images larger than that will be resized.
	- camdate now uses DatTimeOriginal Exif Info
	- new panel system and features
	- complete UI overhaul
