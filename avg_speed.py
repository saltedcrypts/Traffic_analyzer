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
screen.blit(background,(0,0))
pygame.display.update()
con=connect('database/BusRoute.db')
cur=con.cursor()
con1=connect('database/DatabaseAlt_new.db')
cur1=con1.cursor()
def avg(data,x,y):
    av=[]
    t=0
    for i in data:
        if(((x-i[0])**2+(y-i[1])**2)<25):
            av.append(i[2])
    s=sum(av)
    if s==0:
        return 0
    else:
        return float(s)/len(av)
        
with con,con1:
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==6:
                xi,yi=pygame.mouse.get_pos()
                screen.blit(background,(0,0))
                screen.blit(dot,(xi,yi))
                cur.execute("SELECT * FROM CURRENT")
                a=cur.fetchall()
                cur1.execute("SELECT posx,posy,speed FROM Data WHERE ItterID=%d ORDER BY Id"%a[0][1])
                data=cur1.fetchall()
                av=avg(data,xi,yi)
                
                myfont = pygame.font.SysFont(None, 15)
                label = myfont.render("%f"%av, 1, (0,0,0))
                textRect = label.get_rect()
                textRect.centerx = xi-10
                textRect.centery = yi-10
                pygame.draw.rect(screen, (255,0,0), (textRect.left-5, textRect.top - 5, textRect.width + 5, textRect.height + 5))
                screen.blit(label, textRect)
                print av
                pygame.display.update()
                print xi,yi
           
