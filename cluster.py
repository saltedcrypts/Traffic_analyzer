from sqlite3 import *
#import matplotlib.pyplot as plt
import sys
from random import *
#import matplotlib.animation as animation
global git
import pygame,sys
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((786,293),0,32)
background=pygame.image.load('testmap.png').convert()
dot=pygame.image.load('icons/download.png').convert_alpha()
BusPoint=pygame.image.load('icons/bus.png').convert_alpha()
RealBusPoint=pygame.image.load('icons/rect.png').convert_alpha()
screen.blit(background,(0,0))
git=0
#im = plt.imread('testmap.png')
#implot = plt.imshow(im)
con1=connect('database/BusRoute.db')
con2=connect('database/BusPos.db')      
bus_pointer=0
con=connect('database/DatabaseAlt_new.db')
conn=connect('database/Bus_new.db')
cur=con.cursor()
cur1=con1.cursor()
cur2=con2.cursor()
pos=[[-1,-1] for i in range(1500)]
stationx=[35,120,215,120,215,305,396,485,621,759,354,320]
stationy=[141,84,28,235,185,130,185,132,184,78,82,220]
bus=[]
bstp=[0 for i in range(100)]
new_bus=0
rows=[]
x=[35,120,215,120,215,305,396,485,354,320,515,510,570]
y=[141,84,28,235,185,130,185,132,82,220,230,40,150]

stop_icons=["one.png","two.png","three.png","four.jpg","five.png","six.jpg","seven.png","eight.png","nine.jpg","ten.jpg","eleven.png","twelve.png"]
st_icons=[pygame.image.load("images/"+i).convert() for i in stop_icons]
avg_wait_time=[[0 for i in range(1500)] for j in range(len(x))]
bus_freq=[0 for i in range(len(x))]
timer=[0 for i in range(100)]
##################################################################################################################################################
Rrtx=[[] for i in range(100)]
Rrty=[[] for i in range(100)]

with conn:
    curr=conn.cursor()
    curr.execute("SELECT * FROM Bus ORDER BY id,Itter")
    
    Rbus=curr.fetchall()
    for i in Rbus:
        Rrtx[i[0]].append(i[2])
        Rrty[i[0]].append(i[3])
Rrtx=[i for i in Rrtx if not(i==[])]
Rrty=[i for i in Rrty if not(i==[])]
    
##################################################################################################################################################

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

def check_sub(l1,l2):
    for iter_l1 in l1:
        if(iter_l1 not in l2):
            return 1
    return 0

def sub_exists(l1,bs):
    for i_bs in bs:
        if check_sub(l1,i_bs[0])==0:
            return 0
    return 1

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
    for i in a:
        #print i[0],':',i[3],
        pass
    #print ''
    adj_list=[[] for j in range(len(a))]
    for i in a:
        for j in a:
            if i==j:
                continue
            if dist([i[1],i[2]],[j[1],j[2]])<7 and i[4]==j[4] and abs(i[3]-j[3])<10:
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

def median_sp(a):
    if(len(a))==0:
        return 0
    a.sort(key=SortKey)
    return a[len(a)/2][3]

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
        if avg(tmp[:])<20 or not(near(avgcoord_row_list(tmp))==-1):
            if timer[i[1]]<8:
                timer[i[1]]=timer[i[1]]+1
                unchanged.append(bus.index(i))
                continue    
        timer[i[1]]=0   
        #print tmp
        t=cluster(tmp[:])
        if(len(t)==1):
            buss.append([t[0],i[1]])
        elif(len(t)>1):
            t.sort(key=len)
            t.reverse()
            buss.append([t[0],i[1]])
            '''for p in t[1:]:
                buss.append([p,git])
                git=git+1'''
        else:
            #buss.append(i)
            pass
    for i in unchanged:
        buss.append(bus[i])
    return buss
'''    
pt1=[0 for i in range(1000)]
for i in range(1000):
    pt1[i],=plt.plot(0,0,marker='o')
pt=[0 for i in range(0,1000)]
for i in range(1000):
    pt[i],=plt.plot(0,0,marker='*')'''
##############################################################################################################################################################

cur1.execute("DROP TABLE IF EXISTS WaitTime")
cur1.execute("DROP TABLE IF EXISTS BusFreq")

cur1.execute("CREATE TABLE WaitTime(ItId INT,StatId INT, Wait FLOAT)")
cur1.execute("CREATE TABLE BusFreq(ItId INT,StatId INT, Freq INT)")

cur2.execute("DROP TABLE IF EXISTS BusPos")
cur1.execute("DROP TABLE IF EXISTS BusRoute")

cur2.execute("CREATE TABLE BusPos(Id INT, posx FLOAT, posy FLOAT)")
cur1.execute("CREATE TABLE BusRoute(Id INT, Route TEXT)")

