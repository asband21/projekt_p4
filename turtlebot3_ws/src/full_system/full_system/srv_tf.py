import rclpy
from rclpy.node import Node

from tf2_msgs.msg import TFMessage

from geometry_msgs.msg import TransformStamped
from personal_interface.srv import Tf

import tf_transformations as tf


class SrvTF(Node):
    def __init__(self):
        super().__init__('srv_tf')
        self.current_vicon2turtle = TransformStamped()
        self.current_vicon2drone = TransformStamped()

        self.sub_vicon2turtle = self.create_subscription(TFMessage, 'tf', self.callback_vicon2turtle, 10 )
        self.srv_vicon2turtle = self.create_service(Tf, 'vicon2turtle', self.vicon2turtle)

        self.sub_vicon2drone = self.create_subscription(TFMessage, 'tf', self.callback_vicon2drone, 10 )
        self.srv_vicon2drone = self.create_service(Tf, 'vicon2drone', self.vicon2drone)


    def callback_vicon2turtle(self, msg):
        source_frame_id = 'vicon'
        target_frame_id = 'turtle'
        for transform in msg.transforms:
            if (transform.header.frame_id == source_frame_id and transform.child_frame_id == target_frame_id):
                self.current_vicon2turtle = transform
                break

    def vicon2turtle(self, request, response):
        response.tf = self.current_vicon2turtle
        return response


    def callback_vicon2drone(self, msg):
        source_frame_id = 'vicon'
        target_frame_id = 'drone'
        for transform in msg.transforms:
            if (transform.header.frame_id == source_frame_id and transform.child_frame_id == target_frame_id):
                self.current_vicon2drone = transform
                break

    def vicon2drone(self, request, response):
        response.tf = self.current_vicon2drone
        return response



def main():
    rclpy.init()
    node = SrvTF()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
