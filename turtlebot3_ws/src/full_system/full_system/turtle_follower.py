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
        self.pub_turtle = self.create_publisher(Twist,'cmd_vel',10)

        self.state_controller()


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

            turn_vel = 0.2 # unit rad/s

            turn_angle = np.pi/2 # unit rad

            turn_time = turn_vel/turn_angle

            wheel.angular.z = turn_vel

            start_time = time.time()
            current_time = time.time()
            while current_time-start_time > turn_time:
                self.pub_turtle.publish(wheel)
                current_time = time.time()

            wheel.angular.z = 0.0
            self.pub_turtle.publish(wheel)
            
        elif turn_way == "right":
            # turn right 180 degrees 
            wheel = Twist()

            turn_vel = -0.2 # unit rad/s

            turn_angle = np.pi # unit rad

            turn_time = turn_vel/turn_angle

            wheel.angular.z = turn_vel

            start_time = time.time()
            current_time = time.time()
            while current_time-start_time > turn_time:
                self.pub_turtle.publish(wheel)
                current_time = time.time()

            wheel.angular.z = 0.0
            self.pub_turtle.publish(wheel)
            



    def drive_stright(self):
        # drive 1 meter
        wheel = Twist()

        forward_vel = 0.2 # unit m/s

        drive_distance = 1 # unit meters

        turn_time = forward_vel/drive_distance

        wheel.linear.z = forward_vel

        start_time = time.time()
        current_time = time.time()
        while current_time-start_time > turn_time:
            self.pub_turtle.publish(wheel)
            current_time = time.time()

        wheel.linear.z = 0.0
        self.pub_turtle.publish(wheel)



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

            while True:
                if self.state == "continue":
                    self.state = "idle"
                    break
                time.sleep(1/30)

            # turn right 180 degrees
            self.turn("right")


            # send request to image analisys
            self.send_request()

            while True:
                if self.state == "continue":
                    self.state = "idle"
                    break
                time.sleep(1/30)
        
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


