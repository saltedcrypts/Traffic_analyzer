from sqlite3 import *
import pygame,sys
from pygame.locals import *
from random import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
im = plt.imread('testmap.png')
implot = plt.imshow(im)
pt1=[0 for i in range(1000)]
pygame.init()
screen=pygame.display.set_mode((786,293),0,32)
background=pygame.image.load('testmap.png').convert()
dot=pygame.image.load('download.png').convert_alpha()
screen.blit(background,(0,0))
pygame.display.update()
for i in range(1000):
    pt1[i],=plt.plot(0,0,marker='o')
con=connect('database/DatabaseAlt.db')

cur=con.cursor()
with con:
    for i in range(0,500):
        cur.execute("SELECT * FROM Data WHERE ItterID=%d ORDER BY Id"%i)
        rows = cur.fetchall()
        print i
        
        screen.blit(background,(0,0))
        for j in range(len(rows)):
            #print j
            #pt1[j].set_data(rows[j][2]+random()*((-1)**j),rows[j][3]+random()*((-1)**j))
            screen.blit(dot,(rows[j][2]+random()*((-1)**j),rows[j][3]+random()*((-1)**j)))
        
        time.sleep(0.5)
        
        pygame.display.update()
                        
        
        #plt.pause(0.0000001)
            
