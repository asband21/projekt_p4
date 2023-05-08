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




class DesiredPosition(Node):
    def __init__(self):
        super().__init__("desired_position") 

        self.state = "initiation"
        self.tf_buffer = Buffer(rclpy.duration.Duration(seconds=1.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)
        
        self.current_pose = Twist()

        self.srv_change_state = self.create_service(StateChanger, 'change_state', self.state_changer)

        self.desired_pose_sub = self.create_subscription(Twist,"desired_pose",self.trajectroy_pose,10)


        self.sub_vicon = self.create_subscription(TransformStamped,"update",self.vicon_callback,10)


        # hz = 1/30
        # self.create_timer(hz,self.desired_pose)


        self.get_logger().info("Desired Position is now running")
        

    def vicon_callback(self,msg):
        self.desired_pose()


    def desired_pose(self):

        if self.state == "follow_turtle":
            self.turtle_wait_frame()
        elif self.state == "follow_trajectory":
            self.current_pose
        elif self.state == "initiation":
            #wait for trajectory.
            self.tf_buffer.lookup_transform_async("drone","world",self.get_clock().now())



        print(self.current_pose)



    def state_changer(self,request,reponse):
        
        self.state = request.state
        reponse.success = True

        return reponse



    def turtle_wait_frame(self):
        worldToTurtle = self.tf_buffer.lookup_transform_async("turtle","world",self.get_clock().now())

        hover_distance = 0.5 # how fare the drone hover over the turtle in meters
        hover_frame = worldToTurtle
        hover_frame.transform.position.z = hover_frame.transform.position.z + hover_distance

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

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
