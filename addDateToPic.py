#!/usr/bin/python3

import cv2
import os
import argparse
import exifread
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#Get Date info from Pic
def getDate (path):
    #return Image.open(dirPath + '/' + path)._getexif()[36867][0:10]
    with open(dirPath + '/' + path, 'rb') as fh:
        try:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            return str(tags["EXIF DateTimeOriginal"].values)[0:10]
        except:
            print("No EXIF data for" + path)
            return ""

#resize Img to fit FullHD
def resizeImg (image, width=1920, high=1080, fill_color=(0,0,0,0)):

    image.thumbnail((width,high))
    x,y = image.size

    new_image = Image.new('RGB', (width, high), fill_color)
    new_image.paste(image, (int((width-x) / 2 ), int((high-y) / 2)))

    return new_image

#add date text to image
def putText (path):

    image = Image.open(dirPath + '/' + path)

    new_image = resizeImg(image)

    # get date from EXIF
    imageDate = getDate(path)
    
    draw = ImageDraw.Draw(new_image)
    myfont = ImageFont.truetype(fontPath, size=fontSize)
    draw.text((10, 10), imageDate, font=myfont, fill=fontColor)
    
    new_image.save(workPath + imageDate.replace(':','') + path + '.jpg',
               'jpeg')

# Construct the argument parser and parse the arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--directory", required=False, default='.', help="Specify image directory.")
arg_parser.add_argument("-fp", "--fontpath", required=False, default='/usr/share/fonts/gnu-free/FreeMonoBold.ttf', help="Specity font file path.")
arg_parser.add_argument("-fs", "--fontsize", required=False, default=200, help="Specify font size.")
arg_parser.add_argument("-fc", "--fontcolor", required=False, default='#FF0000', help="Specify font color.")
arg_parser.add_argument("-w", "--workpath", required=False, default='./workpath/', help="Specify work path.")
args = vars(arg_parser.parse_args())

# Arguments
dirPath   = args['directory']
fontPath  = args['fontpath']
fontSize  = args['fontsize']
fontColor = args['fontcolor']
workPath  = args['workpath']

if not os.path.exists(workPath):
    os.makedirs(workPath)

for f in os.listdir(dirPath):
    putText (f)
