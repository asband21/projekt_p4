import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty, SetBool


from geometry_msgs.msg import Twist
from personal_interface.srv import StateChanger, TakePicture, Tf
import time
import numpy as np


# from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf_transformations as tf

import concurrent.futures

from std_msgs.msg import String

import threading

from geometry_msgs.msg import TransformStamped

from tf2_msgs.msg import TFMessage 

class turtle_follower(Node):
    def __init__(self):
        super().__init__("turtle_follower")

        self.current_vicon2turtle = TransformStamped()

        self.state = "idle"
        self.msg_state = String()
        self.previous_state = "idle"
        self.meters_driven = 0

        self.drive_velocity = 0.1
        self.turn_velocity = 1.0

        self.node_turtle_follower = rclpy.create_node("node_turtle_follower")


        # # # self.tf_buffer = Buffer(rclpy.duration.Duration(seconds=1.0))
        # # self.tf_listener = TransformListener(self.tf_buffer, self, spin_thread=True)


        self.cli_tf = self.node_turtle_follower.create_client(Tf,"vicon2turtle")
        self.cli_analisys = self.node_turtle_follower.create_client(TakePicture,"calculate_target_pose")
        self.cli_power_motors = self.node_turtle_follower.create_client(SetBool,"motor_power")
        self.srv_turtle_state = self.create_service(StateChanger,"/turtle_state",self.turtle_state_callback)


        self.pub_turtle = self.create_publisher(Twist,'/cmd_vel',10)
        self.pub_state = self.create_publisher(String,'/turtle_state',10)

        self.sub_state = self.create_subscription(String,'/turtle_state',self.state_callback,10)



        # self.power_motors(True)



        # self.create_timer(0.1, self.state_controller)


        # self.thread = threading.Thread(target=self.state_controller)
        # self.thread.daemon = True
        # self.thread.start()

        # while self.state == "done":
        #     thread.join()

        # self.state_controller()


    def send_tf_request(self):
        while not self.cli_tf.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("calculate_target_pose service not available, waiting again...")
        
        request = Tf.Request()
        future = self.cli_tf.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()


    def state_callback(self, msg):
        self.state = msg.data

        self.state_controller()





    def power_motors(self,bool):
        while not self.cli_power_motors.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("motor_power service not available, waiting again...")
        
        request = SetBool.Request()
        request.data = bool
        future = self.cli_power_motors.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()


    # def stop(self):
    #     self.stop_flag.set()
    #     self.thread.join()

    def turtle_state_callback(self, request, response):
        self.state = request.state
        response.success = True
        self.get_logger().info("state changed to: " + request.state)
        self.state_controller()
        return response


    def calculate_trajectory(self,coord1, coord2, max_velocity=1):
        """
        Calculate the trajectory between two 1D coordinates with a maximum velocity of max_velocity.

        Parameters:
        coord1 (tuple): A tuple containing the x, y, z, and t coordinates of the starting point.
        coord2 (tuple): A tuple containing the x, y, z, and t coordinates of the ending point.
        max_velocity (float, optional): The maximum velocity of the object in meters per second. Defaults to 1.

        Returns:
        tuple: A tuple containing the time taken to travel the trajectory and the coordinates at each point along the trajectory.
        """
        distance = coord2 - coord1
        time = abs((distance) / max_velocity)

        print("time it takes: " ,time)

        # create the time vector and calculate the coefficients of the third degree polynomial
        t = np.linspace(0, time, num=int(time)+1)
        A = np.array([
            [t[0]**3   , t[0]**2 , t[0] , 1],
            [t[-1]**3  , t[-1]**2, t[-1], 1],
            [3*t[0]**2 , 2*t[0]  , 1    , 0],
            [3*t[-1]**2, 2*t[-1] , 1    , 0]
        ])
        b = np.array([coord1, coord2, 0, 0])
        c = np.linalg.solve(A, b)



        return (time, c)




    def desired_vel(self, t, c):

        # # calculate the position of the object at each point along the trajectory
        # trajectory = []
        # x = c[0,0]*t**3 + c[1,0]*t**2 + c[2,0]*t + c[3,0]
        # y = c[0,1]*t**3 + c[1,1]*t**2 + c[2,1]*t + c[3,1]
        # z = c[0,2]*t**3 + c[1,2]*t**2 + c[2,2]*t + c[3,2]
        # trajectory.append((x, y, z, 0.0))

        # calculate the position of the object at each point along the trajectory
        # trajectory = 0
        # trajectory = c[0]*t**3 + c[1]*t**2 + c[2]*t + c[3]
        velocity = 3*c[0]*t**2 + 2*c[1]*t + c[2]
        # velocity.append((float(x), float(y), float(z), float(yaw)))




        return velocity





    # def turtle_state_callback(self,request,response):
    #     self.state = request.state
    #     if self.state == "continue":
    #         response.success = True
    #     else:
    #         response.success = False

    #     return response


    def send_request(self):
        while not self.cli_analisys.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")

        self.state = "sending_request"

        request = TakePicture.Request()
        future = self.cli_analisys.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower,future)

        return future.result()

    # def send_request_async(self):
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         future = executor.submit(self.send_request)
    #         return future.result()



    def turn(self, turn_way):

        if turn_way == "left":
            # turn left 90 degrees

            start_transform = self.send_tf_request().tf

            start_quat = [0,0,0,0]
            start_quat[0] = start_transform.transform.rotation.x
            start_quat[1] = start_transform.transform.rotation.y
            start_quat[2] = start_transform.transform.rotation.z
            start_quat[3] = start_transform.transform.rotation.w

            start_zyx = tf.euler_from_quaternion(start_quat,axes='rzyx')

            start_yaw = start_zyx[0]


            turn_angle = np.pi/2 # unit rad



            current_yaw = start_yaw

            cmd_vel = Twist()

            cmd_vel.angular.z = self.turn_velocity
            self.pub_turtle.publish(cmd_vel)

            while abs(start_yaw-current_yaw) < turn_angle:
                self.get_logger().info("angle: " + str(abs(start_yaw-current_yaw)))

                current_transform = self.send_tf_request().tf

                current_quat = [0,0,0,0]
                current_quat[0] = current_transform.transform.rotation.x
                current_quat[1] = current_transform.transform.rotation.y
                current_quat[2] = current_transform.transform.rotation.z
                current_quat[3] = current_transform.transform.rotation.w

                current_zyx = tf.euler_from_quaternion(current_quat,axes='rzyx')

                current_yaw = current_zyx[0]
                time.sleep(1/30)

            cmd_vel.angular.z = 0.0
            self.pub_turtle.publish(cmd_vel)






            # # # wheel = Twist()



            # # # turn_vel = 1.0 # unit rad/s

            # # # turn_angle = np.pi/2 # unit rad

            # # # turn_time = (1/turn_angle)/turn_vel

            # # # # wheel.angular.z = turn_vel


            # # # t,coeffecitents = self.calculate_trajectory(0,turn_angle,turn_vel)

            # # # start_time = time.time()
            # # # current_time = time.time()

            # # # while current_time-start_time < t :

            # # #     dt= current_time-start_time

            # # #     vel = self.desired_vel(dt,coeffecitents)

            # # #     wheel.angular.z = float(vel)
            # # #     self.pub_turtle.publish(wheel)

            # # #     time.sleep(1/30)
            # # #     current_time = time.time()

            # # # wheel.angular.z = float(0)
            # # # self.pub_turtle.publish(wheel)







        elif turn_way == "right":
            # turn right 180 degrees


            start_transform = self.send_tf_request().tf

            start_quat = [0,0,0,0]
            start_quat[0] = start_transform.transform.rotation.x
            start_quat[1] = start_transform.transform.rotation.y
            start_quat[2] = start_transform.transform.rotation.z
            start_quat[3] = start_transform.transform.rotation.w

            start_zyx = tf.euler_from_quaternion(start_quat,axes='rzyx')

            start_yaw = start_zyx[0]


            turn_angle = np.pi # unit rad



            current_yaw = start_yaw

            cmd_vel = Twist()

            cmd_vel.angular.z = -self.turn_velocity
            self.pub_turtle.publish(cmd_vel)

            while abs(start_yaw-current_yaw) < turn_angle:

                self.get_logger().info("angle: " + str(abs(start_yaw-current_yaw)))
                current_transform = self.send_tf_request().tf

                current_quat = [0,0,0,0]
                current_quat[0] = current_transform.transform.rotation.x
                current_quat[1] = current_transform.transform.rotation.y
                current_quat[2] = current_transform.transform.rotation.z
                current_quat[3] = current_transform.transform.rotation.w

                current_zyx = tf.euler_from_quaternion(current_quat,axes='rzyx')

                current_yaw = current_zyx[0]
                time.sleep(1/30)

            cmd_vel.angular.z = 0.0
            self.pub_turtle.publish(cmd_vel)


            # # # wheel = Twist()

            # # # turn_vel = 1.0 # unit rad/s

            # # # turn_angle = -np.pi # unit rad

            # # # turn_time = (1/turn_angle)/turn_vel

            # # # # wheel.angular.z = turn_vel


            # # # t,coeffecitents = self.calculate_trajectory(0,turn_angle,turn_vel)

            # # # start_time = time.time()
            # # # current_time = time.time()

            # # # while current_time-start_time < t :

            # # #     dt= current_time-start_time

            # # #     vel = self.desired_vel(dt,coeffecitents)

            # # #     wheel.angular.z = float(vel)
            # # #     self.pub_turtle.publish(wheel)

            # # #     time.sleep(1/30)
            # # #     current_time = time.time()

            # # # wheel.angular.z = float(0)
            # # # self.pub_turtle.publish(wheel)




    def drive_stright(self):
        # drive 1 meter
        

            start_transform = self.send_tf_request().tf#,rclpy.duration.Duration(seconds=0.5)
            self.get_logger().info("start_transform1234: " + str(start_transform)) 


            drive_distance = 1.0 # unit meter


            
            start_x = start_transform.transform.translation.x
            start_y = start_transform.transform.translation.y
            start_z = start_transform.transform.translation.z

        


            cmd_vel = Twist()

            cmd_vel.linear.x = self.drive_velocity
            cmd_vel.linear.y = self.drive_velocity
            cmd_vel.linear.z = self.drive_velocity
            self.pub_turtle.publish(cmd_vel)
            # time.sleep(4)
            current_transform = self.send_tf_request().tf#,rclpy.duration.Duration(seconds=0.5)
            self.get_logger().info("current_transform1234: " + str(current_transform)) 
            current_x = start_x
            current_y = start_y
            current_z = start_z
            
            distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
            while distance < drive_distance:
                
                # can = self.tf_buffer.can_transform("vicon","turtle",rclpy.time.Time())
                # self.get_logger().info("can: " + str(can)) 
                
                current_transform = self.send_tf_request().tf
                # log the current transform values

                self.get_logger().info("start_transform: " + str(start_transform)) 
                self.get_logger().info("current_transform: " + str(current_transform)) 


                # print("current_transform: ",current_transform)

                current_x = current_transform.transform.translation.x
                current_y = current_transform.transform.translation.y
                current_z = current_transform.transform.translation.z

                distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
                self.get_logger().info("distance: " + str(distance))


                time.sleep(1/30)

            cmd_vel.linear.x = 0.0
            self.pub_turtle.publish(cmd_vel)


        # # wheel = Twist()

        # # forward_vel = 0.2 # unit m/s

        # # drive_distance = 1 # unit meters

        # # drive_time = (1/drive_distance)/ forward_vel
        # # self.get_logger().info("drive_time: " + str(drive_time))

        # # wheel.linear.x = forward_vel

        # # start_time = time.time()
        # # current_time = time.time()
        # # while current_time-start_time < drive_time:
        # #     self.get_logger().info("driving")
        # #     self.pub_turtle.publish(wheel)
        # #     current_time = time.time()
        # #     time.sleep(1/30)


        # # wheel.linear.x = 0.0
        # # self.pub_turtle.publish(wheel)
        # # # wheel = Twist()

        # # # drive_vel = 0.2 # unit rad/s

        # # # drive_distance = 1.0 # unit rad

        # # # turn_time = (1/drive_distance)/drive_vel

        # # # # wheel.angular.z = drive_vel


        # # # t,coeffecitents = self.calculate_trajectory(0,drive_distance,drive_vel)

        # # # start_time = time.time()
        # # # current_time = time.time()

        # # # while current_time-start_time < t :

        # # #     dt= current_time-start_time

        # # #     vel = self.desired_vel(dt,coeffecitents)

        # # #     wheel.linear.x = float(vel)
        # # #     self.pub_turtle.publish(wheel)

        # # #     time.sleep(1/30)
        # # #     current_time = time.time()
        # # # wheel.linear.x = float(0)
        # # # self.pub_turtle.publish(wheel)


    #Rember to look at the state aging, depenon where the state changes
    def state_controller(self):

        self.get_logger().info("state_controller started")

        if self.meters_driven >= 5:
            
            self.get_logger().info("state_controller ended")
            return


        if self.state == "idle":
            self.get_logger().info("state: " + self.state)
            return
        elif self.state == "continue":
            
            self.msg_state.data = "drive_stright"
            self.pub_state.publish(self.msg_state)

        
        elif self.state == "drive_stright":
            self.get_logger().info("state: " + self.state)
            self.drive_stright()
            self.msg_state.data = "turn_left"


            self.previous_state = "drive_stright"
            self.meters_driven += 1
            self.pub_state.publish(self.msg_state)

            return
        

        elif self.state == "turn_right":
            self.get_logger().info("state: " + self.state)
            self.turn("right")

            self.msg_state.data = "image_analisys"

            self.previous_state = "turn_right"
            self.pub_state.publish(self.msg_state)

            return

        elif self.state == "turn_left":
            self.get_logger().info("state: " + self.state)
            self.turn("left")

            if self.previous_state == "drive_stright":
                self.msg_state.data = "image_analisys"


                self.previous_state = "turn_left"
                self.pub_state.publish(self.msg_state)
                return
            elif self.previous_state == "image_analisys":
                self.msg_state.data = "drive_stright"


                self.previous_state = "turn_left"
                self.pub_state.publish(self.msg_state)
                return


            return

        elif self.state == "image_analisys":
            self.get_logger().info("state: " + self.state)
            self.send_request()
            
            
            if self.previous_state == "turn_left":

                self.msg_state.data = "turn_right"
                self.pub_state.publish(self.msg_state)
                return
            elif self.previous_state == "turn_right":
                
                self.previous_state = "image_analisys"
                self.msg_state.data = "turn_left"
                self.pub_state.publish(self.msg_state)
                return            
            
            return




        # while True:
        # # while not self.stop_flag.is_set():
        #     # if self.stop_flag.is_set():
        #     #     break

        #     self.get_logger().info("state: " + self.state)
        #     if self.meters_driven > self.tarck_length:
        #         self.state = "done"
        #         # self.stop()
        #         break

        #     if self.state == "idle":
        #         time.sleep(1/30)
        #         continue

        #     # drive 1 meter
        #     self.drive_stright()
        #     # job1 = threading.Thread(target=self.drive_stright)
        #     # job1.start()
        #     # job1.join()

        #     self.meters_driven += 1
        #     # turn left 90 degrees
        #     self.turn("left")
        #     # job2 = threading.Thread(target=self.turn,args=("left",))
        #     # job2.start()
        #     # job2.join()

        #     # send request to image analisys
        #     self.send_request()
        #     # job3 = threading.Thread(target=self.send_request_async)
        #     # job3.start()
        #     # job3.join()


        #     # while True:
        #     #     self.get_logger().info("waiting for state change: " + str(self.state))
        #     #     if self.state == "continue":
        #     #         self.state = "idle"
        #     #         break
        #     #     time.sleep(1/30)

        #     # turn right 180 degrees
        #     self.turn("right")

        #     # job4 = threading.Thread(target=self.turn,args=("right",))
        #     # job4.start()
        #     # job4.join()



        #     # send request to image analisys
        #     self.send_request()

        #     # job5 = threading.Thread(target=self.send_request_async)
        #     # job5.start()
        #     # job5.join()

        #     # while True:
        #     #     if self.state == "continue":
        #     #         self.state = "idle"
        #     #         break
        #     #     time.sleep(1/30)

        #     # turn left 90 degrees
        #     self.turn("left")

        #     # job6 = threading.Thread(target=self.turn,args=("left",))
        #     # job6.start()
        #     # job6.join()


        self.get_logger().info("state_controller ended")






def main(args=None):
    rclpy.init(args=args)

    node = turtle_follower()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()


