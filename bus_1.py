'''from PIL import Image
im = Image.open("gee-love-black-lines.jpg") #Can be many different formats.
pix = im.load()
print im.size #Get the width and hight of the image for iterating over
print pix[10,10] #Get the RGBA Value of the a pixel of an image
#pix[x,y] = value # Set the RGBA Value of the image (tuple)'''

from PIL import Image
import math
import random as r
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sqlite3 import *
import sys
from random import *
import matplotlib.animation as animation
from math import *
from direction import *
## --------------------------------------------------##

con=connect('database/database.db')
cur=con.cursor()
im = plt.imread('testmap.png')
img = Image.open('testmap.png')
pix = img.load()
implot = plt.imshow(im)
print img.size

## var STORES THE LIST OF PIXELS WHICH CONSTITUTE TH ROAD
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

point_l=[]
point_c=[]

#####################################################################################################################################################################


x=[35,120,215,120,215,305,396,485,621,759,354,320]
y=[141,84,28,235,185,130,185,132,184,78,82,220]
test_points=[[0,[0,0]] for i in range(30)]+[[1,[0,0]] for i in range(30)]+[[2,[0,0]] for i in range(30)]
for i in range(len(x)):
    tem=[[-1,[x[i]-5+10*random(),y[i]-5+10*random()]] for j in range(20)]
    test_points=test_points+tem
bus1=[[38,145],[126,96],[-1,0],[220,37],[-1,0],[248,22],[309,125],[-1,0],[350,191],[315,215],[-1,0],[263,243],[226,179],[-1,0],[212,160],[64,246],[15,160],[38,145],[-1,0]]
bus2=[[126,92],[220,37],[-1,0],[248,22],[298,105],[341,81],[-1,0],[393,166],[315,211],[-1,0],[215,271],[112,100],[126,92],[-1,0]]
bus3=[[349,89],[480,9],[532,91],[682,7],[784,93],[710,158],[617,44],[401,172],[348,89]]
pos=[[44,152],[127,103],[349,89]]
busses=[bus1,bus2,bus3]

#####    DEFINING AUXILIARY FUNCTIONS

def near(pos):
    ind=-1
    m=1000000000000
    for i in range(len(x)):
        if(m>((pos[0]-x[i])**2+(pos[1]-y[i])**2)):
            ind=i
            m=(pos[0]-x[i])**2+(pos[1]-y[i])**2
    return ind
def post(ind):
    if(test_points[ind][0]==-1):
        return test_points[ind][1]
    elif(test_points[ind][0]==-2):
    #print [0,0]
        return 0
    else:
        return pos[test_points[ind][0]]
