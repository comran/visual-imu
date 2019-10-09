import cv2
import numpy as np
import rclpy
import time

from std_msgs.msg import String
import sensor_msgs.msg
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def callback(msg):
    frame = bridge.imgmsg_to_cv2(msg)
    print(frame)
    
    cv2.imshow("preview", frame)

def main(args=None):
    rclpy.init(args=args)

    cv2.namedWindow("preview")

    node = rclpy.create_node('minimal_subscriber')
    # publisher = node.create_publisher(String, 'webcam', 100)
    publisher = node.create_subscription(sensor_msgs.msg.Image, 'webcam', callback, 100)

    while rclpy.ok():
        rclpy.spin_once(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
