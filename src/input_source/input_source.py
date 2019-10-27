import cv2 as cv

class InputSource:
    def __init__(self, path=None):
        if path is None:
            self.input = cv.VideoCapture(0)
        else:
            video_path = path + ".mp4"
            csv_path = path + ".csv"
            self.input = cv.VideoCapture(video_path)

    def fetch(self):
        ret, frame = self.input.read()
        return frame
