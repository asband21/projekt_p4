import rclpy
from rclpy.node import Node

import numpy as np



from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


import math


from personal_interface.srv import TargetPose, TakePicture, StateChanger

import time

import tf_transformations as tf



from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool



class Trajectory(Node):
    def __init__(self):
        super().__init__("trajectory") 

        self.max_velocity = 0.5


        self.tf_buffer = Buffer(rclpy.duration.Duration(seconds=1.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)


        self.node_trajectory = rclpy.create_node("cli_trajectory")

        self.sub_cli_drone = self.node_trajectory.create_client(TakePicture,"take_picture")
        self.sub_cli_state = self.node_trajectory.create_client(StateChanger,"change_state")
        
        self.srv_targetPose = self.create_service(TargetPose, 'go_to_target_pose', self.FindAtoB)
        self.srv_drone2turtle = self.create_service(SetBool, 'drone2turtle', self.service_drone2turtle)

        self.desired_pose_pub = self.create_publisher(Twist,"desired_pose",10)

        self.get_logger().info("Trajectory is now running")





    def calculate_trajectory(self,coord1, coord2, max_velocity=1):
        """
        Calculate the trajectory between two 4D coordinates with a maximum velocity of max_velocity.

        Parameters:
        coord1 (tuple): A tuple containing the x, y, z, and t coordinates of the starting point.
        coord2 (tuple): A tuple containing the x, y, z, and t coordinates of the ending point.
        max_velocity (float, optional): The maximum velocity of the object in meters per second. Defaults to 1.

        Returns:
        tuple: A tuple containing the time taken to travel the trajectory and the coordinates at each point along the trajectory.
        """
        distance = np.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2 + (coord2[2] - coord1[2])**2)
        time = distance / max_velocity
        
        # create the time vector and calculate the coefficients of the third degree polynomial
        t = np.linspace(0, time, num=int(time)+1)
        A = np.array([
            [t[0]**3   , t[0]**2 , t[0] , 1],
            [t[-1]**3  , t[-1]**2, t[-1], 1],
            [3*t[0]**2 , 2*t[0]  , 1    , 0],
            [3*t[-1]**2, 2*t[-1] , 1    , 0]
        ])
        b = np.array([coord1, coord2, [0, 0, 0, 0], [0, 0, 0, 0]])
        c = np.linalg.solve(A, b)
        

            
        return (time, c)




    def desired_pose(self, t, c):

        # # calculate the position of the object at each point along the trajectory
        # trajectory = []
        # x = c[0,0]*t**3 + c[1,0]*t**2 + c[2,0]*t + c[3,0]
        # y = c[0,1]*t**3 + c[1,1]*t**2 + c[2,1]*t + c[3,1]
        # z = c[0,2]*t**3 + c[1,2]*t**2 + c[2,2]*t + c[3,2]
        # trajectory.append((x, y, z, 0.0))

        # calculate the position of the object at each point along the trajectory
        trajectory = [0,0,0,0]
        trajectory[0] = c[0,0]*t**3 + c[1,0]*t**2 + c[2,0]*t + c[3,0]
        trajectory[1] = c[0,1]*t**3 + c[1,1]*t**2 + c[2,1]*t + c[3,1]
        trajectory[2] = c[0,2]*t**3 + c[1,2]*t**2 + c[2,2]*t + c[3,2]
        trajectory[3] = c[0,3]*t**3 + c[1,3]*t**2 + c[2,3]*t + c[3,3]
        # trajectory.append((float(x), float(y), float(z), float(yaw)))



        return trajectory







    def send_request(self,request_to):

        if request_to == "follow_trajectory":
            while not self.sub_cli_state.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('follow_trajectoryservice not available, waiting again...')
            req = StateChanger.Request()

            req.state = "follow_trajectory"
            future = self.sub_cli_state.call_async(req)
            rclpy.spin_until_future_complete(self.node_trajectory,future)
            response = future.result()
            print(response)
            
            return future.result()
        
        elif request_to == "follow_turtle":
            while not self.sub_cli_state.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('follow_turtle service not available, waiting again...')
            req = StateChanger.Request()

            req.state = "follow_turtle"
            future = self.sub_cli_state.call_async(req)
            rclpy.spin_until_future_complete(self.node_trajectory,future)
            response = future.result()
            print(response)

            return future.result()
        
        elif request_to == "take_picture":
            while not self.sub_cli_drone.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('take picture service not available, waiting again...')
            
            req = TakePicture.Request()
            future = self.sub_cli_drone.call_async(req)
            rclpy.spin_until_future_complete(self.node_trajectory,future)

            response = future.result()

            while not response.success:
                time.sleep(1/30)
            
            return future.result()    

        



    def FindAtoB(self,request,response_request):
        self.get_logger().info('Incoming request to go to target')

        telloTransform = self.tf_buffer.lookup_transform('world','drone',rclpy.time.Time(),rclpy.duration.Duration(seconds=0.1))
        

        x_drone = telloTransform.transform.translation.x 
        y_drone = telloTransform.transform.translation.y
        z_drone = telloTransform.transform.translation.z
        yaw_drone = 0 # do better. calculate the yaw.

        print("x_drone: ",x_drone)
        print("y_drone: ",y_drone)
        print("z_drone: ",z_drone)
        print("yaw_drone: ",yaw_drone)
        x_target = request.target_pose.transform.translation.x
        y_target = request.target_pose.transform.translation.y
        z_target = request.target_pose.transform.translation.z

 

        start_pose = [x_drone,y_drone,z_drone,0]
        end_pose = [x_target,y_target,z_target,0]

        t,axis = self.calculate_trajectory(start_pose,end_pose,self.max_velocity)

        print("-----------------t: ",t)
        
        pose = Twist()

        self.send_request("follow_trajectory")
        self.get_logger().info('Sending goal request...')
        start_time = time.time()
        current_time = time.time()

        while current_time-start_time < t :

            dt= current_time-start_time

            numbers = self.desired_pose(dt,axis)

            pose.linear.x =  float(numbers[0])
            pose.linear.y =  float(numbers[1])
            pose.linear.z =  float(numbers[2])
            pose.angular.z = float(numbers[3])

            self.desired_pose_pub.publish(pose)

            time.sleep(1/30)
            current_time = time.time()

        self.get_logger().info('Goal reached!')


        self.get_logger().info('take picture')
        self.send_request("take_picture")
        self.get_logger().info('picture taken')


        
        self.get_logger().info('drone to turtle')
        self.drone2turtle()
        self.get_logger().info('drone at turtle')

        self.get_logger().info('send request to follow turtle')
        response = self.send_request("follow_turtle")

        while not response.success:
            time.sleep(1/30)
            response = self.send_request("follow_turtle")
        
        self.get_logger().info('turtle followed')

        response_request.success = True

        self.get_logger().info('request done')
        return response_request

        
        

    def service_drone2turtle(self, request,respons): #srv_drone2turtle. this is the service that the turtle calls to make the drone go to the turtle
        self.get_logger().info('Incoming request to drone2turtle')

        self.drone2turtle()

        respons.success = True

        self.get_logger().info('request done for drone2turtle')

        return respons


    def drone2turtle(self):
        
        world2drone  = self.tf_buffer.lookup_transform('world','drone' , rclpy.time.Time(), rclpy.duration.Duration(seconds=0.1))
        world2Turtle = self.tf_buffer.lookup_transform('world','turtle', rclpy.time.Time(), rclpy.duration.Duration(seconds=0.1))

        hover_distance = 0.5 # how fare the drone hover over the turtle in meters
        world2Turtle.transform.translation.z += hover_distance


        start_pose = [0,0,0,0]
        start_pose[0] = world2drone.transform.translation.x 
        start_pose[1] = world2drone.transform.translation.y
        start_pose[2] = world2drone.transform.translation.z
        start_pose[3] = 0.0 


        end_pose   = [0,0,0,0]
        end_pose[0] = world2Turtle.transform.translation.x 
        end_pose[1] = world2Turtle.transform.translation.y
        end_pose[2] = world2Turtle.transform.translation.z
        end_pose[3] = 0.0

 


        t,axis = self.calculate_trajectory(start_pose,end_pose,self.max_velocity)


        
        pose = Twist()

        self.send_request("follow_trajectory")

        start_time = time.time()
        current_time = time.time()

        while current_time-start_time < t :

            dt = current_time-start_time

            numbers = self.desired_pose(dt,axis)

            pose.linear.x = numbers[0]
            pose.linear.y = numbers[1]
            pose.linear.z = numbers[2]
            pose.angular.z = numbers[3]

            self.desired_pose_pub.publish(pose)

            time.sleep(1/30)
            current_time = time.time()
        
        self.send_request("follow_turtle")

        



    

