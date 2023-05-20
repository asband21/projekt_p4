import math
import tf2_msgs 

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    
    gamel_tf = 0

    def __init__(self):
        super().__init__('oel')
        self.subscription = self.create_subscription(tf2_msgs.msg.TFMessage, 'tf', self.on_timer,10)

        # Declare and acquire `target_frame` parameter
        self.target_frame = self.declare_parameter('vicon', 'Drone').get_parameter_value().string_value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info("fldfldlf")

    def on_timer(self, dd):
        if gamel_tf == 0:
            gamel_tf = self.target_frame
            return
        self.get_logger().info("x:" + str(ptinfgamel_tf.translation.x))

        from_frame_rel = self.target_frame
        #self.get_logger().info(str(dd))
        #self.get_logger().info(f"llll{str(from_frame_rel)}")

def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
