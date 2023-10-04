import cv2
import numpy as np
#import serial
#from serial import serial
import imutils
import time


def nothing(x):
    pass

cap = cv2.VideoCapture(1)

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
    #frame = cv2.imread('smarties.png')
    ret,frame = cap.read()
    frame = imutils.resize(frame, width=320)
    blurred = cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")
    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    
    kernel = np.ones((5 ,5), "uint8")
    mask = cv2.inRange(hsv, l_b, u_b)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
#    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, frame.shape[0]/64, param1=200, param2=20, minRadius=1, maxRadius=320)
#    if circles is not None:
#        circles = np.uint16(np.around(circles))
#        for i in circles[0, :]:
#            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
#            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

#    kernel = np.ones((3, 3), np.uint8) 
#    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations = 2) 
#    bg = cv2.dilate(closing, kernel, iterations = 1) 
#    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0) 
#    ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0) 

#    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#    cnts = imutils.grab_contours(cnts)
#    center = None
    
#    if len(cnts) > 0:
#        c = max(cnts, key=cv2.contourArea)
#        ((x, y), radius) = cv2.minEnclosingCircle(c)
#        M = cv2.moments(c)
#        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
#        if radius > 0:
#            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#            cv2.circle(frame, center, 1, (0, 0, 255), -1)

#    if len(cnts) == 0:
#        x = 0
#        y = 0

#    print ("detect: %d %d" % (x, y))	
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
