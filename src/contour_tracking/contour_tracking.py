import contour_tracking.thresholding as thresholding

import cv2 as cv
import numpy as np
import math

FARNEBACK_PYRAMID_SCALE = 0.5
FARNEBACK_PYRAMID_LEVELS = 1
FARNEBACK_AVERAGE_WINDOW_SIZE = 2
FARNEBACK_PYRAMID_ITERATIONS_AT_LEVEL = 3
FARNEBACK_POLYNOMIAL_PIXEL_NEIGHBORHOOD = 5
FARNEBACK_POLYNOMIAL_SIGMA = 1.2
FARNEBACK_FLAGS = 0

REAL_CONTOUR_WIDTH = 0.38 # in meters
REAL_CONTOUR_HEIGHT = 0.38 # in meters
CAMERA_FOCAL_LENGTH = 1

SHOW_THRESHOLDED_FRAME = False

class Contour:
    def __init__(self, contour, frame_dimensions):
        self.contour = contour
        
        bounding_rotated_rect = cv.minAreaRect(contour)
        bounding_box_points = cv.boxPoints(bounding_rotated_rect)
        self.bounding_rotated_rect_countour = np.int0(bounding_box_points)
        self.area = cv.contourArea(self.bounding_rotated_rect_countour)

        self.x, self.y, self.w, self.h = self.find_rotated_rect_dimens(bounding_box_points)

        target_plane_width = frame_dimensions[0] / self.w * REAL_CONTOUR_WIDTH
        target_plane_height = frame_dimensions[1] / self.h * REAL_CONTOUR_HEIGHT

        self.target_plane_dimens = (target_plane_width, target_plane_height)
        self.distance_from_camera = REAL_CONTOUR_WIDTH * CAMERA_FOCAL_LENGTH / self.w

    def find_rotated_rect_dimens(self, rect_points):
        x = int((rect_points[2][0] - rect_points[0][0]) / 2)
        y = int((rect_points[2][1] - rect_points[0][1]) / 2)

        w = int( \
            math.sqrt( \
                math.pow(rect_points[1][1] - rect_points[0][1], 2) + \
                math.pow(rect_points[1][0] - rect_points[0][0], 2)))

        if w < 1:
            w = 1

        h = int( \
            math.sqrt( \
                math.pow(rect_points[1][1] - rect_points[2][1], 2) + \
                math.pow(rect_points[1][0] - rect_points[2][0], 2)))

        if h < 1:
            h = 1

        return x, y, w, h

class ContourTracking:
    def __init__(self):
        self.contour_threshold = thresholding.Thresholding()
        cv.namedWindow("bounding_box_highlight_frame", cv.WINDOW_NORMAL)

        if SHOW_THRESHOLDED_FRAME:
            cv.namedWindow("thresholded_frame", cv.WINDOW_NORMAL)

        self.previous_bw_frame = None

    def process(self, input_frame):
        thresholded_frame = self.contour_threshold.process(input_frame)

        if SHOW_THRESHOLDED_FRAME:
            cv.imshow("thresholded_frame", thresholded_frame)

        bounding_box_highlight_frame = input_frame.copy()

        contours = self.process_contours(thresholded_frame, input_frame)


        target_distance = 0
        reject = False
        for contour in contours:
            if not reject:
                target_distance = contour.distance_from_camera * 640.315789474
                print("TARGET DISTANCE: " + str(target_distance))


            r = 0
            g = 0
            if reject is False:
                g = 255  # Good contour :)
            else:
                r = 255  # Bad contour :(

            box = contour.bounding_rotated_rect_countour
            cv.drawContours(bounding_box_highlight_frame, [box], 0, (0, g, r), 1)

            reject = True

        cv.imshow("bounding_box_highlight_frame", bounding_box_highlight_frame)

        flow_avg_x = 0
        flow_avg_y = 0

        return target_distance

    def process_contours(self, thresholded_frame, input_frame):
        _, contours, _ = cv.findContours( \
            thresholded_frame, \
            cv.RETR_EXTERNAL, \
            cv.CHAIN_APPROX_SIMPLE)

        frame_height, frame_width = thresholded_frame.shape[:2]
        frame_dimensions = (frame_width, frame_height)

        contour_objects = list()
        for contour in contours:
            contour_objects.append(Contour(contour, frame_dimensions))
            
        contour_objects.sort(key=lambda x: x.area, reverse=True)

        return contour_objects
