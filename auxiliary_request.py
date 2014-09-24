from sqlite3 import *
import math
import pygame,sys
from pygame.locals import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

BusStop=[[] for i in range(100)]
#BusStop=[[1,2,3],[2,5,4,6],[2,6,8]]
BusPos=[[] for i in range(100)]
x=[35,120,215,120,215,305,396,485,354,320,515,510,570,0,0,0,0,0,0,0,0]
y=[141,84,28,235,185,130,185,132,82,220,230,40,150,0,0,0,0,0,0,0,0]

def calc_dist(i1,i2,t0=1):
    if i1==-1 or i2==-1:
        return 0
    return t0*int(math.sqrt((x[i1]-x[i2])**2+(y[i1]-y[i2])**2))

Time=[[calc_dist(i,j) for i in range(15)] for j in range(15)]



def near(pos,lst,ign=-1):
    #print 'in near'
    ind=-1
    m=1000000000000
    for i in range(len(lst)):
        if lst[i]==-1:
            continue
        if(m>((pos[0]-x[lst[i]])**2+(pos[1]-y[lst[i]])**2) and not(lst[i]==ign)):
            ind=lst[i]
            m=(pos[0]-x[lst[i]])**2+(pos[1]-y[lst[i]])**2
    return ind

def get(bus,stat):
    #print 'in get'
    #print bus,stat,BusPos
    near1=near(BusPos[bus],BusStop[bus])
    near2=near(BusPos[bus],BusStop[bus],near1)
    time=0
    #print near1,near2,BusPos[bus]
    if BusStop[bus].index(near1) < BusStop[bus].index(near2):
        start=BusStop[bus].index(near1)
    else:
        start=BusStop[bus].index(near2)
    time_val=0
    #print 'here'
    mod_len=len(BusStop[bus])
    start=(start+1)%mod_len
    count_steps=0
    #for i in BusStop:
    #    print i
    #print 'stat = ',stat,bus
    while not(BusStop[bus][(start-1)%mod_len]==stat) and count_steps<15:
        #raw_input()
        count_steps+=1
        cur=BusStop[bus][start-1]
        nxt=BusStop[bus][start]
        time_val=time_val+Time[cur][nxt]
        start=(start+1)%mod_len
    return time
    

def request(stat1,stat2):
    con=connect('database/BusPos.db')    
    con_rt=connect('database/BusRoute.db')
    cur_rt=con_rt.cursor()
    cur=con.cursor()
    with con:
        cur.execute("SELECT * FROM BusPos")
        row_positions=cur.fetchall()
        for i in row_positions:
            BusPos[i[0]]=[i[1],i[2]]
        #row_routes=[]
    with con_rt:
        cur_rt.execute("SELECT * FROM BusRoute")
        row_routes=cur_rt.fetchall()
    for i in row_routes:
        #print i
        temp_rt=str(i[1])
        temp_rt=temp_rt[1:-1]
        temp_rt=temp_rt.split(',')
        temp_rt=[int(j) for j in temp_rt if not(j=='')]
        BusStop[i[0]]=temp_rt
    #print BusStop
    pygame.init()
    screen=pygame.display.set_mode((786,293),0,32)
    background=pygame.image.load('testmap.png').convert()
    dot=pygame.image.load('icons/bus.png').convert_alpha()
    screen.blit(background,(0,0))
    pygame.display.update()
    #print 'reached'
    possible=[]
    #print stat1,stat2
    for i in range(len(BusStop)):
        if stat1 in BusStop[i] and stat2 in BusStop[i]:
            possible.append(i)
            #print i
    if len(possible)==0:
        return -1
    minTime=1000000000000
    ind=-1
    for i in possible:
        mod_len=len(BusStop[i])
        start=(BusStop[i].index(stat1)+1)%mod_len
        stop=BusStop[i].index(stat2)
        time_val=0
        count_steps=0
        while not(start==stop) and count_steps<15:
            count_steps+=1
            #print 'looping'
            currn=BusStop[i][start]
            nxt=BusStop[i][(start-1)%mod_len]
            time_val=time_val+Time[currn][nxt]
            start=(start+1)%mod_len
        time_val=time_val+get(i,stat1)
        if time_val<minTime:
            minTime=time_val
            ind=i
    #print ind
    for temp in range(100):
        for event in pygame.event.get():
            if event.type == QUIT: ## defined in pygame.locals
                return [ind,minTime]
        screen.blit(background,(0,0))
        cur.execute("SELECT posx,posy FROM BusPos WHERE Id=%d"%(ind))
        row_list=cur.fetchall()
        #print row_list
        screen.blit(dot,(row_list[0][0],row_list[0][1]))
        pygame.display.update()
        time.sleep(0.4)
    return [ind,minTime]
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
        
    
if __name__=="__main__":
    stat1=int(raw_input('Enter Start Station: '))
    stat2=int(raw_input('Enter destination Station: '))
    request(stat1,stat2)