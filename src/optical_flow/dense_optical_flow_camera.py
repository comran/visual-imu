import numpy as np
import cv2 as cv
import argparse
import math
import time

def resize_res(frame, scale, invert=False):
    if invert:
        scale = scale

    return cv.resize(frame,
            (int(frame.shape[1] * scale), int(frame.shape[0] * scale)),
            interpolation = cv.INTER_AREA)

cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
frame1 = resize_res(frame1, 1.0 / 2)
prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
last_time = time.time()

#TODO: Create a plot of optical flow yz noise from algorithm
#TODO: Use weighted average for angle.
#TODO: Look into divergence/curl for x and roll 
#TODO: Contour detection research

while(1):
    ret, frame_original = cap.read()
    frame2 = resize_res(frame_original, 1.0 / 2)
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])

    flow_avg_x = np.mean(flow[...,0])
    flow_avg_y = np.mean(flow[...,1])
    avg_mag, avg_ang = cv.cartToPolar(np.array(flow_avg_x), np.array(flow_avg_y))
    # print((flow_avg_x, flow_avg_y))

    # avg_mag = np.mean(mag)
    # avg_ang = np.mean(ang)
    avg_ang_deg = avg_ang * 180 / np.pi
    print("magnitude: " + str(avg_mag) + " angle: " + str(avg_ang_deg))

    # Draw an arrow depicting the average optical flow.
    arrow_scale = 30
    arrow_x1 = frame_original.shape[1] / 2
    arrow_y1 = frame_original.shape[0] / 2
    arrow_x2 = int(arrow_x1 + arrow_scale * avg_mag * math.cos(avg_ang))
    arrow_y2 = int(arrow_y1 + arrow_scale * avg_mag * math.sin(avg_ang))
    cv.line(frame_original, (arrow_x1, arrow_y1), (arrow_x2, arrow_y2), (0,255,0), 3)

    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)

    # Show FPS
    current_time = time.time()
    diff = round(1.0 / (current_time - last_time))
    cv.putText(frame_original, str(diff), (10, 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=3)
    last_time = current_time
    
    cv.imshow('frame2', resize_res(bgr, 4.0 / 1, invert=True))
    cv.imshow('frame2_raw', resize_res(frame_original, 2))
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png',frame2)
        cv.imwrite('opticalhsv.png',bgr)
    prvs = next

