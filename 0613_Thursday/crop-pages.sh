#This script crops to the gutter of the recto and verso pages of the Sophonisba page
#images provided by UVA Digitization Services.
#
#Place this file in the folder of sequentially numbered *color* TIFF files 
#(01.tif, 02.tif, etc.). To run the script, navigate to that folder in the terminal and
#type bash crop-pages.sh
#
#Several lines below are commented out below for teaching purposes. When you are ready
#to actually crop your page images, you should uncomment lines 19, 27, and 31. You will
#  probably want to comment out lines 25, 26, 29, and 30.
#
#When line 19 is uncommented, the script will make a new directory called cropped;
#Lines 27 and 31 expect that directory to be in place so that the resulting cropped
#page images can be placed there.
#
#Note that the value of 140 pixels in lines 27 and 31 is specific to the Sophonisba
#images from UVA. You would need to adjust that number for other images.

mkdir cropped
for file in *.tif
do
filenum=${file%*.tif}
	if [ $(((10#$filenum-8)%2)) -eq 0 ]
		then 
 		echo $filenum is really $((10#$filenum-8)), which is even
# 		echo ${file%.tif}-crop.tif
		convert -gravity East -chop 140x0 -quiet $file[0] cropped/${file%.tif}-crop.tif
	else 
 		echo $filenum is really $((10#$filenum-8)), which is odd
# 		echo ${file%.tif}-crop.tif
		convert -gravity West -chop 140x0 -quiet $file[0] cropped/${file%.tif}-crop.tif

	fi 
done