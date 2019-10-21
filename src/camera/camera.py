import cv2 as cv

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0)

    def fetch(self):
        ret, frame = self.camera.read()
        return frame
