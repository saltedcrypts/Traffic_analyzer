from sqlite3 import *
import matplotlib.pyplot as plt
import sys
from random import *
import matplotlib.animation as animation
im = plt.imread('testmap.png')
implot = plt.imshow(im)
pt=[0 for i in range(1000)]
con=connect('database/database.db')
cur=con.cursor()
pos=[[-1,-1] for i in range(1000)]
stationx=[35,120,215,120,215,305,396,485,621,759,354,320]
stationy=[141,84,28,235,185,130,185,132,184,78,82,220]
bus=[[]]
new_bus=0
rows=[]
def dist(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
def SortKey(a):
    return a[3]
def SetDiff(a,b):
    a.sort()
    b.sort()
    thres=0.4
    common=0
    for i in a:
        if(i in b):
            common=common+1
    if(common>(thres)*len(a)):
        return 1
    else:
        return 0

def cluster(a):
    a.sort(key=SortKey)
    minspeed=30
    thres=5
    a=[i for i in a if i[3]>minspeed]
    adj_list=[[] for j in range(len(a))]
    for i in a:
        for j in a:
            if i==j:
                continue
            if dist([i[1],i[2]],[j[1],j[2]])<5 and i[4]==j[4] and abs(i[3]-j[3])<10:
                adj_list[a.index(i)].append(a.index(j))
    # RUNNING DFS TO IDENTIFY THE CLUSTER
    visited=[0 for i in range(len(a))]
    stack=[]
    visit_node=0
    curr_iter=1
    while(visit_node<len(a)):
        for j in range(len(a)):
            if visited[j]==0:
                visited[j]=curr_iter
                stack.append(a[j])
                visit_node=visit_node+1
                break
        while(len(stack)>0):
            temp=stack.pop()
            temp=a.index(temp)
            for i in adj_list[temp]:
                if visited[i]==0:
                    visited[i]=curr_iter
                    stack.append(a[i])
                    visit_node=visit_node+1
        curr_iter=curr_iter+1
    tem=[]
    for i in range(1,curr_iter):
        temp=[a[j][0] for j in range(len(visited)) if visited[j]==i]
        if len(temp)>thres:
            tem.append(temp)
    #print tem
    return tem
def avg(a):
    if(len(a))==0:
        return 0
    speed=0
    for i in a:
        speed=speed+i[3]
    speed=speed/len(a)
    return speed

def max_sp(a):
    if(len(a))==0:
        return 0
    speed=0
    for i in a:
        if i[3]>speed:
            speed=i[3]
    return speed


def preserve(bus,rows):
    tem=[]
    for i in bus:
        tmp=[]
        for j in i:
            tmp.append(rows[j])
        if max_sp(tmp)<30:
            tem.append(i)
            continue
        #print tmp
        tem=tem+cluster(tmp)
    return tem
    

for i in range(400):

    cur.execute("SELECT * FROM Data_%d ORDER BY Id"%i)
    rows = cur.fetchall()
    rows.sort()
    for j in rows:
        pos[j[0]]=[j[1],j[2]]
    
    for j in range(len(stationx)):
        tem=[]
        for k in rows:
            if(dist([stationx[j],stationy[j]],pos[k[0]])<20):
                #print k[0],j
                
                tem.append(k)
        
        NewBus=cluster(tem)
        rem=[]
        ne=[]
        for k in NewBus:
            for l in bus:
                if l==[] or k==[]:
                    continue
                if SetDiff(l,k) == 1:
                    #print l,k
                    
                    bus[bus.index(l)]=k
                    rem.append(k)
        for k in rem:
            if k in NewBus:
                NewBus.remove(k)
        for adder in NewBus:
            if adder in bus:
                continue
            bus.append(adder)
    bus=preserve(bus,rows)
    bus.sort()
    temp_bus=[bus[dup] for dup in range(1,len(bus)) if not(bus[dup]==bus[dup-1])]
    #print bus
    print len(temp_bus)
            
bus.sort()
bus=[bus[dup] for dup in range(1,len(bus)) if not(bus[dup]==bus[dup-1])]
print(len(bus))
    
