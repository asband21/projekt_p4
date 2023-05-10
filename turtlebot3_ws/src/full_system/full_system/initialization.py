import rclpy
from rclpy.node import Node

import os
from glob import glob
from std_srvs.srv import Empty
import launch
import launch_ros.actions



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

        self.sub_node_initialization = rclpy.create_node("sub_node_initialization")

        print(     (os.path.join('share', "full_system", 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))))
        print(get_launch_file_path("system.launch.py"))
        self.start_my_node()


    def create_all_clients(self):
        self.cli_calculate_target_pose = self.sub_node_initialization.create_client(Empty,"calculate_target_pose")
        self.cli_go_to_target_pose = self.sub_node_initialization.create_client(Empty,"go_to_target_pose")
        self.cli_state_changer = self.sub_node_initialization.create_client(Empty,"state_changer")
        self.cli_drone2turtle = self.sub_node_initialization.create_client(Empty,"drone2turtle")
        self.cli_change_state = self.sub_node_initialization.create_client(Empty,"change_state")
        self.cli_take_picture = self.sub_node_initialization.create_client(Empty,"take_picture")
        self.cli_takeoff = self.sub_node_initialization.create_client(Empty,"takeoff")

    def start_my_node(self):
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
            self.get_logger().info("service not available, waiting again...")




    def send_request(self,client,request):
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self.sub_node_initialization,future)
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