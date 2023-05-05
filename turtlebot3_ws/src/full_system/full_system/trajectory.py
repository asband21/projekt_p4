import rclpy
from rclpy.node import Node

import numpy as np

from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


import math


from personal_interface.srv import TargetPose, TakePicture, ContinuePath, DesiredPoseState

import time

import tf_transformations as tf



from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool



class Trajectory(Node):
    def __init__(self):
        super().__init__("trajectory") 
        self.sub_node_trajectory = rclpy.create_node("sub_cli_trajectory")

        self.sub_cli_drone = self.sub_node_trajectory.create_client(TakePicture,"take_picture")
        self.sub_cli_state = self.sub_node_trajectory.create_client(DesiredPoseState,"Position")
        
        self.srv_targetPose = self.create_service(TargetPose, 'go_to_target_pose', self.FindAtoB)
        self.srv_drone2turtle = self.create_service(SetBool, 'drone2turtle', self.service_drone2turtle)


        self.desired_pose_pub = self.create_publisher(Twist,"desired_pose")

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)




    def trajectory(self,t, pos_q0, pos_qf):


        G = np.zeros((4,4))
        B = np.zeros((4,1))
        x = np.zeros((4,1))


        t0 = t[0]
        tf = t[1]

        G[0, 0] = 1
        G[0, 1] = t0
        G[0, 2] = np.power(t0,2)
        G[0, 3] = np.power(t0,3)

        G[1, 0] = 0
        G[1, 1] = 1
        G[1, 2] = np.multiply(2,t0)
        G[1, 3] = np.multiply(3, np.power(t0,2))

        G[2, 0] = 1
        G[2, 1] = tf
        G[2, 2] = np.power(tf,2)
        G[2, 3] = np.power(tf,3)

        G[3, 0] = 0
        G[3, 1] = 1
        G[3, 2] = np.multiply(2,tf)
        G[3, 3] = np.multiply(3, np.power(tf,2))


        B[0, 0] = pos_q0
        B[1, 0] = 0
        B[2, 0] = pos_qf
        B[3, 0] = 0

        X_inv = np.linalg.inv(G)
        coefficients = X_inv.dot(B)

        return coefficients



    def AxisTrajectory(self, A, B):
        t = np.zeros((2,1))
        t[0] = 0
        t[1] = 1

        while True:
            axis = np.zeros((4,1))
            axis[0] = self.trajectory(t, A[0], B[0])
            axis[1] = self.trajectory(t, A[1], B[1])
            axis[2] = self.trajectory(t, A[2], B[2])
            axis[3] = self.trajectory(t, A[3], B[3])

            axis_max = np.zeros((4,1))
            axis_max[0]=-axis[0,2]/(2*axis[0,3])
            axis_max[1]=-axis[1,2]/(2*axis[1,3])
            axis_max[2]=-axis[2,2]/(2*axis[2,3])
            axis_max[3]=-axis[3,2]/(2*axis[3,3])

            if axis_max.any > 0.9:
                t[1] += 0.5
            else:
                break

        return t[1], axis # this is an array with the coefficents to the trajectories

    def desired_pose(self, dt, axis):

        pos_x = axis[0,0] + axis[0,1]*dt + axis[0,2]*np.power(dt,2) + axis[0,3]*np.power(dt,3)
        pos_y = axis[1,0] + axis[1,1]*dt + axis[1,2]*np.power(dt,2) + axis[1,3]*np.power(dt,3)
        pos_z = axis[2,0] + axis[2,1]*dt + axis[2,2]*np.power(dt,2) + axis[2,3]*np.power(dt,3)
        yaw_z = axis[3,0] + axis[3,1]*dt + axis[3,2]*np.power(dt,2) + axis[3,3]*np.power(dt,3)

        pose = np.zeros((4,1))
        pose[0] = pos_x
        pose[1] = pos_y
        pose[2] = pos_z
        pose[3] = yaw_z

        return pose # this is a 4 d array with the unit of meters for the first 3 elements and the last is radiens



    def oariantationDifference(self, q1, q2):
        
        q1.orientation.x
        q1.orientation.y
        q1.orientation.z
        q1.orientation.w

        start_rotation_M = tf.quaternion_matrix(q1[0],q1[1],q1[2],q1[3])

        q2.target_pose.pose.orientation.x
        q2.target_pose.pose.orientation.y
        q2.target_pose.pose.orientation.z
        q2.target_pose.pose.orientation.w

        end_rotation_M = tf.quaternion_matrix(q2[0],q2[1],q2[2],q2[3])

        start_y = [0,0]
        end_y   = [0,0]

        start_y[0] = start_rotation_M[0,1]
        start_y[1] = start_rotation_M[1,1]
        
        
        end_y[0] = end_rotation_M[1,1]
        end_y[1] = end_rotation_M[1,1]

        return math.atan2(end_y[1],end_y[0]) # returns the oriantation diff of the end y vector to the drones oriantation. THE UNIT IS RADIANS



    def send_request(self,request_to, request, respons):

        if request_to == "follow_trajectory":
            while not self.sub_cli_trajectory.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('service not available, waiting again...')
            req = DesiredPoseState.Request()

            req.state = "follow_trajectory"
            future = self.sub_cli_position.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_trajectory,future)
            return future.result()
        
        elif request_to == "follow_turtle":
            while not self.sub_cli_trajectory.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('service not available, waiting again...')
            req = DesiredPoseState.Request()

            req.state = "follow_turtle"
            future = self.sub_cli_position.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_trajectory,future)
            return future.result()
        



        


    def FindAtoB(self,request,response):
        telloTransform = self.tf_buffer.lookup_transform('tello','world')
        
        x_drone = telloTransform.transform.translation.x 
        y_drone = telloTransform.transform.translation.y
        z_drone = telloTransform.transform.translation.z
        yaw_drone = 0 # do better. calculate the yaw.


        x_target = request.target_pose.transform.translation.x
        y_target = request.target_pose.transform.translation.y
        z_target = request.target_pose.transform.translation.z

        radians = self.oariantationDifference(telloTransform,request)
 
        yaw_target = radians

        start_pose = [x_drone,y_drone,z_drone,yaw_drone]
        end_pose = [x_target,y_target,z_target,yaw_target]

        t,axis = self.AxisTrajectory(start_pose,end_pose)
        
        
        pose = Twist()

        self.send_request("follow_trajectory")

        start_time = time.time()
        current_time = time.time()

        while current_time-start_time < t :

            dt= current_time-start_time

            numbers = self.desired_pose(dt,axis)

            pose.linear.x = numbers[0]
            pose.linear.y = numbers[1]
            pose.linear.z = numbers[2]
            pose.angular.z = numbers[3]

            self.desired_pose_pub(pose)

            time.sleep(1/30)
            current_time = time.time()

        req_drone = TakePicture.Request()
        future_drone =self.sub_cli_drone.call_async(req_drone)
        rclpy.spin_until_future_complete(self.sub_node_trajectory,future_drone)

        result_drone = future_drone.result()

        if result_drone.success == False:
            # log that the drone failed to take a picture.
            print("drone failed to take a picture")
            
            pass
        
        self.drone2turtle()

        self.send_request("follow_turtle")

        response.success = True
        

    def service_drone2turtle(self, request,respons): #srv_drone2turtle. this is the service that the turtle calls to make the drone go to the turtle
        self.drone2turtle()

        respons.success = True

        return respons


    def drone2turtle(self):
        world2drone = self.tf_buffer.lookup_transform("drone","world")
        world2Turtle = self.tf_buffer.lookup_transform("turtle","world")

        hover_distance = 0.5 # how fare the drone hover over the turtle in meters
        hover_frame = world2Turtle
        hover_frame.transform.translation.z = hover_frame.transform.translation.z + hover_distance

        x_drone = world2drone.transform.translation.x 
        y_drone = world2drone.transform.translation.y
        z_drone = world2drone.transform.translation.z
        yaw_drone = 0 


        x_target = hover_frame.transform.translation.x 
        y_target = hover_frame.transform.translation.y
        z_target = hover_frame.transform.translation.z

        radians = self.oariantationDifference(world2drone,hover_frame)
 
        yaw_target = radians

        start_pose = [x_drone,y_drone,z_drone,yaw_drone]
        end_pose = [x_target,y_target,z_target,yaw_target]

        t,axis = self.AxisTrajectory(start_pose,end_pose)
        
        
        pose = Twist()

        self.send_request("follow_trajectory")

        start_time = time.time()
        current_time = time.time()

        while current_time-start_time < t :

            dt= current_time-start_time

            numbers = self.desired_pose(dt,axis)

            pose.linear.x = numbers[0]
            pose.linear.y = numbers[1]
            pose.linear.z = numbers[2]
            pose.angular.z = numbers[3]

            self.desired_pose_pub(pose)

            time.sleep(1/30)
            current_time = time.time()
        
        self.send_request("follow_turtle")

        



    

def main(args=None):
    rclpy.init(args=args)

    node = Trajectory()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        

