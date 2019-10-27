import numpy as np
import cv2 as cv
import math
import time
import functools

FARNEBACK_PYRAMID_SCALE = 0.5
FARNEBACK_PYRAMID_LEVELS = 1
FARNEBACK_AVERAGE_WINDOW_SIZE = 15
FARNEBACK_PYRAMID_ITERATIONS_AT_LEVEL = 3
FARNEBACK_POLYNOMIAL_PIXEL_NEIGHBORHOOD = 5
FARNEBACK_POLYNOMIAL_SIGMA = 1.2
FARNEBACK_FLAGS = 0

class DenseOpticalFlow:
    def __init__(self):
        self.previous_bw_frame = None

    def find_divergence(self, vector_field):
        return np.mean(functools.reduce(np.add, np.gradient(vector_field)))

    def process(self, input_frame):
        scale = 0.5
        input_frame = cv.resize(input_frame,
            (int(input_frame.shape[1] * scale), int(input_frame.shape[0] * scale)),
            interpolation = cv.INTER_AREA)

        current_bw_frame = cv.cvtColor(input_frame, cv.COLOR_BGR2GRAY)

        if self.previous_bw_frame is None:
            self.previous_bw_frame = current_bw_frame
            return ((0, 0), 0)

        flow = cv.calcOpticalFlowFarneback(
            self.previous_bw_frame,
            current_bw_frame,
            None, # Computed flow image
            FARNEBACK_PYRAMID_SCALE,
            FARNEBACK_PYRAMID_LEVELS,
            FARNEBACK_AVERAGE_WINDOW_SIZE,
            FARNEBACK_PYRAMID_ITERATIONS_AT_LEVEL,
            FARNEBACK_POLYNOMIAL_PIXEL_NEIGHBORHOOD,
            FARNEBACK_POLYNOMIAL_SIGMA,
            FARNEBACK_FLAGS)

        flow_avg_x = np.mean(flow[..., 0])
        flow_avg_y = np.mean(flow[..., 1])

        self.previous_bw_frame = current_bw_frame

        divergence = self.find_divergence(flow)

        return ((flow_avg_x, flow_avg_y), divergence)
