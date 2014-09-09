from sqlite3 import *
import sys
from random import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
im = plt.imread('testmap.png')
implot = plt.imshow(im)
pt=[0 for i in range(1000)]
for i in range(1000):
    pt[i],=plt.plot(0,0,marker='o')
con=connect('database/database.db')
cur=con.cursor()

for i in range(900):
    cur.execute("SELECT * FROM Data_%d ORDER BY Id"%i)
    rows = cur.fetchall()
    
    for j in range(len(rows)):
        pt[j].set_data(rows[j][1]+random()*((-1)**j),rows[j][2]+random()*((-1)**j))
    
    plt.pause(0.0000001)
        
