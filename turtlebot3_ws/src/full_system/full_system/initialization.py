import rclpy
from rclpy.node import Node


class initialization(Node):
    def __init__(self):
        super().__init__("initialization") 

        self.sub_node_initialization = rclpy.create_node("sub_node_initialization")

        self.create_all_clients()


        self.check_all_services()

    def create_all_clients(self):
        self.sub_cli_calculate_target_pose = self.sub_node_initialization.create_client(Empty,"calculate_target_pose")
        self.sub_cli_go_to_target_pose = self.sub_node_initialization.create_client(Empty,"go_to_target_pose")
        self.sub_cli_state_changer = self.sub_node_initialization.create_client(Empty,"state_changer")
        self.sub_cli_drone2turtle = self.sub_node_initialization.create_client(Empty,"drone2turtle")
        self.sub_cli_change_state = self.sub_node_initialization.create_client(Empty,"change_state")
        self.sub_cli_take_picture = self.sub_node_initialization.create_client(Empty,"take_picture")
        self.sub_cli_takeoff = self.sub_node_initialization.create_client(Empty,"takeoff")


    def check_all_services(self):
        while not self.sub_cli_calculate_target_pose.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        