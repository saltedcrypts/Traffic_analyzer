import urllib2,math
def mapping(st):
    mapp=0
    for i in range(0,len(st)):
        if(ord(st[i])<ord('a')):
            mapp=mapp+(ord(st[i])-ord('0')+26)*(36**i)
        else:
            mapp=mapp+(ord(st[i])-ord('a'))*(36**i)
    return math.log(mapp)

def street(x,y):
    response=urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f"%(x,y)).read()
    response=list(response)
    for i in range(len(response)):
        if(response[i:i+22]==list('"formatted_address" : ')):
           strt = response[i+23:i+47]
           while ' ' in strt:
               strt.remove(' ')
           print strt
           print mapping(strt)
           return mapping(strt)
    
street(40.714224,-73.961452)
