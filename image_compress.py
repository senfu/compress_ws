import rostopic
import rospy
import roslib
from cv_bridge import CvBridge
import cv2
from std_msgs.msg import UInt8MultiArray
from compressor.msg import RGBEnc
from sensor_msgs.msg import Image

bridge = CvBridge()
pub1 = rospy.Publisher("/compress/rgb", RGBEnc, queue_size=1000)
pub2 = rospy.Publisher("/compress/depth", Image, queue_size=1000)

def image_callback(image_message):
    cv_image = bridge.imgmsg_to_cv2(image_message, desired_encoding="rgb8")
    src_len = cv_image.flatten().shape[0]
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
    _, encimg = cv2.imencode('.jpg', cv_image, encode_param)
    array = encimg.flatten().tolist()
    dest_len = len(array)
    uint8array = UInt8MultiArray(data=array)
    message = RGBEnc(rgb_enc=uint8array, header=image_message.header)
    pub1.publish(message)
    rospy.loginfo("RGB image compress rate {:.2f} [{}/{}]".format(float(dest_len) / float(src_len), dest_len, src_len))

def depth_callback(depth_message):
    pub2.publish(depth_message)

if __name__ == "__main__":
    rospy.init_node("image_compress", anonymous=True)
    sub1 = rospy.Subscriber("/camera/drop/fast/rgb/image_raw", Image, image_callback)
    sub2 = rospy.Subscriber("/camera/drop/fast/depth/image_raw", Image, depth_callback)
    rospy.loginfo("Node has been started")
    rospy.spin()
