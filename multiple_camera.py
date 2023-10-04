import numpy as np
import cv2
import time
import imutils as im

def nothing(x):
	pass

cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(2)

while True:
	ret1,frame1 = cam1.read()
	ret2,frame2 = cam2.read()
	
	if (ret1):
#		frame1 = im.resize(frame1, width=320)
		cv2.imshow("frame1", frame1)
	if (ret2):
#		frame2 = im.resize(frame2, width=320)
		cv2.imshow("frame2", frame2)
	
#	frame1 = im.resize(frame1, width=320)
#	frame2 = im.resize(frame2, width=320)
	
#	cv2.imshow("frame1", frame1)
#	cv2.imshow("frame2", frame2)
	
	key = cv2.waitKey(1)
	if key == 27:
		break

cam1.release()
cam2.release()
cv2.destroyAllWindows()
