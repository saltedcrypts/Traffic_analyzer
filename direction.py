import math
from random import *

def get_dir(i1,j1,i2,j2):
	magnitude=math.sqrt((i1-i2)**2+(j1-j2)**2)
	if magnitude==0:
                return (math.ceil(4*random()))
	if (math.acos( ((j2-j1)*(-1))/magnitude ) <= math.pi/4):
		return 1
	if (math.acos( ((j2-j1)*(1))/magnitude ) <= math.pi/4):
		return 3
	if (math.acos( ((i2-i1)*(1))/magnitude ) <= math.pi/4):
		return 2
	if (math.acos( ((i2-i1)*(-1))/magnitude ) <= math.pi/4):
		return 4
	print 'fall'
