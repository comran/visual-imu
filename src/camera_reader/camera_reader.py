import cv2
import numpy as np
import rclpy
import time

from std_msgs.msg import String
import sensor_msgs.msg
from cv_bridge import CvBridge, CvBridgeError

class CameraReader:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        

def main(args=None):
    rclpy.init(args=args)

    node = rclpy.create_node('minimal_publisher')
    publisher = node.create_publisher(sensor_msgs.msg.Image, 'webcam', 100)
    bridge = CvBridge()

    vc = cv2.VideoCapture(0)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    last_time = time.time()
    while rval:
        rval, frame = vc.read()

        publisher.publish(bridge.cv2_to_imgmsg(frame))

        current_time = time.time()
        print(1.0 / (current_time - last_time))
        last_time = current_time

if __name__ == '__main__':
    main()
