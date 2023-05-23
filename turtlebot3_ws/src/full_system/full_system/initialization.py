import rclpy
from rclpy.node import Node

import os
from glob import glob
from std_srvs.srv import Empty
import launch
import launch_ros.actions
from personal_interface.srv import TakePicture,TargetPose, StateChanger


class initialization(Node):
    def __init__(self):
        super().__init__("initialization") 

        self.node_initialization = rclpy.create_node("node_initialization")

        # self.cli_user_input = self.node_initialization.create_client(Empty,"user_input")
     
        self.create_all_clients()
        up = self.check_all_services()

        if up:
            # self.get_logger().info("All services are up, ready to fly into position? : ")
            self.get_logger().info("All services are up, ready to drive")
            self.change_turtle_state()

            # self.user_input()

            
        

    def create_all_clients(self):
        self.cli_calculate_target_pose = self.node_initialization.create_client(TakePicture,"calculate_target_pose")
        # self.cli_go_to_target_pose = self.node_initialization.create_client(TargetPose,"go_to_target_pose")
        # self.cli_desired_pose_state = self.node_initialization.create_client(StateChanger,"desired_pose_state")
        # self.cli_drone2turtle = self.node_initialization.create_client(Empty,"drone2turtle")
        self.cli_turtle_state = self.node_initialization.create_client(StateChanger,"/turtle_state")
        # self.cli_take_picture = self.node_initialization.create_client(TakePicture,"take_picture")
        # self.cli_takeoff = self.node_initialization.create_client(Empty,"takeoff")

    def change_turtle_state(self):
        while not self.cli_turtle_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        request = StateChanger.Request()
        request.state = "continue"
        self.get_logger().info("request sent" + str(request))
        future = self.cli_turtle_state.call_async(request)
        rclpy.spin_until_future_complete(self.node_initialization,future)
        
        return future.result()


    def user_input(self):
                
        # user_input = input("All services are up, ready to fly into position? : ")
        user_input = input("All services are up, ready to drive? : ")
        
        print(user_input)
        if user_input == "y":
            # self.send_request()
            self.get_logger().info("sending request to from user")
            self.change_turtle_state()
            self.get_logger().info("turtle_state changed")
        elif user_input == "n":
            print("hello")





    def check_all_services(self):
        # while not self.cli_calculate_target_pose.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("cli_calculate_target_pose service not available, waiting again...")
        # while not self.cli_go_to_target_pose.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("cli_go_to_target_pose service not available, waiting again...")
        # while not self.cli_desired_pose_state.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("cli_desrided_pose_state service not available, waiting again...")
        # while not self.cli_drone2turtle.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("cli_drone2turtle service not available, waiting again...")
        while not self.cli_turtle_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("cli_turtle_state service not available, waiting again...")
        # while not self.cli_take_picture.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("cli_take_picture service not available, waiting again...")

        return True




    def send_request(self,client,request):
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(f"{client} service not available, waiting again...")
        

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self.node_initialization,future)
        while future.result() == None:
            self.get_logger().info("waiting for response...")
        
        return future.result()
    




def main(args=None):
    rclpy.init(args=args)
    
    node = initialization()

    rclpy.spin(node)    

    rclpy.shutdown()

if __name__ == "__main__":
    main()