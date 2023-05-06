import rostopic
import rospy
import roslib
from cv_bridge import CvBridge
import cv2
import sys
import numpy as np
from sensor_msgs.msg import Image, CameraInfo

WIDTH = 640
HEIGHT = 480
# K = (543.3278198242188, 0.0, 319.8379211425781, 0.0, 543.3278198242188, 238.32423400878906, 0.0, 0.0, 1.0)
K = (623.4906069676767, 0, 359.8902325676703, 0, 632.9580922290963, 256.31564384077, 0, 0, 1)
# R = (0.9999368786811829, -0.011222388595342636, 0.0005063230055384338, 0.011223847977817059, 0.999932587146759, -0.002976364456117153, -0.000472886924399063, 0.002981859492138028, 0.9999954700469971)
R = (1, 0, 0, 0, 1, 0, 0, 0, 1)
# P = (543.3278198242188, 0.0, 319.8379211425781, -24.796586990356445, 0.0, 543.3278198242188, 238.32423400878906, -0.3025660812854767, 0.0, 0.0, 1.0, -1.2722423076629639)
P = (662.204345703125, 0, 372.2213480131322, 0, 0, 683.232421875, 252.0754116159515, 0, 0, 0, 1, 0)
bridge = CvBridge()
pub1 = rospy.Publisher("/camera/rgb/image_raw", Image, queue_size=1000)
pub2 = rospy.Publisher("/camera/rgb/camera_info", CameraInfo, queue_size=1000)
pub3 = rospy.Publisher("/camera/depth/image_raw", Image, queue_size=1000)


def image_callback(msg):
    # cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
    # cv_image = cv2.resize(cv_image, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
    # image = bridge.cv2_to_imgmsg(cv_image, encoding="rgb8")
    # image.header = msg.header
    image = msg
    pub1.publish(image)


def camera_info_callback(msg):
    msg.width = WIDTH
    msg.height = HEIGHT
    msg.K = K
    msg.R = R
    msg.P = P
    pub2.publish(msg)


def depth_callback(msg):
    # cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="16UC1")
    # cv_image = cv2.resize(cv_image, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
    # image = bridge.cv2_to_imgmsg(cv_image, encoding="16UC1")
    # image.header = msg.header
    image = msg
    pub3.publish(image)


if __name__ == "__main__":
    rospy.init_node("image_resize", anonymous=True)
    sub1 = rospy.Subscriber("/camera/fast/rgb/image_raw", Image, image_callback)
    sub2 = rospy.Subscriber("/camera/fast/rgb/camera_info", CameraInfo, camera_info_callback)
    sub3 = rospy.Subscriber("/camera/fast/depth/image_raw", Image, depth_callback)
    rospy.loginfo("Node has been started")
    rospy.spin()
