import matplotlib.pyplot as plt
from random import *
import matplotlib.animation as animation
im = plt.imread('testmap.png')
plt.imshow(im)
x=[35,120,215,120,215,305,396,485,621,759]
y=[141,84,28,235,185,130,185,132,184,78]
test_points=[[0,[0,0]] for i in range(30)]+[[1,[0,0]] for i in range(30)]+[[2,[0,0]] for i in range(30)]
for i in range(len(x)):
    tem=[[-1,[x[i]-5+10*random(),y[i]-5+10*random()]] for j in range(20)]
    test_points=test_points+tem
bus1=[[44,152],[130,100],[-1,0],[225,45],[-1,0],[255,28],[313,126],[-1,0],[358,197],[268,250],[228,180],[-1,0],[218,165],[75,251],[20,166],[44,152]]

bus2=[[127,103],[253,26],[305,112],[349,85],[401,173],[221,277],[117,107],[127,103]]
bus3=[[349,89],[480,9],[532,91],[682,7],[790,93],[710,158],[617,44],[401,172],[348,89]]
pos=[[44,152],[127,103],[349,89]]
busses=[bus1,bus2,bus3]
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
    else:
        return pos[test_points[ind][0]]
def dist(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
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

pt=[0 for i in range(0,len(test_points))]
for i in range(len(test_points)):
    tem=post(i)
    #print tem
    pt[i],=plt.plot(tem[0],tem[1],marker='o')
plt.scatter(x,y)
for i in range(1000):
    
    i1=i%len(rtx[0])
    if(i1>0 and [rtx[0][i1],rty[0][i1]]==[rtx[0][i1-1],rty[0][i1-1]] and not([rtx[0][i1-2],rty[0][i1-2]]==[rtx[0][i1],rty[0][i1]])):
        n=near([rtx[0][i1],rty[0][i1]])
        for k in range(len(test_points)):
            if(test_points[k][0]==-1 and dist([x[n],y[n]],test_points[k][1])<5 and random()<0.2):
                test_points[k][0]=0
                brd=brd+1
                
        for k in range(len(test_points)):
            if(test_points[k][0]==0 and random()<0.2):
                dbrd=dbrd+1
                test_points[k][0]=-1
                test_points[k][1]=[x[near([rtx[0][i1],rty[0][i1]])],y[near([rtx[0][i1],rty[0][i1]])]]
        print brd,dbrd          
    pos[0]=[rtx[0][i1],rty[0][i1]]  
    if(i<len(rtx[1])):
        pos[1]=[rtx[1][i],rty[1][i]]
        
    if(i<len(rtx[2])):
        pos[2]=[rtx[2][i],rty[2][i]]
        
    for j in range(len(test_points)):
        tem=post(j)
        pt[j].set_data(tem[0]+random()*((-1)**j),tem[1]+random()*((-1)**j))
    plt.pause(0.000000001)

plt.show()
