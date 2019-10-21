import contour_tracking.thresholding as thresholding

class ContourTracking:
    def __init__(self):
        self.contour_threshold = thresholding.Thresholding()
        pass

    def process(self, input_frame):
        thresholded_frame = self.contour_threshold.process(input_frame)
