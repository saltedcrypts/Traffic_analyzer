from sqlite3 import *
import matplotlib.pyplot as plt
import sys
from random import *
import matplotlib.animation as animation
global git
git=0
im = plt.imread('testmap.png')
implot = plt.imshow(im)
pt=[0 for i in range(1000)]
bus_pointer=0
con=connect('database/database.db')
cur=con.cursor()
pos=[[-1,-1] for i in range(1000)]
stationx=[35,120,215,120,215,305,396,485,621,759,354,320]
stationy=[141,84,28,235,185,130,185,132,184,78,82,220]
bus=[]
bstp=[0 for i in range(100)]
new_bus=0
rows=[]
x=[35,120,215,120,215,305,396,485,621,759,354,320]
y=[141,84,28,235,185,130,185,132,184,78,82,220]
pt=[0 for i in range(0,1000)]
for i in range(1000):
    tem=[0,0]
    pt[i],=plt.plot(tem[0],tem[1],marker='o')
route=[[-1] for i in range(1000)]
def avgcoord_row_list(pos):
    x=0
    y=0
    for i in pos:
        x=i[0]+x
        y=y+i[1]
    l=len(pos)
    return (x/l,y/l)

def avgcoord(lis,pos):
    x=0
    y=0
    for i in lis:
        x=pos[i][0]+x
        y=y+pos[i][1]
    l=len(lis)
    return (x/l,y/l)
def dist(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def near(pos):
    ind=-1
    m=1000000000000
    for i in range(len(x)):
        if(m>((pos[0]-x[i])**2+(pos[1]-y[i])**2)):
            ind=i
            m=(pos[0]-x[i])**2+(pos[1]-y[i])**2
    if(dist(pos,[x[ind],y[ind]])<30):
        return ind
    else:
        return -1

def SortKey(a):
    return a[3]
def SetDiff(a,b):
    a.sort()
    b.sort()
    thres=0.2
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
            if (speed>30):
                return 40
    return speed


def preserve(bus,rows):
    global git
    tem=[]
    unchanged=[]
    changed=[]
    new=[]
    buss=[]
    for i in bus:
        tmp=[]
        for j in i[0]:
            tmp.append(rows[j])
        if max_sp(tmp)<30 or not(near(avgcoord_row_list(tmp))==-1):
            unchanged.append(bus.index(i))
            continue
        #print tmp
        t=cluster(tmp)
        if(len(t)==1):
            buss.append([t[0],i[1]])
        elif(len(t)>1):
            t.sort(key=len)
            t.reverse()
            buss.append([t[0],i[1]])
            for p in t[1:]:
                buss.append([p,git])
                git=git+1
        else:
            #buss.append(i)
            pass
    for i in unchanged:
        buss.append(bus[i])
    return buss
    

for i in range(950):
    #print i
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
        rep=[]
        ne=[]
        rm=[]
        for k in NewBus:
            for l in bus:
                if l==[] or k==[]:
                    continue
                
                if SetDiff(l[0],k) == 1:
                    #print l,k
                    if k in rem:
                        continue
                    rep.append(bus.index(l))
                    rem.append([k,l[1]])
                    rm.append(k)
                    break
        
        for k in range(len(rem)):
            bus[rep[k]]=rem[k]
        for k in range(len(rem)):
            NewBus.remove(rm[k])
        for adder in NewBus:
            if adder in bus:
                continue
            bus.append([adder,git])
            git=git+1
    bus=preserve(bus,rows)
    bus.sort()
    temp_bus=[bus[0]]+[bus[dup] for dup in range(1,len(bus)) if not(bus[dup]==bus[dup-1])]
    
    for j in range(len(temp_bus)):
        coord=avgcoord(temp_bus[j][0],pos)
        #print coord
        #pt[j].set_data(coord[0],coord[1])
        tm=[rows[k] for k in temp_bus[j][0]]
        if(avg(tm)>30):
            continue
        bstop=near([coord[0],coord[1]])
        if bstop==4 and temp_bus[j][1]==1:
            print '-> ',bstop,temp_bus[j][1],i,rows[temp_bus[j][0][0]][4]
        if not(bstop==-1 ) and not(bstop in route[temp_bus[j][1]][-4:]):
            route[temp_bus[j][1]].append(bstop)
    bus=temp_bus        
'''    #plt.pause(0.0001)
    for srt_i in range(len(bus)):
        bus[srt_i][0].sort()
    for iter_prnt in bus:
        print iter_prnt,rows[iter_prnt[0][0]][3]
        #print route[iter_prnt[1]],near(avgcoord(iter_prnt[0],pos))
    #temp_input=raw_input()
    #print len(temp_bus)'''
    
bus.sort()
bus=[bus[0]]+[bus[dup] for dup in range(1,len(bus)) if not(bus[dup]==bus[dup-1])]

print(len(bus))
for i in route[:len(bus)]:
    print i    
for i in route[:10]:
    for j in range(1,len(i)):
        #pt[j].set_data(x[i[j]],y[i[j]])
    #plt.pause(10)
        pass
