import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty

from geometry_msgs.msg import Twist
from personal_interface.srv import StateChanger, TakePicture
import time
import numpy as np


class turtle_follower(Node):
    def __init__(self):
        super().__init__("turtle_follower") 

        self.tarck_length = 5
        self.state = "idle"
        self.meters_driven = 0

        self.node_turtle_follower = rclpy.create_node("node_turtle_follower")

        self.cli_analisys = self.node_turtle_follower.create_client(TakePicture,"calculate_target_pose")
        self.srv_state_changer = self.create_service(StateChanger,"state_changer",self.state_changer_callback)
        self.pub_turtle = self.create_publisher(Twist,'/cmd_vel',10)

        self.state_controller()



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
        time = distance / max_velocity
        
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





    def state_changer_callback(self,request,response):
        self.state = request.state
        if self.state == "continue":
            response.success = True
        else:
            response.success = False
                    
        return response


    def send_request(self):
        while not self.cli_analisys.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        request = TakePicture.Request()
        future = self.cli_analisys.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower,future)

        while future.result() == None:
            time.sleep(1/30)
            
        return future.result()



    def turn(self, turn_way):

        if turn_way == "left":
            # turn left 90 degrees
            wheel = Twist()

            turn_vel = 1.0 # unit rad/s

            turn_angle = np.pi/2 # unit rad

            turn_time = (1/turn_angle)/turn_vel

            # wheel.angular.z = turn_vel


            t,coeffecitents = self.calculate_trajectory(0,turn_angle,1)

            start_time = time.time()
            current_time = time.time()

            while current_time-start_time < t :

                dt= current_time-start_time

                vel = self.desired_vel(dt,coeffecitents)

                wheel.angular.z = float(vel)
                self.pub_turtle.publish(wheel)

                time.sleep(1/30)
                current_time = time.time()



            
        elif turn_way == "right":
            # turn right 180 degrees 
            wheel = Twist()

            turn_vel = 1.0 # unit rad/s

            turn_angle = -np.pi # unit rad

            turn_time = (1/turn_angle)/turn_vel

            # wheel.angular.z = turn_vel


            t,coeffecitents = self.calculate_trajectory(0,turn_angle,1)

            start_time = time.time()
            current_time = time.time()

            while current_time-start_time < t :

                dt= current_time-start_time

                vel = self.desired_vel(dt,coeffecitents)

                wheel.angular.z = float(vel)
                self.pub_turtle.publish(wheel)

                time.sleep(1/30)
                current_time = time.time()
            



    def drive_stright(self):
        # drive 1 meter
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
        wheel = Twist()

        drive_vel = 1.0 # unit rad/s

        drive_distance = 1.0 # unit rad

        turn_time = (1/drive_distance)/drive_vel

        # wheel.angular.z = drive_vel


        t,coeffecitents = self.calculate_trajectory(0,drive_distance,1)

        start_time = time.time()
        current_time = time.time()

        while current_time-start_time < t :

            dt= current_time-start_time

            vel = self.desired_vel(dt,coeffecitents)

            wheel.linear.x = float(vel)
            self.pub_turtle.publish(wheel)

            time.sleep(1/30)
            current_time = time.time()



    #Rember to look at the state aging, depenon where the state changes
    def state_controller(self):

        self.get_logger().info("state_controller started")
        while True:

            self.get_logger().info("state: " + self.state)
            if self.meters_driven > self.tarck_length:
                break

            # drive 1 meter 
            self.drive_stright()

            self.meters_driven += 1
            # turn left 90 degrees
            self.turn("left")

            # send request to image analisys
            self.send_request()

            # while True:
            #     self.get_logger().info("waiting for state change: " + str(self.state))
            #     if self.state == "continue":
            #         self.state = "idle"
            #         break
            #     time.sleep(1/30)

            # turn right 180 degrees
            self.turn("right")


            # send request to image analisys
            self.send_request()

            # while True:
            #     if self.state == "continue":
            #         self.state = "idle"
            #         break
            #     time.sleep(1/30)
        
            # turn left 90 degrees
            self.turn("left")
        
        self.get_logger().info("state_controller ended")






def main(args=None):
    rclpy.init(args=args)

    node = turtle_follower()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()