test=[0 for i in range(50)]
#############################################################################################################################################################
with con,con1,con2:
    for i in range(50):
        cur2.execute("INSERT INTO BusPos VALUES(%d,%f,%f)"%(i,-1,-1))
        cur1.execute('INSERT INTO BusRoute VALUES(%d,"%s")'%(i,''))
    for i in range(1,1000):
        if(i%100==0):
            for itr in range(len(x)):
                ppl_count=0
                tot_val=0
                for jtr in range(len(avg_wait_time[itr])):
                    if(not(avg_wait_time[itr][jtr]==0)):
                        ppl_count+=1
                        tot_val+=avg_wait_time[itr][jtr]
                        avg_wait_time[itr][jtr]=0
                if (ppl_count==0):
                    ppl_count=1

                #WRITE IN DATABSE -- i, itr ,tot_val/ppl_count
                cur1.execute('INSERT INTO WaitTime VALUES(%d,%d,%f)'%(i,itr,(tot_val/ppl_count)))
            for itr in range(len(x)):
                #WRITE IN DATABASE bus_freq[itr]
                cur1.execute('INSERT INTO BusFreq VALUES(%d,%d,%d)'%(i,itr,(bus_freq[itr])))
                bus_freq[itr]=0

        cur.execute("SELECT * FROM Data WHERE ItterID=%d ORDER BY Id"%i)
        rows = cur.fetchall()
        rows=[j[1:] for j in rows]
        rows.sort()
        #for j in range(len(rows)):
            #pt1[j].set_data(rows[j][1]+random()*((-1)**j),rows[j][2]+random()*((-1)**j))
       
        for j in rows:
            pos[j[0]]=[j[1],j[2]]
            
        for j in range(len(bus)):
            tm=[rows[k] for k in bus[j][0]]
        for j in range(len(stationx)):
            tem=[]
            for k in rows:
                if(dist([stationx[j],stationy[j]],pos[k[0]])<20):
                    #print k[0],j
                    if(k[3]<21):
                        avg_wait_time[j][k[0]]+=1
                    tem.append(k)
            NewBus=cluster(tem[:])
            #print NewBus
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
                if(sub_exists(adder,bus)==0):
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
            if not(bstop==-1 ):
                if not(bstop in route[temp_bus[j][1]]):
                    route[temp_bus[j][1]].append(bstop)
                bus_freq[bstop]+=1

        bus=temp_bus        
        #plt.pause(0.0001)
        for srt_i in range(len(bus)):
            bus[srt_i][0].sort()
        for iter_prnt in bus:
            print iter_prnt[0],rows[iter_prnt[0][0]][3] # Print the ID of points belonging to the bus  
            #print route[iter_prnt[1]],near(avgcoord(iter_prnt[0],pos))
            pass
        cbus=[avgcoord(k[0],pos) for k in bus]
        screen.blit(background,(0,0))
        for j in range(len(st_icons)):
            screen.blit(st_icons[j],(x[j]-20,y[j]-20))

        for j in range(len(rows)):
            #print j
            #pt1[j].set_data(rows[j][2]+random()*((-1)**j),rows[j][3]+random()*((-1)**j))
            screen.blit(dot,(rows[j][1]+5*random()*((-1)**j),rows[j][2]+5*random()*((-1)**j)))
        for j in range(len(Rrtx)):
            screen.blit(RealBusPoint,(Rrtx[j][i%len(Rrtx[j])]-6,Rrty[j][i%len(Rrtx[j])]-6))
        print i,' -> ',len(cbus)  #Prints the iteration number and the number of busses 
        for k in bus:
            print len(k[0]),k[1]
            #print k[1],k[0]
            
        for k in range(len(cbus)):
            screen.blit(BusPoint,(cbus[k][0],cbus[k][1]))
            cur2.execute("UPDATE BusPos SET posx=%f , posy=%f WHERE Id=%d"%(cbus[k][0],cbus[k][1],bus[k][1]))
            cur1.execute('UPDATE  BusRoute SET Route="%s" WHERE Id=%d'%(str(route[bus[k][1]]),bus[k][1]))
            #pt[k].set_data(cbus[k][0],cbus[k][1])
        
        
        
           
        time.sleep(0.1)
        pygame.display.update()   
        #plt.pause(0.001)
        con1.commit()
        con2.commit()
        con.commit()
        #print "1"
        #raw_input()
        print ''
        print ''

        
    bus.sort()
    bus=[bus[0]]+[bus[dup] for dup in range(1,len(bus)) if not(bus[dup]==bus[dup-1])]

    print(len(bus))
    for iterat in route[:len(bus)]:
        print iterat    
    for iterat in route[:10]:
        for j in range(1,len(iterat)):
            #pt[j].set_data(x[i[j]],y[i[j]])
        #plt.pause(10d
            pass
pygame.quit()
sys.exit()
