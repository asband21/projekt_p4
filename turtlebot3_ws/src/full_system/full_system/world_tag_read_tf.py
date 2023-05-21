import rclpy
from rclpy.node import Node

from tf2_ros import TransformBroadcaster, TransformStamped

import os

import pickle

from std_msgs.msg import Header

import tf_transformations as tf

import numpy as np

import os
class TFPublisher(Node):

    def __init__(self):
        super().__init__('qr_tf_pub')
        
        self.tf_broadcaster = TransformBroadcaster(self)
        self.tf_msg = TransformStamped()
        self.tf_head = Header()

        self.create_timer(1, self.timer_callback)

        self.mode = "wolrd"

        # make sure the file exists, if not create it
        

        


    def timer_callback(self):
        try:
            if self.mode == "cal":
                with open("/home/ubuntu/tests/turtleTest/calibration_turtle2cam.pkl", 'rb') as f:
                    self.data = pickle.load(f)
            else:
                with open("/home/ubuntu/tests/turtleTest/world_targets.pkl", 'rb') as f:
                    self.data = pickle.load(f)
        except Exception as e:
            print(e)
            return

        ids,transforms = self.data

        # send tf for each qr code, so that the id matches the transform
        for i in range(len(ids)):
            self.tf_head.frame_id = "vicon"
            self.tf_head.stamp = self.get_clock().now().to_msg()
            self.tf_msg.header = self.tf_head
            self.tf_msg.child_frame_id = f"tag_{ids[i]}"
            transform = transforms[i]#.tolist()

            self.tf_msg.transform.translation.x = transform[0,3]
            self.tf_msg.transform.translation.y = transform[1,3]
            self.tf_msg.transform.translation.z = transform[2,3]


        
            quat = tf.quaternion_from_matrix(transform)

            self.tf_msg.transform.rotation.x = quat[0]
            self.tf_msg.transform.rotation.y = quat[1]
            self.tf_msg.transform.rotation.z = quat[2]
            self.tf_msg.transform.rotation.w = quat[3]


            self.tf_broadcaster.sendTransform(self.tf_msg)
            self.get_logger().info(f"Published tf for qr_{ids[i]}")
        # except Exception as e:
        #     print(e)
        #     pass



        




def main(args=None):
    rclpy.init(args=args)

    tf_pub = TFPublisher()

    rclpy.spin(tf_pub)

    tf_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()