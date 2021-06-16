##colors
grey='#C0C0C0'
lightgrey='#E8E8E8'
white='#FFFFFF'
black='#000000'
blue='#0000FF'
red='#FF0000'
orange='#F29B24'

def col_invert(color): #ok!
	table = '0123456789abcdef'.translate(str.maketrans('0123456789abcdef','fedcba9876543210'))
	return color.lower().translate(table).upper()

def rgb2lab(inputColor) :
	num = 0
	RGB = [0, 0, 0]
	for value in inputColor :
		value = float(value) / 255
		if value > 0.04045 :
			value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
		else :
			value = value / 12.92
		RGB[num] = value * 100
		num = num + 1
	XYZ = [0, 0, 0,]
	X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
	Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
	Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
	XYZ[ 0 ] = round( X, 4 )
	XYZ[ 1 ] = round( Y, 4 )
	XYZ[ 2 ] = round( Z, 4 )
	XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2, Illuminant= D65
	XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
	XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883
	num = 0
	for value in XYZ :
		if value > 0.008856 :
			value = value ** ( 0.3333333333333333 )
		else :
			value = ( 7.787 * value ) + ( 16 / 116 )
		XYZ[num] = value
		num = num + 1
	Lab = [0, 0, 0]
	L = ( 116 * XYZ[ 1 ] ) - 16
	a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
	b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )
	Lab [ 0 ] = round( L, 4 )
	Lab [ 1 ] = round( a, 4 )
	Lab [ 2 ] = round( b, 4 )
	return Lab

def hex_to_rgb(value):
	value = value.lstrip('#')
	lv = len(value) #this is 6
	steps = int(lv/3) #this is 2
	out = tuple( int(value[i:i+steps],16) for i in range(0, lv, steps) )
	return out

def deltaE(col1,col2):
	from math import sqrt
	return sqrt((col1[0]-col2[0])**2 + (col1[1]-col2[1])**2 + (col1[2]-col2[2])**2)

def same_cols(col1,col2,crit=50):
	c1 = hex_to_rgb(col1)
	c2 = hex_to_rgb(col2)
	c1 = rgb2lab(c1)
	c2 = rgb2lab(c2)
	if deltaE(c1,c2) > crit: # 2.3 is jnd (see color difference wikipedia) #higher values, more distinct
		return True
	else:
		return False
