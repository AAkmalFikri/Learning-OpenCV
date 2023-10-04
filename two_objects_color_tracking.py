import numpy as np
import cv2
import imutils
import time
#import serial
#from serial import serial

def nothing(x):
	pass

cap = cv2.VideoCapture(0)

cv2.namedWindow("Calibration")
cv2.createTrackbar("Field LH", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Field UH", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Field LS", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Field US", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Field LV", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Field UV", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Ball LH", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball UH", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Ball LS", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball US", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Ball LV", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball UV", "Calibration", 255, 255, nothing)

while True:
	frame = cv2.imread('field.png')
#	ret,frame = cap.read()
	frame = imutils.resize(frame, width=320)
	blurred = cv2.GaussianBlur(frame,(11,11),0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	lh_f = cv2.getTrackbarPos("Field LH", "Calibration")
	uh_f = cv2.getTrackbarPos("Field UH", "Calibration")
	ls_f = cv2.getTrackbarPos("Field LS", "Calibration")
	us_f = cv2.getTrackbarPos("Field US", "Calibration")
	lv_f = cv2.getTrackbarPos("Field LV", "Calibration")
	uv_f = cv2.getTrackbarPos("Field UV", "Calibration")
	lh_b = cv2.getTrackbarPos("Ball LH", "Calibration")
	uh_b = cv2.getTrackbarPos("Ball UH", "Calibration")
	ls_b = cv2.getTrackbarPos("Ball LS", "Calibration")
	us_b = cv2.getTrackbarPos("Ball US", "Calibration")
	lv_b = cv2.getTrackbarPos("Ball LV", "Calibration")
	uv_b = cv2.getTrackbarPos("Ball UV", "Calibration")
	l_f = np.array([lh_f, ls_f, lv_f], np.uint8)
	u_f = np.array([uh_f, us_f, uv_f], np.uint8)	
	l_b = np.array([lh_b, ls_b, lv_b], np.uint8)
	u_b = np.array([uh_b, us_b, uv_b], np.uint8)
	
	field = cv2.inRange(hsv, l_f, u_f)
	ball = cv2.inRange(hsv, l_b, u_b)
	
	kernel = np.ones((5 ,5), "uint8")
	mask1 = cv2.erode(field, kernel, iterations=2)
	mask1 = cv2.dilate(field, kernel, iterations=2)
	mask2 = cv2.erode(ball, kernel, iterations=2)
	mask2 = cv2.dilate(ball, kernel, iterations=2)
	res1 = cv2.bitwise_and(frame, frame, mask=field)
	res2 = cv2.bitwise_and(frame, frame, mask=ball)
	cnts1,hierarchy = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(frame, cnts1, -1, (0, 255, 0), 3)
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts2 = imutils.grab_contours(cnts2)
	center = None
	
	if len(cnts2) > 0:
		c = max(cnts2, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 0:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 1, (0, 0, 255), -1)

	if len(cnts2) == 0:
		x = 0
		y = 0
		
#	try:
#		ball = [x, y]
#		i, j, k, _ = np.shape(cnts1)
#		cnts1_list = cnts1_rs.tolist()
#		ball in cnts1_list
#		if True:
#			print ("detect: %d %d" % (x, y))
#		if False:
#			x = 0
#			y = 0
#			print ("detect: %d %d" % (x, y))
#	except ValueError:
#		x = 0
#		y = 0
#		print ("detect: %d %d" % (x, y))				

#	print("res1"+ str(res1))
#	print("res2"+ str(res2))
#	print("mask1"+ str(mask1))
#	print("mask2"+ str(mask2))
#	print('cnts1' + str(cnts1))
#	print('cnts2' + str(cnts2))
		
#	print ("detect: %d %d" % (x, y))	
	res = cv2.add(res1,res2)
	cv2.imshow("frame", frame)
	cv2.imshow("mask feld", mask1)
	cv2.imshow("mask ball", mask2)
	cv2.imshow("res", res)

	key = cv2.waitKey(1)
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()

