#letters.py

import csv
import re
import glob
from PIL import Image
import io
import os
import sys
import argparse
import time

# This is considered poor form--it's kind of an extreme way to make sure that Unicode
# behaves the way we want it to in Python 2.7. It's bloody, but it works.
reload(sys)
sys.setdefaultencoding('utf-8')

# To use this code at the command line on a folder that you choose, uncomment the following 
# lines (by deleting the single quotes on line 22 and line 31). The argparse library will 
#accept arguments from the command line and pass them to the rest of the script as variables. 
# Usage: python letters.py -i path/to/TIFF/folder/ -o path/to/glyph/destination
'''
parser = argparse.ArgumentParser(description='Define input (folder of TIFF/box pairs) and output folder for resulting glyphs.')
parser.add_argument('-i', action='store', dest='source', help='Give path to TIFF file or folder of TIFFs')
parser.add_argument('-o', action='store', dest='destination', help='Give path to desired destination for output glyphs')
	
args = parser.parse_args()

source = args.source
destination = args.destination
'''

source = '/media/sf_RBSDigitalApproaches/data/0613_Thursday_data/Page_images/UVA_1730j/BW/'
destination = '/media/sf_RBSDigitalApproaches/output/Glyphs'

start_time = time.time()
count = 0

# If the destination folder doesn't exist, create it.
if not os.path.isdir(destination) :
	os.makedirs(destination)

print('Working on TIFF files in ' + source + '...')

# Loop through all the TIFF files in the folder
for filename in glob.glob(source + '*.tif') :
	print('\tFound TIFF file ' + filename)
	filename_root = filename.rstrip('.tif')
	pagenum = filename_root[-3:]
	boxfile_name = filename_root + '.box'
	
	# Open the TIFF file with pillow
	im = Image.open(filename)
	# Get the height of the image (in pixels)
	height = im.height
	
	# Look for the boxfile
	if os.path.isfile(boxfile_name) :
		print('Opening ' + boxfile_name)
		with open(boxfile_name, "rb") as boxfile :	
			# Read the boxfile, using spaces as the delimiters instead of commas.
			reader = csv.reader(boxfile, delimiter=' ', quotechar='"')
			print('Reading ' + boxfile_name)
			# Work through each row of the boxfile
			for row in reader :
				print('Reading row...')
				# Figure out what character is on each line of the boxfile
				char = row[0].encode('unicode_escape')
				# Get the character's coordinates from the boxfile.
				# The y coordinates have to be subtracted from the image height because
				# Tesseract starts counting from the bottom left corner, while pillow 
				# starts counting from the top left corner.
				x1 = int(row[1])
				y1 = height - int(row[2])
				x2 = int(row[3])
				y2 = height - int(row[4])
				# Calculate the width and height of the letter, based on its coordinates
				w = x2 - x1
				h = y2 - y1
				
				# Loads of tedious logic around unicode codes and characters that wouldn't
				# make for good file names
				if re.findall('e6',char) :
					char = 'u00e6'
				elif char == '\u2019' :
					char = 'apostrophe'
				elif char == '\u201C' :
					char = 'lquot'
				elif char == '\u201D' :
					char = 'rquot'
				elif re.findall('\u',char) :
					char = char.replace('\\','')
				elif char == "~" :
					char = 'tilde'
				elif char == '.' :
					char = 'period'
				elif char == ',' :
					char = 'comma'
				elif char == ':' :
					char = 'colon'
				elif char == ';' :
					char = 'semicolon'
				elif char == '!' :
					char = 'exclamation'
				elif char == '(' :
					char = 'lparen'
				elif char == ')' :
					char = 'rparen'
				elif char == '-' :
					char = 'hyphen'
				elif char == '?' :
					char = 'question'
				
				# Check to see if the character is upper- or lower-case
				upper = re.compile('[A-Z]')
				lower = re.compile('[a-z]')
				# Check to see if character is a punctuation mark
				punct = re.compile('tilde|period|comma|colon|semicolon|apostrophe|quot|exclamation|lparen|rparen|hyphen|question')
				if re.findall(punct, char) :
					char = char
				# Prepend "Upper-" or "lower-" to the name of the character
				elif re.findall(upper, char) :
					char = 'Upper-' + char
				elif re.findall(lower, char) :
					char = 'lower-' + char
				
				# Check to see if there's already a folder for this character. If not, 
				# create one.
				if not os.path.isdir(destination + '/' + char) :
					os.mkdir(destination + '/' + char)
				
				# Use pillow to create an image of the character by cropping the page image
				# at the coordinates from the box file	
				letter = im.crop((float(x1),float(y2),float(x2),float(y1)))
				# Assemble a filename for the character
				letter_filename = char + '-' + str(pagenum) + '-' + str(x1) + '-' + str(y2) + '-' + str(x2) + '-' + str(y1) + '.jpg'
				
				# Save the character of the image as a .jpg 
				letter.save(destination + '/' + char + '/' + letter_filename, dpi=(600,600), "JPEG")
				print('Writing ' + letter_filename)
				count += 1
				letter.close()
	# 			
			boxfile.close()
			im.close()
end_time = time.time()
elapsed_time = end_time - start_time
print('Isolated ' + str(count) + ' characters. Elapsed time: ' + str(elapsed_time) + ' seconds.')