def dist(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def poissons_rand(l):
    return (-1*math.log(1-random())*l)



########################################################   END AUXILIARY DEFINITION SECTION   #########

rtx=[]
rty=[]
for bus in busses:
    routex=[]
    routey=[]
    for i in range(1,len(bus)):
        if(bus[i][0]==-1):
            temx=[bus[i-1][0]]*5
            temy=[bus[i-1][1]]*5
            routex=routex+temx
            routey=routey+temy
            bus[i]=bus[i-1]
            continue
            
        init=bus[i-1]
        fin=bus[i]
        dx=(fin[0]-init[0])
        dy=(fin[1]-init[1])
        mag=(dx**2+dy**2)**0.5
        s=int(5*random())+3
        dx=(dx/mag)*s
        dy=(dy/mag)*s
        temx=[init[0]+i*dx for i in range(0,int(mag/s))]
        temy=[init[1]+i*dy for i in range(0,int(mag/s))]
        routex=routex+temx
        routey=routey+temy
    rtx.append(routex)
    rty.append(routey)
brd=0
dbrd=0
random_id=[]
next_index=290
pt=[0 for i in range(0,len(test_points))]
for i in range(len(test_points)):
    tem=post(i)
    #print tem
    pt[i],=plt.plot(tem[0],tem[1],marker='o')
plt.scatter(x,y)
ptbus,=plt.plot(rtx[0][0],rty[0][0],marker='o')

for i in range(1000):
    
    try:
        cur.execute("CREATE TABLE Data_%d(Id INT, posx FLOAT, posy FLOAT, speed FLOAT, Direction INT,Street TEXT )"%i)
    except:
        cur.execute("DROP TABLE IF EXISTS Data_%d"%i)
        cur.execute("CREATE TABLE Data_%d(Id INT, posx FLOAT, posy FLOAT , speed FLOAT, Direction INT, Street TEXT)"%i)
        pass
    
    i1=i%len(rtx[0])
    if(i1>0 and [rtx[0][i1],rty[0][i1]]==[rtx[0][i1-1],rty[0][i1-1]] and not([rtx[0][i1-2],rty[0][i1-2]]==[rtx[0][i1],rty[0][i1]])):
        n=near([rtx[0][i1],rty[0][i1]])
        board_number=poissons_rand(8);
        print 'board', board_number
        # NUMBER OF PEOPLE WHO BOARD IS DEPENDANT ON THE BUS -- LAMBDA=AVG NUMBER WHO BOARD A BUS
        for k in range(len(test_points)):
            if(board_number==0):
                break
            if(test_points[k][0]==-1 and dist([x[n],y[n]],test_points[k][1])<5 and board_number>0):
                board_number=board_number-1
                test_points[k][0]=0
                brd=brd+1

        # NUMBER OF PEOPLE WHO DEBOARD IS DEPENDANT ON THE STOP -- LAMBDA=AVG NUMBER WHO GET DOWN AT THE STOP                
        deboard_number=int(poissons_rand(12))+4
        print 'deboard', deboard_number
        deboard_number=deboard_number%10
        for k in range(len(test_points)):
            if (deboard_number<=0):
                break
            if(test_points[k][0]==0 and deboard_number>0):
                deboard_number=deboard_number-1
                dbrd=dbrd+1
                test_points[k][0]=-1
                random_id.append(next_index)
                next_index=next_index+1
                test_points[k][1]=[x[near([rtx[0][i1],rty[0][i1]])],y[near([rtx[0][i1],rty[0][i1]])]]
                ar=math.ceil(random()*20)-10
                br=math.ceil(random()*20)-10
        
                pt_rand,=plt.plot(test_points[k][1][0]+ar,test_points[k][1][1]+br,marker='o')
                track.append([])
                lpx.append(0)
                lpy.append(0)
                for filler in range(0,150):
                        track[-1].append((-1,-1))
                point_l.append(pt_rand)
                point_c.append([test_points[k][1][0]+ar,test_points[k][1][1]+br])
                track[-1].append((test_points[k][1][0]+ar,test_points[k][1][1]+br))
                if(len(point_l)>1000):
                    point_l=point_l[-1000:]
                    point_c=point_c[-1000:]
                    track=track[-1000:]
                    lpx=lpx[-1000:]
                    lpy=lpx[-1000:]
    #ptbus.set_data(rtx[0][i1],rty[0][i1])
    pos[0]=[rtx[0][i1],rty[0][i1]]                      
    i1=i%len(rtx[1])
    if(i1>0 and [rtx[1][i1],rty[1][i1]]==[rtx[1][i1-1],rty[1][i1-1]] and not([rtx[1][i1-2],rty[1][i1-2]]==[rtx[1][i1],rty[1][i1]])):
        n=near([rtx[0][i1],rty[0][i1]])
        board_number=poissons_rand(8);
        print 'board', board_number
        # NUMBER OF PEOPLE WHO BOARD IS DEPENDANT ON THE BUS -- LAMBDA=AVG NUMBER WHO BOARD A BUS
        for k in range(len(test_points)):
            if(board_number==0):
                break
            if(test_points[k][0]==-1 and dist([x[n],y[n]],test_points[k][1])<5 and board_number>0):
                board_number=board_number-1
                test_points[k][0]=1
                brd=brd+1

        # NUMBER OF PEOPLE WHO DEBOARD IS DEPENDANT ON THE STOP -- LAMBDA=AVG NUMBER WHO GET DOWN AT THE STOP                
        deboard_number=int(poissons_rand(12))+4
        print 'deboard', deboard_number
        deboard_number=deboard_number%13
        for k in range(len(test_points)):
            if (deboard_number<=0):
                break
            if(test_points[k][0]==1 and deboard_number>0):
                #print 'here'
                deboard_number=deboard_number-1
                dbrd=dbrd+1
                test_points[k][0]=-1
                random_id.append(next_index)
                next_index=next_index+1
                test_points[k][1]=[x[near([rtx[1][i1],rty[1][i1]])],y[near([rtx[1][i1],rty[1][i1]])]]
                ar=math.ceil(random()*20)-10
                br=math.ceil(random()*20)-10
        
                pt_rand,=plt.plot(test_points[k][1][0]+ar,test_points[k][1][1]+br,marker='o')
                track.append([])
                lpx.append(0)
                lpy.append(0)
                for filler in range(0,150):
                        track[-1].append((-1,-1))
                point_l.append(pt_rand)
                point_c.append([test_points[k][1][0]+ar,test_points[k][1][1]+br])
                track[-1].append((test_points[k][1][0]+ar,test_points[k][1][1]+br))
                if(len(point_l)>1000):
                    point_l=point_l[-1000:]
                    point_c=point_c[-1000:]
                    track=track[-1000:]
                    lpx=lpx[-1000:]
                    lpy=lpx[-1000:]
    #print pos[1],
    pos[1]=[rtx[1][i1],rty[1][i1]]
    pos[2]=[rtx[2][i%len(rtx[2])],rty[2][i%len(rtx[2])]]
    for j in range(len(test_points)):
        tem=post(j)
        if tem==0:
            continue
        if(test_points[j][0]==-1):
            
            direct=int(ceil(4*random()))
            speed=10+10*random()
        else:
            bus_no=test_points[j][0]
            if(rtx[bus_no][i%len(rtx[bus_no])]==rtx[bus_no][(i-1)%len(rtx[bus_no])] and rty[bus_no][i%len(rty[bus_no])]==rty[bus_no][(i-1)%len(rty[bus_no])]):
                #print 'stopped'
                direct=int(ceil(4*random()))
                speed=2+1*random()
            else:                                                                                    
                direct=get_dir(rtx[bus_no][(i-1)%len(rtx[bus_no])],rty[bus_no][(i-1)%len(rty[bus_no])],rtx[bus_no][i%len(rtx[bus_no])],rty[bus_no][i%len(rty[bus_no])])
                speed=50+10*random()
        #pt[j].set_data(tem[0]+random()*((-1)**j),tem[1]+random()*((-1)**j))
        street=str(pix[int(tem[0]),int(tem[1])])
        cur.execute('INSERT INTO Data_%d VALUES(%d,%f,%f,%f,%d,"%s")'%(i,j,tem[0],tem[1],speed,direct,street))
        
    
    plt.pause(0.001)
    it=i
    for pnt in range(len(point_c)):
        if pix[point_c[pnt][0],point_c[pnt][1]] in var:
                min_dis=80
        else:
                min_dis=1000
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
                if (i[0]-x_init)**2 + (i[1]-y_init)**2 <= min_dis and (i[0],i[1]) not in track[pnt] and ( curr_dot*((i[0]-x_init)*(x_init-lpx[pnt])+(i[1]-y_init)*(y_init-lpy[pnt]))>0):
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
        #print track[pnt]
        if x_m==0 and y_m==0:
                track[pnt]=[(-1,-1) for i in track[pnt]]
                track[pnt][-1]=(x_init,y_init)
                lpx[pnt]=2*x_init-lpx[pnt]
                lpy[pnt]=2*y_init-lpy[pnt]
        else:
                lpx[pnt]=x_init
                lpy[pnt]=y_init
                track[pnt].append((x_init,y_init))
                track[pnt]=track[pnt][len(track[pnt])-100:len(track[pnt])]
                x_init=x_m
                y_init=y_m

        #point_l[pnt].set_data(x_init,y_init)
        point_c[pnt][0]=x_init
        point_c[pnt][1]=y_init
        street=str(pix[int(x_init),int(y_init)])
        cur.execute('INSERT INTO Data_%d VALUES(%d,%f,%f,%f,%d,"%s")'%(it,random_id[pnt],x_init,y_init,50+10*random(),int(ceil(4*random())),street))
    plt.pause(0.001)        
#plt.show()
