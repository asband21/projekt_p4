

import rclpy


from rclpy.node import Node
from std_srvs.srv import SetBool

from personal_interface.srv import TargetPose


class request(Node):
    def __init__(self):
        super().__init__("request") 

        self.sub_node_simulated_vicon = rclpy.create_node("sub_node_simulated_vicon")

        self.cli_target = self.sub_node_simulated_vicon.create_client(TargetPose,"go_to_target_pose")
        self.cli_drone2turtle = self.sub_node_simulated_vicon.create_client(SetBool,"drone2turtle")




    def send_request(self,type):

        if type == "1":
            req = TargetPose.Request()
            while not self.cli_target.wait_for_service(timeout_sec=1.0):
                self.get_logger().info("service not available, waiting again...")
            
            req.target_pose.transform.translation.x = 6.0
            req.target_pose.transform.translation.y = 1.0
            req.target_pose.transform.translation.z = 4.0

            future = self.cli_target.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_simulated_vicon,future)
            print(future.result())
            return future.result()
        elif type == "2":
            req = SetBool.Request()
            while not self.cli_drone2turtle.wait_for_service(timeout_sec=1.0):
                self.get_logger().info("service not available, waiting again...")
            
            
            future = self.cli_drone2turtle.call_async(req)
            rclpy.spin_until_future_complete(self.sub_node_simulated_vicon,future)
            print(future.result())
            return future.result()


def main(args=None):
    rclpy.init(args=args)
    
    node = request()
    
    inputs = input("type here: ")
    response = node.send_request(inputs)

    while True:
        if response.success:
            print("Success")
            break
        elif not response.success:
            print("Failure")
            break

    
    rclpy.shutdown()


if __name__ == "__main__":
    main()