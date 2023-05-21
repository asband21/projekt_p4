import rclpy
from rclpy.node import Node

import numpy as np
from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from personal_interface.srv import StateChanger, Tf
from geometry_msgs.msg import Twist, TransformStamped

import time
import string
import asyncio
import os

class DesiredPosition(Node):
    def __init__(self):
        super().__init__("desired_position") 
        self.transform = Twist()

        # self.state = "initiation"
        self.state = "follow_turtle"
        
        self.desired_drone_pose = Twist()

        self.node_desired_position = rclpy.create_node("node_desired_position")

        self.srv_desrided_pose_state = self.create_service(StateChanger, 'desrided_pose_state', self.state_changer)
        self.cli_tf_vicon2turtle = self.node_desired_position.create_client(Tf,"vicon2turtle")
        self.cli_tf_vicon2drone = self.node_desired_position.create_client(Tf,"vicon2drone")

        self.desired_pose_sub = self.create_subscription(Twist,"desired_pose",self.trajectroy_pose,10)


        self.sub_vicon = self.create_subscription(TransformStamped,"update",self.updater,10)


        # hz = 1/30
        # self.create_timer(hz,self.desired_pose)


        self.get_logger().info("Desired Position is now running")
    
    def updater(self,msg):

        self.desired_pose()

        # asyncio.run(co)



    def vicon2drone_tf_request(self):
        while not self.cli_tf_vicon2drone.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("calculate_target_pose service not available, waiting again...")
        
        request = Tf.Request()
        future = self.cli_tf_vicon2drone.call_async(request)
        rclpy.spin_until_future_complete(self.node_desired_position, future)
        
        return future.result().tf



    def vicon2turtle_tf_request(self):
        while not self.cli_tf_vicon2turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("calculate_target_pose service not available, waiting again...")
        
        request = Tf.Request()
        future = self.cli_tf_vicon2turtle.call_async(request)
        rclpy.spin_until_future_complete(self.node_desired_position, future)
        
        return future.result().tf




    def desired_pose(self):

        if self.state == "follow_turtle":
            self.desired_drone_pose = self.turtle_wait_frame()
        elif self.state == "follow_trajectory":
            self.desired_drone_pose
        elif self.state == "initiation":
            #wait for trajectory.
            try:
                pose = self.vicon2drone_tf_request()
                self.desired_drone_pose.linear.x = pose.transform.translation.x
                self.desired_drone_pose.linear.y = pose.transform.translation.y
                self.desired_drone_pose.linear.z = pose.transform.translation.z
            except TransformException as ex:
                self.get_logger().info("No transform from drone to vicon")
                


            


        print("twist: {}".format(self.desired_drone_pose), end="\r")
        # self.get_logger().info("Desired Pose: {}".format(self.desired_drone_pose))

        



    def state_changer(self,request,response):
        
        self.state = request.state
        response.success = True

        return response



    def turtle_wait_frame(self):
        vicon2Turtle = self.vicon2turtle_tf_request()

        hover_distance = 0.5 # how fare the drone hover over the turtle in meters
        hover_frame = vicon2Turtle
        hover_frame.transform.translation.z = hover_frame.transform.translation.z + hover_distance

        return hover_frame


    def trajectroy_pose(self,msg):
        self.desired_drone_pose = msg



    def service_for_desired_pose(self, request, response):


        response.pose.linear.x  = self.desired_drone_pose.linear.x
        response.pose.linear.y  = self.desired_drone_pose.linear.y
        response.pose.linear.z  = self.desired_drone_pose.linear.z
        response.pose.angular.z = self.desired_drone_pose.angular.z

        return response


    
def main(args=None):
    rclpy.init(args=args)

    node = DesiredPosition()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()
