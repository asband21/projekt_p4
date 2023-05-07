

import rclpy


from rclpy.node import Node

from personal_interface.srv import TargetPose


class request(Node):
    def __init__(self):
        super().__init__("request") 

        self.sub_node_simulated_vicon = rclpy.create_node("sub_node_simulated_vicon")

        self.sub_cli_simulated_vicon = self.create_client(TargetPose,"go_to_target_pose")




    def send_request(self):
        req = TargetPose.Request()
        while not self.sub_cli_simulated_vicon.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        req.target_pose.transform.translation.x = 6.0
        req.target_pose.transform.translation.y = 1.0
        req.target_pose.transform.translation.z = 4.0

        future = self.sub_cli_simulated_vicon.call_async(req)
        rclpy.spin_until_future_complete(self.sub_node_simulated_vicon,future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    
    node = request()
    
    if input()=="1":
        
        response = node.send_request()
        while True:
            if response.success:
                print("Success")
            elif not response.success:
                print("Failure")

    
    rclpy.shutdown()


if __name__ == "__main__":
    main()