def main(args=None):
    rclpy.init(args=args)
    node = Trajectory()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        



























    # def trajectory(self,t0,tx, pos_q0, pos_qf):


    #     G = np.zeros((4,4))
    #     B = np.zeros((4,1))
    #     x = np.zeros((4,1))



    #     G[0, 0] = 1
    #     G[0, 1] = t0
    #     G[0, 2] = np.power(t0,2)
    #     G[0, 3] = np.power(t0,3)

    #     G[1, 0] = 0
    #     G[1, 1] = 1
    #     G[1, 2] = np.multiply(2,t0)
    #     G[1, 3] = np.multiply(3, np.power(t0,2))

    #     G[2, 0] = 1
    #     G[2, 1] = tx
    #     G[2, 2] = np.power(tx,2)
    #     G[2, 3] = np.power(tx,3)

    #     G[3, 0] = 0
    #     G[3, 1] = 1
    #     G[3, 2] = np.multiply(2,tx)
    #     G[3, 3] = np.multiply(3, np.power(tx,2))


    #     B[0, 0] = pos_q0
    #     B[1, 0] = 0
    #     B[2, 0] = pos_qf
    #     B[3, 0] = 0

    #     X_inv = np.linalg.inv(G)
    #     coefficients = X_inv.dot(B)
    #     array = np.zeros((4))
    #     array[0] = coefficients[0]
    #     array[1] = coefficients[1]
    #     array[2] = coefficients[2]
    #     array[3] = coefficients[3]
    #     self.get_logger().info("Coefficients: " + str(array))
    #     return array



    # def calculate_trajectory(self, coord1, coord2, max_velocity=1):
    #     """
    #     Calculate the trajectory between two 3D coordinates with a maximum velocity of max_velocity.

    #     Parameters:
    #     coord1 (tuple): A tuple containing the x, y, and z coordinates of the starting point.
    #     coord2 (tuple): A tuple containing the x, y, and z coordinates of the ending point.
    #     max_velocity (float, optional): The maximum velocity of the object in meters per second. Defaults to 1.

    #     Returns:
    #     tuple: A tuple containing the time taken to travel the trajectory and the coordinates at each point along the trajectory.
    #     """
    #     distance = np.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2 + (coord2[2] - coord1[2])**2)
    #     time = distance / max_velocity
        
    #     # create the time vector and calculate the coefficients of the third degree polynomial
    #     t = np.linspace(0, time, num=int(time)+1)
    #     A = np.array([
    #         [t[0]**3, t[0]**2, t[0], 1],
    #         [t[-1]**3, t[-1]**2, t[-1], 1],
    #         [3*t[0]**2, 2*t[0], 1, 0],
    #         [3*t[-1]**2, 2*t[-1], 1, 0]
    #     ])
    #     b = np.array([coord1, coord2, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    #     c = np.linalg.solve(A, b)
        
    #     # # calculate the position of the object at each point along the trajectory
    #     # trajectory = []
    #     # for i in range(int(time)+1):
    #     #     x = c[0,0]*t[i]**3 + c[1,0]*t[i]**2 + c[2,0]*t[i] + c[3,0]
    #     #     y = c[0,1]*t[i]**3 + c[1,1]*t[i]**2 + c[2,1]*t[i] + c[3,1]
    #     #     z = c[0,2]*t[i]**3 + c[1,2]*t[i]**2 + c[2,2]*t[i] + c[3,2]
    #     #     trajectory.append((x, y, z))
            
    #     return (time, c)


    # def AxisTrajectory(self, A, B):
        
    #     t0 = 0
    #     tx = 1
    #     axis_max = np.zeros((4))
    #     axis = np.zeros((4,4))

    #     while True:
    #         value = 0            
    #         print("---------tx", tx)
    #         axis[0] = self.trajectory(t0,tx, A[0], B[0])
    #         axis[1] = self.trajectory(t0,tx, A[1], B[1])
    #         axis[2] = self.trajectory(t0,tx, A[2], B[2])
    #         axis[3] = self.trajectory(t0,tx, A[3], B[3])

    #         axis_max[0] = -(2*axis[0,1])/(2*(3*axis[0,0]))
    #         axis_max[1] = -(2*axis[1,1])/(2*(3*axis[1,0]))
    #         axis_max[2] = -(2*axis[2,1])/(2*(3*axis[2,0]))
    #         axis_max[3] = 0.0
    #         #-(2*axis[3,2])/(2*(3*axis[3,3]))

    #         print("---------axis_max", axis_max)
    #         for i in range(4):
    #             if abs(axis_max[i]) > 0.2:
    #                 value = 1
    #         if value==1:
    #             tx += 0.5
    #         else:
    #             break

    #     return tx, axis # this is an array with the coefficents to the trajectories
    # def desired_pose(self, dt, axis):

    #     pos_x = axis[0,0] + axis[0,1]*dt + axis[0,2]*np.power(dt,2) + axis[0,3]*np.power(dt,3)
    #     pos_y = axis[1,0] + axis[1,1]*dt + axis[1,2]*np.power(dt,2) + axis[1,3]*np.power(dt,3)
    #     pos_z = axis[2,0] + axis[2,1]*dt + axis[2,2]*np.power(dt,2) + axis[2,3]*np.power(dt,3)
    #     yaw_z = axis[3,0] + axis[3,1]*dt + axis[3,2]*np.power(dt,2) + axis[3,3]*np.power(dt,3)

    #     pose = np.zeros((4))
    #     pose[0] = pos_x
    #     pose[1] = pos_y
    #     pose[2] = pos_z
    #     pose[3] = yaw_z

    #     return pose # this is a 4 d array with the unit of meters for the first 3 elements and the last is radiens





    

    # def oariantationDifference(self, q1, q2):
        
    #     rot_x_1 =q1.transform.rotation.x
    #     rot_y_1 =q1.transform.rotation.y
    #     rot_z_1 =q1.transform.rotation.z
    #     rot_w_1 =q1.transform.rotation.w

    #     start_rotation_M = tf.quaternion_matrix(rot_x_1,rot_y_1,rot_z_1,rot_w_1)

    #     rot_x_2 = q2.target_pose.transform.rotation.x
    #     rot_y_2 = q2.target_pose.transform.rotation.y
    #     rot_z_2 = q2.target_pose.transform.rotation.z
    #     rot_w_2 = q2.target_pose.transform.rotation.w

    #     end_rotation_M = tf.quaternion_matrix(rot_x_2,rot_y_2,rot_z_2,rot_w_2)

    #     start_y = [0,0]
    #     end_y   = [0,0]

    #     start_y[0] = start_rotation_M[0,1]
    #     start_y[1] = start_rotation_M[1,1]
        
        
    #     end_y[0] = end_rotation_M[1,1]
    #     end_y[1] = end_rotation_M[1,1]

    #     return math.atan2(end_y[1],end_y[0]) # returns the oriantation diff of the end y vector to the drones oriantation. THE UNIT IS RADIANS

