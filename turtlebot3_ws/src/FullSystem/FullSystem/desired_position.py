import rclpy
from rclpy.node import Node

import numpy as np
from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from OwnSrvAndMsg import TargetPose, TakePicture, ContinuePath
from geometry_msgs.msg import Twist








class DesiredPosition(Node):
    def __init__(self):
        super().__init__("desired_position") 

        
        self.targetPose = self.create_service(TargetPose, 'change_state', self.FindAtoB)

        self.desired_pose_pub = self.create_publisher(Twist,"desired_pose")

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.get_logger().info("Desired Position is now running")



    def current_desired_pose(self, msg):
        self.current_desired_pose = msg