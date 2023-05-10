import rclpy
from rclpy.node import Node

import numpy as np
from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from personal_interface.srv import StateChanger
from geometry_msgs.msg import Twist, TransformStamped

import time
import string
import asyncio
import os

class DesiredPosition(Node):
    def __init__(self):
        super().__init__("desired_position") 
        self.transform = Twist()

        self.state = "initiation"
        self.tf_buffer = Buffer(rclpy.duration.Duration(seconds=1.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.current_pose = Twist()

        self.srv_change_state = self.create_service(StateChanger, 'change_state', self.state_changer)

        self.desired_pose_sub = self.create_subscription(Twist,"desired_pose",self.trajectroy_pose,10)


        self.sub_vicon = self.create_subscription(TransformStamped,"update",self.updater,10)


        # hz = 1/30
        # self.create_timer(hz,self.desired_pose)


        self.get_logger().info("Desired Position is now running")
    
    def updater(self,msg):

        self.desired_pose()

        # asyncio.run(co)


    def desired_pose(self):

        if self.state == "follow_turtle":
            self.turtle_wait_frame()
        elif self.state == "follow_trajectory":
            self.current_pose
        elif self.state == "initiation":
            #wait for trajectory.
            try:
                pose = self.tf_buffer.lookup_transform("drone","world",rclpy.time.Time(),rclpy.time.Duration(seconds=0.1))
                self.current_pose.linear.x = pose.transform.translation.x
                self.current_pose.linear.y = pose.transform.translation.y
                self.current_pose.linear.z = pose.transform.translation.z
            except TransformException as ex:
                self.get_logger().info("No transform from drone to world")
                


            


        print("twist: {}".format(self.current_pose), end="\r")
        # self.get_logger().info("Desired Pose: {}".format(self.current_pose))

        



    def state_changer(self,request,response):
        
        self.state = request.state
        response.success = True

        return response



    def turtle_wait_frame(self):
        worldToTurtle = self.tf_buffer.lookup_transform("turtle","world",rclpy.time.Time(),rclpy.time.Duration(seconds=0.1))

        hover_distance = 0.5 # how fare the drone hover over the turtle in meters
        hover_frame = worldToTurtle
        hover_frame.transform.translation.z = hover_frame.transform.translation.z + hover_distance

        return hover_frame


    def trajectroy_pose(self,msg):
        self.current_pose = msg



    def service_for_desired_pose(self, request, response):


        response.pose.linear.x  = self.current_pose.linear.x
        response.pose.linear.y  = self.current_pose.linear.y
        response.pose.linear.z  = self.current_pose.linear.z
        response.pose.angular.z = self.current_pose.angular.z

        return response


    
def main(args=None):
    rclpy.init(args=args)

    node = DesiredPosition()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()
