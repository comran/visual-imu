import numpy as np
import cv2 as cv
import argparse
import math

def resize_res(frame, invert=False):
    scale = 0.25
    if invert:
        scale = 1 / scale

    return cv.resize(frame,
            (int(frame.shape[1] * scale), int(frame.shape[0] * scale)),
            interpolation = cv.INTER_AREA)

cap = cv.VideoCapture(0)
ret, frame1 = cap.read()
frame1 = resize_res(frame1)
prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
while(1):
    ret, frame_original = cap.read()
    frame2 = resize_res(frame_original)
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])

    avg_mag = max(0.0, np.mean(mag) - 0.2)
    avg_ang = np.mean(ang)
    avg_ang_deg = avg_ang * 180 / np.pi
    print("magnitude: " + str(avg_mag) + " angle: " + str(avg_ang_deg))

    arrow_scale = 30
    arrow_x1 = frame_original.shape[1] / 2
    arrow_y1 = frame_original.shape[0] / 2
    arrow_x2 = int(arrow_x1 + arrow_scale * avg_mag * math.cos(avg_ang))
    arrow_y2 = int(arrow_y1 + arrow_scale * avg_mag * math.sin(avg_ang))

    cv.line(frame_original, (arrow_x1, arrow_y1), (arrow_x2, arrow_y2), (0,255,0), 3)

    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    cv.imshow('frame2',resize_res(bgr, invert=True))
    cv.imshow('frame2_raw',frame_original)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png',frame2)
        cv.imwrite('opticalhsv.png',bgr)
    prvs = next

