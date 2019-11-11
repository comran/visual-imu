import cv2 as cv
import numpy as np

class Thresholding:
    def __init__(self):
        pass

    def process(self, input_frame):
        lower = np.array([0, 55, 0])
        upper = np.array([30, 255, 30])

        thresholded_frame = input_frame.copy()
        mask = cv.inRange(thresholded_frame, lower, upper)
        thresholded_frame = cv.cvtColor(thresholded_frame, cv.COLOR_BGR2GRAY)
        thresholded_frame = cv.bitwise_and(thresholded_frame, mask)
        thresholded_frame = cv.bitwise_not(thresholded_frame)
        thresholded_frame = cv.GaussianBlur(thresholded_frame, (15, 15), 5)
        thresholded_frame = cv.adaptiveThreshold(thresholded_frame, 255,
                 cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 1)

        return thresholded_frame
