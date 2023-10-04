"""
before run this project, your computer must connected with arduino first 
if you don't have arduino, you can comment all 'serial' function on this project to run this project
without serial communication

"""

import numpy as np
import cv2
import serial
from serial import Serial
import imutils
import time

#set serial communication
arduino = serial.Serial('/dev/ttyACM0', 115200,timeout=0)  
arduino.flush()		

#variable for access camera			    
cap = cv2.VideoCapture(0)	#change number to 1 if you want to access external camera


# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = np.array([151, 49, 55 ])
greenUpper = np.array([153, 255, 255])




#set font on the window
fo = cv2.FONT_HERSHEY_DUPLEX
w = (200,200,0)


# keep looping
while True:

	ret,img = cap.read(0)
	img = imutils.resize(img, width=320)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y),radius) = cv2.minEnclosingCircle(c)

		if radius > 0:
			cv2.circle(mask, (int(x), int(y)), 5,(255, 0, 255), 2)
			cv2.putText(mask,"detected",(30,30),fo,1,w,2)
	
			if x < 100:
				cv2.putText(mask,"kanan",(30,60),fo,1,w,2)  #print on the window
				data = str("1")
				arduino.write(data.encode())
	
			if x >= 100 and x < 200:
				cv2.putText(mask,"tengah",(30,60),fo,1,w,2)  #print on the window
				data = str("2")
				arduino.write(data.encode())

	
			if x >= 200 and x < 320:
				cv2.putText(mask,"kiri",(30,60),fo,1,w,2)  #print on the window
				data = str("3")
				arduino.write(data.encode())

		else:
			data = str("0")
			arduino.write(data.encode())
			
	if len(cnts) == 0:
		ada_color = 0
		x = 0
		y = 0
		 

	fps = cap.get(cv2.CAP_PROP_FPS)
	afs = str("Fps {0}".format(fps))
	cv2.putText(img,afs,(10,10),fo,0.5,w)
	cv2.imshow("Frame", mask)
	cv2.imshow("img", img)
	print ("detect: %d %d" % (x, y))	
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

#Frame cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()


