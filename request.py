from sqlite3 import *
BusStop=[[1,2,3],[2,5,4,6],[2,6,8]]
BusPos=[]
Time=[[1 for i in range(10)] for j in range(10)]
x=[35,120,215,120,215,305,396,485,354,320,515,510,570]
y=[141,84,28,235,185,130,185,132,82,220,230,40,150]


def near(pos,ign=-1):
    ind=-1
    m=1000000000000
    for i in range(len(x)):
        if(m>((pos[0]-x[i])**2+(pos[1]-y[i])**2) and not(i==ign)):
            ind=i
            m=(pos[0]-x[i])**2+(pos[1]-y[i])**2
    return ind

def get(bus,stat):
    near1=near(BusPos[bus])
    near2=near(BusPos[bus],near1)
    time=0
    if BusStop[bus].index(near1) < BusStop[bus].index(near2):
        start=near1
    else:
        start=near2
    time=0
    while not(start==stat):
        cur=BusStop[bus][start]
        nxt=BusStop[bus][start+1]
        time=time+Time[cur][nxt]
        start=start+1
    return time
    
        
    
def request(stat1,stat2):
    possible=[]
    for i in range(len(BusStop)):
        if stat1 in BusStop[i] and stat2 in BusStop[i] and BusStop[i].index(stat1) < BusStop[i].index(stat2):
            possible.append(i)
    if len(possible)==0:
        return -1
    minTime=1000000000000
    ind=-1
    for i in possible:
        start=BusStop[i].index(stat1)
        stop=BusStop[i].index(stat2)
        time=0
        while not(start==stop):
            cur=BusStop[i][start]
            nxt=BusStop[i][start+1]
            time=time+Time[cur][nxt]
            start=start+1
        time=time+get(i,stat1)
        if time<minTime:
            minTime=time
            ind=i
    return i
con=connect('database/BusPos.db')
cur=con.cursor()
with con:
    while True:
        raw_input("Press any key ")
        cur.execute("SELECT * FROM BusPos")
        a=cur.fetchall()
        print a
        
    
