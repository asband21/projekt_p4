import rclpy
from rclpy.node import Node

import numpy as np

import asyncio


from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


import math


from personal_interface.srv import TargetPose, TakePicture, ContinuePath, StateChanger

import time

import tf_transformations as tf



from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool



class Trajectory(Node):
    def __init__(self):
        super().__init__("trajectory") 
        self.sub_node_trajectory = rclpy.create_node("sub_cli_trajectory")

        self.sub_cli_drone = self.sub_node_trajectory.create_client(TakePicture,"take_picture")
        self.sub_cli_state = self.sub_node_trajectory.create_client(StateChanger,"Position")
        
        self.srv_targetPose = self.create_service(TargetPose, 'go_to_target_pose', self.FindAtoB)
        self.srv_drone2turtle = self.create_service(SetBool, 'drone2turtle', self.service_drone2turtle)


        self.desired_pose_pub = self.create_publisher(Twist,"desired_pose",10)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.get_logger().info("Trajectory is now running")




    def trajectory(self,t0,tx, pos_q0, pos_qf):


        G = np.zeros((4,4))
        B = np.zeros((4,1))
        x = np.zeros((4,1))



        G[0, 0] = 1
        G[0, 1] = t0
        G[0, 2] = np.power(t0,2)
        G[0, 3] = np.power(t0,3)

        G[1, 0] = 0
        G[1, 1] = 1
        G[1, 2] = np.multiply(2,t0)
        G[1, 3] = np.multiply(3, np.power(t0,2))

        G[2, 0] = 1
        G[2, 1] = tx
        G[2, 2] = np.power(tx,2)
        G[2, 3] = np.power(tx,3)

        G[3, 0] = 0
        G[3, 1] = 1
        G[3, 2] = np.multiply(2,tx)
        G[3, 3] = np.multiply(3, np.power(tx,2))


        B[0, 0] = pos_q0
        B[1, 0] = 0
        B[2, 0] = pos_qf
        B[3, 0] = 0

        X_inv = np.linalg.inv(G)
        coefficients = X_inv.dot(B)
        array = np.zeros((4))
        array[0] = coefficients[0]
        array[1] = coefficients[1]
        array[2] = coefficients[2]
        array[3] = coefficients[3]
        self.get_logger().info("Coefficients: " + str(array))
        return array



    def AxisTrajectory(self, A, B):
        
        t0 = 0
        tx = 1
        axis_max = np.zeros((4))
        axis = np.zeros((4,4))

        while True:
            value = 0            
            axis[0] = self.trajectory(t0,tx, A[0], B[0])
            axis[1] = self.trajectory(t0,tx, A[1], B[1])
            axis[2] = self.trajectory(t0,tx, A[2], B[2])
            axis[3] = self.trajectory(t0,tx, A[3], B[3])

            axis_max[0]=-axis[0,2]/(2*axis[0,3])
            axis_max[1]=-axis[1,2]/(2*axis[1,3])
            axis_max[2]=-axis[2,2]/(2*axis[2,3])
            axis_max[3]=-axis[3,2]/(2*axis[3,3])

            for i in range(4):
                if axis_max[i] > 0.9:
                    value = 1
            if value==1:
                tx += 0.5
            else:
                break

        return tx, axis # this is an array with the coefficents to the trajectories

    def desired_pose(self, dt, axis):

        pos_x = axis[0,0] + axis[0,1]*dt + axis[0,2]*np.power(dt,2) + axis[0,3]*np.power(dt,3)
        pos_y = axis[1,0] + axis[1,1]*dt + axis[1,2]*np.power(dt,2) + axis[1,3]*np.power(dt,3)
        pos_z = axis[2,0] + axis[2,1]*dt + axis[2,2]*np.power(dt,2) + axis[2,3]*np.power(dt,3)
        yaw_z = axis[3,0] + axis[3,1]*dt + axis[3,2]*np.power(dt,2) + axis[3,3]*np.power(dt,3)

        pose = np.zeros((4))
        pose[0] = pos_x
        pose[1] = pos_y
        pose[2] = pos_z
        pose[3] = yaw_z

        return pose # this is a 4 d array with the unit of meters for the first 3 elements and the last is radiens



    def oariantationDifference(self, q1, q2):
        
        rot_x_1 =q1.transform.rotation.x
        rot_y_1 =q1.transform.rotation.y
        rot_z_1 =q1.transform.rotation.z
        rot_w_1 =q1.transform.rotation.w

        start_rotation_M = tf.quaternion_matrix(rot_x_1,rot_y_1,rot_z_1,rot_w_1)

        rot_x_2 = q2.target_pose.transform.rotation.x
        rot_y_2 = q2.target_pose.transform.rotation.y
        rot_z_2 = q2.target_pose.transform.rotation.z
        rot_w_2 = q2.target_pose.transform.rotation.w

        end_rotation_M = tf.quaternion_matrix(rot_x_2,rot_y_2,rot_z_2,rot_w_2)

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
            req = StateChanger.Request()

            req.state = "follow_trajectory"
            future = self.sub_cli_position.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_trajectory,future)
            return future.result()
        
        elif request_to == "follow_turtle":
            while not self.sub_cli_trajectory.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('service not available, waiting again...')
            req = StateChanger.Request()

            req.state = "follow_turtle"
            future = self.sub_cli_position.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_trajectory,future)
            return future.result()
        



    async def FindAtoB(self,request,response):
        self.get_logger().info('Incoming request')
        telloTransform = asyncio.run(self.tf_buffer.lookup_transform_async('drone','world',self.get_clock().now()))
        self.get_logger().info('shut up')
        

        x_drone = telloTransform.transform.translation.x 
        y_drone = telloTransform.transform.translation.y
        z_drone = telloTransform.transform.translation.z
        yaw_drone = 0 # do better. calculate the yaw.


        x_target = request.target_pose.transform.translation.x
        y_target = request.target_pose.transform.translation.y
        z_target = request.target_pose.transform.translation.z

        # radians = self.oariantationDifference(telloTransform,request)
 
        # yaw_target = radians

        start_pose = [x_drone,y_drone,z_drone,0]
        end_pose = [x_target,y_target,z_target,0]

        t,axis = self.AxisTrajectory(start_pose,end_pose)
        
        
        pose = Twist()

        self.send_request("follow_trajectory")
        self.get_logger().info('Sending goal request...')
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

        self.get_logger().info('Goal reached!')

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
        world2drone  = asyncio.run(self.tf_buffer.lookup_transform_async("drone","world",  self.get_clock().now()))
        world2Turtle = asyncio.run(self.tf_buffer.lookup_transform_async("turtle","world",self.get_clock().now()))

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
        

