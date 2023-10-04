import numpy as np
import cv2
import time
import imutils

def nothing(x):
	pass

cap = cv2.VideoCapture(1)

cv2.namedWindow("Calibration")
cv2.createTrackbar("Ball LH", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball UH", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Ball LS", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball US", "Calibration", 255, 255, nothing)
cv2.createTrackbar("Ball LV", "Calibration", 0, 255, nothing)
cv2.createTrackbar("Ball UV", "Calibration", 255, 255, nothing)

def coba_awal():
	ret, frame = cap.read()
	frame = imutils.resize(frame, width=320)
	blurred = cv2.GaussianBlur(frame,(11,11),0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	blurr = cv2.medianBlur(gray, 5)
	edges = cv2.Canny(blurr, 50, 200)

	lh_b = cv2.getTrackbarPos("Ball LH", "Calibration")
	uh_b = cv2.getTrackbarPos("Ball UH", "Calibration")
	ls_b = cv2.getTrackbarPos("Ball LS", "Calibration")
	us_b = cv2.getTrackbarPos("Ball US", "Calibration")
	lv_b = cv2.getTrackbarPos("Ball LV", "Calibration")
	uv_b = cv2.getTrackbarPos("Ball UV", "Calibration")
	l_b = np.array([lh_b, ls_b, lv_b], np.uint8)
	u_b = np.array([uh_b, us_b, uv_b], np.uint8)
	ball = cv2.inRange(hsv, l_b, u_b)
	
	kernel = np.ones((5 ,5), "uint8")
	mask = cv2.inRange(hsv, l_b, u_b)
	mask = cv2.erode(mask, kernel, iterations=2)
	mask = cv2.dilate(mask, kernel, iterations=2)
	res = cv2.bitwise_and(frame, frame, mask=mask)

	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, frame.shape[0]/64, param1=100, param2=15, minRadius=1, maxRadius=320)
#	if circles is not None:
#		circles = np.uint16(np.around(circles))
#		for i in circles[0, :]:
#			cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
#			cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		for (x, y, r) in circles:
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			print ("detect: %d %d" % (x, y))	
			
	cv2.imshow("Frame", frame)
	cv2.imshow("Canny", edges)
	cv2.imshow("Gray", blurr)
#	cv2.imshow("Mask", mask)
#	cv2.imshow("Res", res)

def coba_kedua():
	ret, frame = cap.read()
	frame = imutils.resize(frame, width=320)
	blurred = cv2.GaussianBlur(frame,(11,11),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	lh_b = cv2.getTrackbarPos("Ball LH", "Calibration")
	uh_b = cv2.getTrackbarPos("Ball UH", "Calibration")
	ls_b = cv2.getTrackbarPos("Ball LS", "Calibration")
	us_b = cv2.getTrackbarPos("Ball US", "Calibration")
	lv_b = cv2.getTrackbarPos("Ball LV", "Calibration")
	uv_b = cv2.getTrackbarPos("Ball UV", "Calibration")
	l_b = np.array([lh_b, ls_b, lv_b], np.uint8)
	u_b = np.array([uh_b, us_b, uv_b], np.uint8)
	mask = cv2.inRange(hsv, l_b, u_b)
	kernel = np.ones((5 ,5), "uint8")
	mask = cv2.inRange(hsv, l_b, u_b)
	mask = cv2.erode(mask, kernel, iterations=2)
	mask = cv2.dilate(mask, kernel, iterations=2)
	mask1 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
	mask1 = cv2.Canny(mask1, 100, 300)
	mask1 = cv2.GaussianBlur(mask1, (1, 1), 0)
	mask1 = cv2.Canny(mask1, 100, 300)
	
	try:
		im2, cnts, hierarchy = cv2.findContours(mask1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5] # get largest five contour area
		rects = []
		for c in cnts:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			x, y, w, h = cv2.boundingRect(approx)
			if h >= 15:
				rect = (x, y, w, h)
				rects.append(rect)
				cv2.rectangle(roi_copy, (x, y), (x+w, y+h), (0, 255, 0), 1);
			print ("detect: %d %d" % (x, y))
			
	except ValueError:
		print("None")
	
	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)
	cv2.imshow("Mask1", mask1)

def coba_ketiga():
	ret, frame = cap.read()
	frame = imutils.resize(frame, width=320)
	blurred = cv2.GaussianBlur(frame,(11,11),0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	lh_b = cv2.getTrackbarPos("Ball LH", "Calibration")
	uh_b = cv2.getTrackbarPos("Ball UH", "Calibration")
	ls_b = cv2.getTrackbarPos("Ball LS", "Calibration")
	us_b = cv2.getTrackbarPos("Ball US", "Calibration")
	lv_b = cv2.getTrackbarPos("Ball LV", "Calibration")
	uv_b = cv2.getTrackbarPos("Ball UV", "Calibration")
	l_b = np.array([lh_b, ls_b, lv_b], np.uint8)
	u_b = np.array([uh_b, us_b, uv_b], np.uint8)
	mask = cv2.inRange(hsv, l_b, u_b)
	kernel = np.ones((5 ,5), "uint8")
	mask = cv2.inRange(hsv, l_b, u_b)
	mask = cv2.erode(mask, kernel, iterations=2)
	mask = cv2.dilate(mask, kernel, iterations=2)
	mask1 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
	mask1 = cv2.Canny(mask1, 100, 300)
	mask1 = cv2.GaussianBlur(mask1, (1, 1), 0)
	mask1 = cv2.Canny(mask1, 100, 300)
	res = cv2.bitwise_and(frame, frame, mask=mask1)

	circles = cv2.HoughCircles(mask1, cv2.HOUGH_GRADIENT, 1, frame.shape[0]/64, param1=300, param2=30, minRadius=0, maxRadius=320)
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		for (x, y, r) in circles:
			cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			print ("detect: %d %d" % (x, y))
	
	cv2.imshow("Frame", frame)
	cv2.imshow("Mask", mask)
	cv2.imshow("Mask1", mask1)
	cv2.imshow("Res", res)
	

while True:
#	coba_awal()
#	coba_kedua()
	coba_ketiga()
	key = cv2.waitKey(1)
	if key == 27:
		break

		
cap.release()
cv2.destroyAllWindows()
