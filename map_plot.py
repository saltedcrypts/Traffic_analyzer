from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sqlite3 import *
import sys
from random import *
import matplotlib.animation as animation
im = plt.imread('testmap.png')
img = Image.open('testmap.png')
pix = img.load()
implot = plt.imshow(im)
x=[35,120,215,120,215,305,396,485,621,759,354,320]
y=[141,84,28,235,185,130,185,132,184,78,82,220]
plt.scatter(x,y)
bus2=[[127,103],[225,45],[-1,0],[253,26],[305,112],[349,85],[-1,0],[401,173],[317,211],[-1,0],[221,277],[117,107],[127,103]]
for i in bus2:
    plt.scatter(i[0],i[1],marker='+')
plt.show()


a=raw_input()
