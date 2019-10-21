import numpy as np
import cv2 as cv
import math
import time

class DenseOpticalFlow:
    def __init__(self):
        self.previous_bw_frame = None

    def process(self, input_frame):
        current_bw_frame = cv.cvtColor(input_frame, cv.COLOR_BGR2GRAY)

        if self.previous_bw_frame is None:
            self.previous_bw_frame = current_bw_frame
            return (0, 0)

        flow = cv.calcOpticalFlowFarneback(
            self.previous_bw_frame,
            current_bw_frame,
            None,
            0.5,
            3,
            15,
            3,
            5,
            1.2,
            0)

        flow_avg_x = np.mean(flow[..., 0])
        flow_avg_y = np.mean(flow[..., 1])

        self.previous_bw_frame = current_bw_frame

        return (flow_avg_x, flow_avg_y)
