import rclpy
from rclpy.node import Node

import os
from glob import glob
from std_srvs.srv import Empty
import launch
import launch_ros.actions
from personal_interface.srv import TakePicture,TargetPose, StateChanger



def get_launch_file_path(launch_file_name):
    # Get the path to the directory containing this Python script
    this_file_dir = os.path.dirname(os.path.abspath(launch_file_name))
    
    # this_file_dir = os.path.abspath('system.launch.py')

    # Construct the path to the launch file relative to this script
    launch_file_path = os.path.join(this_file_dir,'install',"full_system",'share', "full_system", 'launch', launch_file_name)
    
    # Return the absolute path to the launch file
    return os.path.abspath(launch_file_path)
    # return this_file_dir

class initialization(Node):
    def __init__(self):
        super().__init__("initialization") 

        self.node_initialization = rclpy.create_node("node_initialization")

        self.cli_user_input = self.node_initialization.create_client(Empty,"user_input")
        # print(     (os.path.join('share', "full_system", 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))))
        # print(get_launch_file_path("system.launch.py"))
        # self.launch()
        self.create_all_clients()
        up = self.check_all_services()

        if up:
            # self.get_logger().info("All services are up, ready to fly into position? : ")
            self.get_logger().info("All services are up, ready to drive : ")
            self.send_request_to_user()
            
        
    def send_request_to_user(self):
        while not self.cli_user_input.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        request = Empty.Request()
        future = self.cli_user_input.call_async(request)
        rclpy.spin_until_future_complete(self.node_initialization,future)
        
        return future.result()


    def create_all_clients(self):
        self.cli_calculate_target_pose = self.node_initialization.create_client(TakePicture,"calculate_target_pose")
        # self.cli_go_to_target_pose = self.node_initialization.create_client(TargetPose,"go_to_target_pose")
        # self.cli_desired_pose_state = self.node_initialization.create_client(StateChanger,"desired_pose_state")
        # self.cli_drone2turtle = self.node_initialization.create_client(Empty,"drone2turtle")
        self.cli_turtle_state = self.node_initialization.create_client(StateChanger,"turtle_state")
        # self.cli_take_picture = self.node_initialization.create_client(TakePicture,"take_picture")
        # self.cli_takeoff = self.node_initialization.create_client(Empty,"takeoff")

    def launch(self):
        # Create the launch description
        ld = launch.LaunchDescription([
            launch.actions.IncludeLaunchDescription(
                launch.launch_description_sources.PythonLaunchDescriptionSource(
                    get_launch_file_path("system.launch.py")
                )
            )
        ])

        # Start the launch file
        launch_service = launch.LaunchService()
        launch_service.include_launch_description(ld)
        launch_service.run()





    def check_all_services(self):
        while not self.cli_calculate_target_pose.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("cli_calculate_target_pose service not available, waiting again...")
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