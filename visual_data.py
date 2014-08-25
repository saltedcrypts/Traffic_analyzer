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
print pix[798,190]
'''x_init=11
y_init=446
plt.scatter([x_init],[y_init])'''
var=[(218, 37, 91), (244, 129, 23), (255, 242, 0),(153, 217, 234),(218, 7, 29),
(255, 174, 201),
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
lpx=0
lpy=0
track=[]
chk_avail=0
dot_product=0
a=r.random()
b=r.random()
x_init=85
y_init=94
for i in range(0,49):
	track.append((-1,-1))
track.append((x_init,y_init))
#693,303
pt,=plt.plot(x_init,y_init,marker='o')
#x_init>774 or x_init<8 or y_init>281 or y_init<8 
#plt.scatter(a*786,b*293)
'''print img.size'''
for it in range(0,1000):
	min_dis=100000
	delx=-11
	dely=-11
	check_avail=0
	for i in range(max(x_init-90,5),min(798,x_init+90)) :
		for j in range(max(y_init-90,5),min(303,y_init+90)):
			if i==x_init and j==y_init:
				continue
			temp_delx=(i-x_init)*5/max(abs(i-x_init),abs(j-y_init))
			temp_dely=(j-y_init)*5/max(abs(i-x_init),abs(j-y_init))
			if pix[i,j] in var and (abs(x_init-i)**2+abs(y_init-j)**2)<=min_dis and ((lpx==0 and lpy==0) or ((x_init-lpx)*(i-x_init)+(y_init-lpy)*(j-y_init)>1)):
				if (min(798,max(x_init+delx,5)),min(303,max(y_init+dely,5))) in track:
					#print "sent"
					continue
				p=r.random()
				if p>0.5:
					continue
				x_m=i
				y_m=j
				dot_product=(x_init-lpx)*(i-x_init)+(y_init-lpy)*(j-y_init)
				min_dis=abs(x_init-i)**2+abs(y_init-j)**2
				delx=(i-x_init)*5/max(abs(i-x_init),abs(j-y_init))
				dely=(j-y_init)*5/max(abs(i-x_init),abs(j-y_init))

	if not (delx==-11 or dely==-11):
		#print delx,dely
		lpx=x_init
		lpy=y_init
		x_init=min(798,max(x_init+delx,5))
		y_init=min(303,max(y_init+dely,5))
		pt.set_data(x_init,y_init)
		track.append((x_init,y_init))
		track=track[len(track)-20:len(track)]
	else:
		lpx=0
		lpy=0
		track.append((-1,-1))
		track=track[len(track)-20:len(track)]
	#print x_init,y_init


	plt.pause(0.001)

'''	else:
		lpx=x_init
		lpy=y_init
		x_init=min(774,max(x_init-4,4))
		y_init=min(281,max(y_init-4,4))
		pt.set_data(x_init,y_init)
		'''




