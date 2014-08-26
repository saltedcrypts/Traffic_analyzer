'''from PIL import Image
im = Image.open("gee-love-black-lines.jpg") #Can be many different formats.
pix = im.load()
print im.size #Get the width and hight of the image for iterating over
print pix[10,10] #Get the RGBA Value of the a pixel of an image
#pix[x,y] = value # Set the RGBA Value of the image (tuple)'''
from PIL import Image
import random as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation

im = plt.imread('testmap.png')
img = Image.open('testmap.png')
pix = img.load()
implot = plt.imshow(im)
#print img.size
print pix[570,115]
'''x_init=11
y_init=446
plt.scatter([x_init],[y_init])'''
var=[(218, 37, 91), (244, 129, 23), (255, 242, 0),(153, 217, 234),(218, 7, 29),
(255, 174, 201),
(195,195,195),
(64, 128, 128),
(128, 64, 0),
(181, 230, 29),
(128, 128, 0),
(184, 254, 133),
(112, 146, 190),
(64, 128, 128),
(63, 72, 204),
(0, 0, 0),
(185, 122, 87),
(163, 73, 164)]
list_p=[]
#x_init>774 or x_init<8 or y_init>281 or y_init<8 
#plt.scatter(a*786,b*293)
'''print img.size'''
for i in range(4,800,8) :
	for j in range(4,305,8):
		if pix[i,j] in var:
			list_p.append((i,j))
			plt.scatter(i,j)

plt.show()