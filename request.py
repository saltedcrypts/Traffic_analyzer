from sqlite3 import *
import math
import pygame,sys
from pygame.locals import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

BusStop=[[] for i in range(50)]
#BusStop=[[1,2,3],[2,5,4,6],[2,6,8]]
BusPos=[[200,35],[300,120],[250,350]]
x=[35,120,215,120,215,305,396,485,354,320,515,510,570]
y=[141,84,28,235,185,130,185,132,82,220,230,40,150]

def calc_dist(i1,i2,t0=1):
    return t0*int(math.sqrt((x[i1]-x[i2])**2+(y[i1]-y[i2])**2))

Time=[[calc_dist(i,j) for i in range(10)] for j in range(10)]



def near(pos,lst,ign=-1):
    ind=-1
    m=1000000000000
    for i in range(len(lst)):
        if(m>((pos[0]-x[lst[i]])**2+(pos[1]-y[lst[i]])**2) and not(lst[i]==ign)):
            ind=lst[i]
            m=(pos[0]-x[lst[i]])**2+(pos[1]-y[lst[i]])**2
    return ind

def get(bus,stat):
    print bus,stat,BusPos
    near1=near(BusPos[bus],BusStop[bus])
    near2=near(BusPos[bus],BusStop[bus],near1)
    time=0
    print near1,near2,BusPos[bus]
    if BusStop[bus].index(near1) < BusStop[bus].index(near2):
        start=near1
    else:
        start=near2
    time=0
    mod_len=len(BusStop[bus])
    start=(start+1)%mod_len
    while not(start+1==stat):
        cur=BusStop[bus][start-1]
        nxt=BusStop[bus][start]
        time=time+Time[cur][nxt]
        start=(start+1)%mod_len
    return time
    

def request(stat1,stat2):
    con_rt=connect('database/BusRoute.db')
    cur_rt=con_rt.cursor()
    #row_routes=[]
    with con_rt:
        cur_rt.execute("SELECT * FROM BusRoute")
        row_routes=cur_rt.fetchall()
    for i in row_routes:
        #print i
        temp_rt=str(i[1])
        temp_rt=temp_rt[1:-1]
        temp_rt=temp_rt.split(',')
        temp_rt=[int(j) if not(j=='') else -1 for j in temp_rt]
        BusStop[i[0]]=temp_rt
    #print BusStop
    pygame.init()
    screen=pygame.display.set_mode((786,293),0,32)
    background=pygame.image.load('testmap.png').convert()
    dot=pygame.image.load('download.png').convert_alpha()
    screen.blit(background,(0,0))
    pygame.display.update()
    possible=[]
    for i in range(len(BusStop)):
        if stat1 in BusStop[i] and stat2 in BusStop[i]:
            possible.append(i)
    if len(possible)==0:
        return -1
    minTime=1000000000000
    ind=-1
    for i in possible:
        start=BusStop[i].index(stat1)
        stop=BusStop[i].index(stat2)
        time_val=0
        while not(start==stop):
            cur=BusStop[i][start]
            nxt=BusStop[i][start+1]
            time_val=time_val+Time[cur][nxt]
            start=start+1
        time_val=time_val+get(i,stat1)
        if time_val<minTime:
            minTime=time_val
            ind=i
    con=connect('database/BusPos.db')
    cur=con.cursor()
    for temp in range(100):
        screen.blit(background,(0,0))
        cur.execute("SELECT posx,posy FROM BusPos WHERE Id=%d"%(ind))
        row_list=cur.fetchall()
        #print row_list
        screen.blit(dot,(row_list[0][0],row_list[0][1]))
        pygame.display.update()
        time.sleep(0.5)

    return ind
'''
con=connect('database/BusPos.db')
cur=con.cursor()
with con:
    while True:
        raw_input("Press any key ")
        cur.execute("SELECT * FROM BusPos")
        a=cur.fetchall()
        #print a
'''
request(2,9)


        
    
