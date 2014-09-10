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
bus1=[[38,145],[126,96],[-1,0],[220,37],[-1,0],[248,22],[309,125],[-1,0],[350,191],[315,215],[-1,0],[263,243],[226,179],[-1,0],[212,160],[64,246],[15,160],[38,145]]
bus2=[[126,92],[220,37],[-1,0],[248,22],[298,105],[341,81],[-1,0],[393,166],[315,211],[-1,0],[215,271],[112,100],[126,92]]
bus3=[[349,89],[480,9],[532,91],[682,7],[790,93],[710,158],[617,44],[401,172],[348,89]]
for i in bus3:
    plt.scatter(i[0],i[1],marker='+')
plt.show()


a=raw_input()
