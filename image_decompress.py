import rostopic
import rospy
import roslib
from cv_bridge import CvBridge
import cv2
import sys
import numpy as np
from std_msgs.msg import UInt8MultiArray
from compressor.msg import RGBEnc
from sensor_msgs.msg import Image

bridge = CvBridge()
pub1 = rospy.Publisher("/camera/rgb/image_raw", Image, queue_size=1000)
pub2 = rospy.Publisher("/camera/depth/image_raw", Image, queue_size=1000)

def image_callback(msg):
    encimg = msg.rgb_enc
    encimg = np.array([ord(c) for c in encimg.data], dtype=np.uint8).reshape(-1, 1)
    cv_image = cv2.imdecode(encimg, cv2.IMREAD_COLOR)
    rospy.loginfo("decompressed RGB image size: {}".format(cv_image.shape))
    image_message = bridge.cv2_to_imgmsg(cv_image, encoding="rgb8")
    image_message.header = msg.header
    pub1.publish(image_message)

def depth_callback(encimg):
    pub2.publish(encimg)

if __name__ == "__main__":
    rospy.init_node("image_decompress", anonymous=True)
    sub1 = rospy.Subscriber("/compress/rgb", RGBEnc, image_callback)
    sub2 = rospy.Subscriber("/compress/depth", Image, depth_callback)
    rospy.loginfo("Node has been started")
    rospy.spin()
