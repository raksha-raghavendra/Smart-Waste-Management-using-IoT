'''from Tkinter import *
import tkFont'''
import RPi.GPIO as GPIO
import time
import serial
from firebase import firebase
import string
from lcd import *
import pynmea2

GPIO.setwarnings(False)
lcd_init()
lcd_byte(LCD_LINE_1, LCD_CMD)
lcd_string("SMART WASTE", 2)
lcd_byte(LCD_LINE_2, LCD_CMD)
lcd_string("MANAGEMENT", 2)
time.sleep(3)
GPIO.setmode(GPIO.BCM)
firebase= firebase.FirebaseApplication('https://swmiot-e9d0e.firebaseio.com/', None)
'''win= Tk()
win.title("SMART WASTE MANAGEMENT")
status= "START THE PROGRAM FIRST"
win.geometry("380x280")
myFont  = tkFont.Font(family= "Helvetica", size= 12, weight= "bold")
def textToggle1():
	textToggle(status)'''
def program1():
	global status
	port= '/dev/ttyAMA0'
	RAIN1= 24
	RAIN2= 17
	RAIN3= 27
	RAIN4= 22
	TRIG= 4
	ECHO=18
	LED= 23
	LED_EMPTY= 8	
	LED_HALF= 7	
	BUZZER= 25

	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(LED, GPIO.OUT)
	GPIO.setup(LED_EMPTY, GPIO.OUT)
	GPIO.setup(LED_HALF, GPIO.OUT)
	GPIO.setup(RAIN1, GPIO.IN)
	GPIO.setup(RAIN2, GPIO.IN)
	GPIO.setup(RAIN3, GPIO.IN)
	GPIO.setup(RAIN4, GPIO.IN)
	GPIO.setup(BUZZER, GPIO.OUT)
	flag=0
	num1=[]
	def get_digit(num):
		if num<10:
			num1.append(num)
		else:
			get_digit(num//10)
			num1.append(num%10)
		print(num1)
	while True:

		if flag==0:
			ser= serial.Serial(port, baudrate=9600, timeout= 0.5)
			data= ser.readline()
			data= data.split(',')
			if data[0]== 'GPGGA' or data[0]== '$GPRMC':
				data= ','.join(data)
				msg= pynmea2.parse(data)
				latval=msg.lat
				latval= str(latval)
				d= float(latval[:2])
				m= float(latval[3:])
				concatlat= d+ float(m)/60 
				print 'Latitude:{}'.format(concatlat)
				longval= msg.lon
				longval= str(longval)
				d2= float(longval[:3])
				m2= float(longval[3:])
				concatlong= d2+ float(m2)/60
				print 'Longitude: {}'.format(concatlong)
				time.sleep(1)
				flag=1
		if (GPIO.input(RAIN1)==0 or GPIO.input(RAIN2)==0 or GPIO.input(RAIN3)==0 or GPIO.input(RAIN4)==0):
			print 'Water Detected'
			time.sleep(3)
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)== False:
			start= time.time()
		while GPIO.input(ECHO)== True:
			end= time.time()
		sig_time= end-start
		distance= sig_time/0.000148
		print('Distance is: {}'.format(distance))
		GPIO.output(LED_EMPTY, GPIO.LOW)
		GPIO.output(LED, GPIO.LOW)
		GPIO.output(LED_HALF, GPIO.LOW)
		if distance <4:
			status= "FULL"
			print('FULL')
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string("FULL BIN", 2)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("", 2)
			if flag==1:

				firebase.post('user', {'lat': concatlat, 'long': concatlong, 'Status': 'Full'})
			time.sleep(0.0001)
			GPIO.output(BUZZER, GPIO.HIGH)
			GPIO.output(LED, GPIO.HIGH)
			time.sleep(3)
			GPIO.output(LED, GPIO.LOW)
			GPIO.output(BUZZER, GPIO.LOW)
		elif distance >4 and distance <8:
			status= "HALF"
			print('HALF')
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string("HALF BIN", 2)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("", 2)
			GPIO.output(LED_HALF, GPIO.HIGH)
			time.sleep(3)
			if flag==1:
				firebase.post('user', {'lat':concatlat, 'long':concatlong, 'Status': 'Half'})
			GPIO.output(LED_HALF, GPIO.LOW)
			time.sleep(0.0001)
		else:
			status= "EMPTY"
			print('EMPTY')
			lcd_byte(LCD_LINE_1, LCD_CMD)
			lcd_string("EMPTY BIN", 2)
			lcd_byte(LCD_LINE_2, LCD_CMD)
			lcd_string("", 2)
			GPIO.output(LED_EMPTY, GPIO.HIGH)
			if flag==1:
				firebase.post('user', {'lat':concatlat, 'long':concatlong, 'Status': 'Empty'})
			GPIO.output(LED_EMPTY, GPIO.LOW) 
			time.sleep(1)
	GPIO.output(LED, GPIO.LOW)
	GPIO.output(LED_HALF, GPIO.LOW)
	GPIO.output(LED_EMPTY, GPIO.LOW)
'''def textToggle(status):
	if status=="FULL":
                textButton["text"]= "FULL"
                textButton["bg"]= "RED"
        elif status== "HALF":
                textButton["text"]= "HALF"
                textButton["bg"]= "YELLOW"
        else:
                textButton["text"]= "EMPTY"
                textButton["bg"]= "GREEN"

textButton= Button(win, text= "CLICK HERE FOR STATUS", font= myFont, command= textToggle1, bg= "bisque2", height=1, width= 24)
textButton.grid(row=1, column=1)
programButton= Button(win, text= "START THE PROGRAM", font = myFont, command= program1, bg= "bisque2", height=1, width = 24)
programButton.grid(row=0, column= 1)'''

program1()
GPIO.cleanup()
'''mainloop()'''

