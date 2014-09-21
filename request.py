from kivy.uix.togglebutton import ToggleButton
from kivy.base import runTouchApp
from kivy.uix.button import Button
from request import *
dic={}
for i in range(12):
	dic['Bus Stop '+str(i+1)]=i

fin_choice=0

tb = ToggleButton(text = "Choose Bus Stop",group = 'misc' ,size_hint=(0.15,0.1),state = 'down', height=44, pos = (350,550))
 
for i in range (1,13):

	btn1 = ToggleButton(text='Bus Stop %d' % i, group='Initial',size_hint=(0.075,0.075), height=44, pos = (80,500-40*i))
	tb.add_widget(btn1)

for i in range (1,13):

	btn1 = ToggleButton(text='Bus Stop %d' % i, group='Final',size_hint=(0.075,0.075), height=44, pos = (600,500-40*i))
	tb.add_widget(btn1)

clicked = 0

def func(instance): 
	global clicked
	if clicked == 0:
		for child in tb.children:

			if child.state == 'down':
				if child.group == 'Initial':
					print "initial choice=",child.text
					request(dic[child.text],fin_choice)
				
				else:
					print "final choice=",child.text
					fin_choice=dic[child.text]
		#clicked = 1

mainbutton = Button(text='Enter', size_hint=(None, None), pos = (350,10))
tb.add_widget(mainbutton)

mainbutton.bind(on_release=func)


runTouchApp(tb)
