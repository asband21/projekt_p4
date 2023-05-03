import math
import copy
import tf2_msgs 

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    
    def quat2yor (self,x,y,z,w):
        return math.atan2(w*w + x*x - y*y - z*z , 2.0*(x*y + w*z))
 

    def __init__(self):
        super().__init__('oel')
        self.subscription = self.create_subscription(tf2_msgs.msg.TFMessage, 'tf', self.on_timer,10)

        # Declare and acquire `target_frame` parameter
        self.target_frame = self.declare_parameter('vicon', 'Drone').get_parameter_value().string_value

        self.gammel_tf = 0

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info("fldfldlf")

    def on_timer(self, dd):

        if self.gammel_tf == 0:
            self.gammel_tf = copy.deepcopy(dd)
            #dd.transform.translation.x = dd.transform.translation.x+2
            for tra in self.gammel_tf.transforms:
                if(tra.child_frame_id == "Drone" or tra.child_frame_id == "drone"):
                    tra.transform.translation.x = tra.transform.translation.x + 1
            return 

        vec = [0,0,0,0,0,0,0,0]
        del_tid = 0
        for tra in dd.transforms:
            if(tra.child_frame_id == "Drone" or tra.child_frame_id == "drone" ):
                #self.get_logger().info("x:" + str(tra.transform.translation.x))
                vec[0] = tra.transform.translation.x
                vec[1] = tra.transform.translation.y
                vec[2] = tra.transform.translation.z
                vec[3] = self.quat2yor(tra.transform.rotation.x, tra.transform.rotation.y, tra.transform.rotation.z, tra.transform.rotation.w)
                del_tid = tra.header.stamp

        for tra in self.gammel_tf.transforms:
            if(tra.child_frame_id == "Drone" or tra.child_frame_id == "drone" ):
                #self.get_logger().info("x:" + str(tra.transform.translation.x))
                if(del_tid.sec-tra.header.stamp.sec != 0):
                    del_tid =  del_tid.nanosec - tra.header.stamp.nanosec +1000000000
                else:
                    del_tid =  del_tid.nanosec - tra.header.stamp.nanosec
                vec[4] = (vec[0] - tra.transform.translation.x)/(del_tid/1000000000)
                vec[5] = (vec[1] - tra.transform.translation.y)/(del_tid/1000000000)
                vec[6] = (vec[2] - tra.transform.translation.z)/(del_tid/1000000000)
                vec[7] = (vec[4] - self.quat2yor(tra.transform.rotation.x, tra.transform.rotation.y, tra.transform.rotation.z, tra.transform.rotation.w))/(del_tid/1000000000)

        
        self.get_logger().info("vec:" + str(vec))
        #self.get_logger().info("delta tid:" + str(del_tid))    
        #self.get_logger().info("x:" + str(self.gammel_tf.msg.transform.translation.x))
        #from_frame_rel = self.target_frame
        """
        self.get_logger().info("--------------------------------")
        self.get_logger().info(str(dd.transforms[0].child_frame_id))
        self.get_logger().info(str(dd.transforms[0].header.stamp))
        self.get_logger().info("x:" + str(dd.transforms[0].transform.translation.x))
        self.get_logger().info("y:" + str(dd.transforms[0].transform.translation.y))
        self.get_logger().info("z:" + str(dd.transforms[0].transform.translation.z))
        """
        #self.get_logger().info(f"llll{str(from_frame_rel)}")
        self.gammel_tf = copy.deepcopy(dd)

def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()