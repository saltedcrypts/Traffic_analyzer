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
print img.size
num_points=1
#print pix[798,190]
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
for i in range(4,786,4) :
	for j in range(4,293,4):
		if pix[i,j] in var:
			list_p.append((i,j))
			#plt.scatter(i,j)

lpx=[]
lpy=[]
track=[]
chk_avail=0
dot_product=0
a=r.random()
b=r.random()
x_init=85
y_init=94

for j in range(0,num_points):
	track.append([])
	lpx.append(0)
	lpy.append(0)
	for i in range(0,150):
		track[j].append((-1,-1))
point_l=[]
point_c=[]
#693,303
print lpx
print lpy
for i in range(0,num_points):
	a=r.random()
	b=r.random()
	pt,=plt.plot(a*786,b*293,marker='o')
	point_l.append(pt)
	point_c.append([a*786,b*293])
	track[i].append((a*786,b*293))
#x_init>774 or x_init<8 or y_init>281 or y_init<8 
#plt.scatter(a*786,b*293)
'''print img.size'''
for it in range(0,1000):
	for pnt in range(len(point_c)):
		if pix[point_c[pnt][0],point_c[pnt][1]] in var:
			min_dis=20
		else:
			min_dis=100000
		delx=-11
		dely=-11
		x_m=0
		y_m=0
		curr_dot=1
		dot_product=0
		x_init=point_c[pnt][0]
		y_init=point_c[pnt][1]
		for i in list_p:
			if (i[0]-x_init)==0 and (i[1]-y_init)==0:
				continue
			print_val=(i[0]-x_init)**2+(i[1]-y_init)**2
			entered=0
			if (i[0]-x_init)**2	+ (i[1]-y_init)**2 <= min_dis:
				print (i[0]-x_init)**2	+ (i[1]-y_init)**2 <= min_dis, (i[0],i[1]) not in track[pnt], ( curr_dot*((i[0]-x_init)*(x_init-lpx[pnt])+(i[1]-y_init)*(y_init-lpy[pnt]))>=0)
			if (i[0]-x_init)**2	+ (i[1]-y_init)**2 <= min_dis and (i[0],i[1]) not in track[pnt] and ( curr_dot*((i[0]-x_init)*(x_init-lpx[pnt])+(i[1]-y_init)*(y_init-lpy[pnt]))>=0):
				entered=1
				if not(curr_dot==1):
					curr_dot=1
				min_dis=(i[0]-x_init)**2 + (i[1]-y_init)**2
				x_m=i[0]
				y_m=i[1]
				dot_product=(i[0]-x_init)*(x_init-lpx[pnt])+(i[1]-y_init)*(y_init-lpy[pnt])
				p=r.random()
				if p>0.9:
					break
		print x_m, y_m, entered
		#print track[pnt]
		if x_m==0 and y_m==0:
			track[pnt]=[(-1,-1) for i in track[pnt]]
			track[pnt][-1]=(x_init,y_init)
			curr_dot=0
		else:
			lpx[pnt]=x_init
			lpy[pnt]=y_init
			track[pnt].append((x_init,y_init))
			track[pnt]=track[pnt][len(track[pnt])-100:len(track[pnt])]
			x_init=x_m
			y_init=y_m
		point_l[pnt].set_data(x_init,y_init)
		point_c[pnt][0]=x_init
		point_c[pnt][1]=y_init
	plt.pause(0.1)