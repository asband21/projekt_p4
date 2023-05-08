import rclpy
from rclpy.node import Node


from personal_interface.srv import TargetPose
from std_srvs.srv import Empty



class image_analisys(Node):
    def __init__(self):
        super().__init__("image_analisys") 

        self.sub_node_image_analisys = rclpy.create_node("sub_node_image_analisys")

        self.sub_cli_image_analisys = self.create_client(TargetPose,"go_to_target_pose")

        self.srv_calulate_target_pose = self.create_service(Empty,"calculate_target_pose",self.callback_srv_taget_pose)



    def send_request(self,req):
        while not self.sub_cli_simulated_vicon.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        future = self.sub_cli_simulated_vicon.call_async(req)
        rclpy.spin_until_future_complete(self.sub_node_image_analisys,future)
        return future.result()
    

    def callback_srv_taget_pose(self,request,response):
        
        
        return 

    def image_analisys(self):
        req = TargetPose.Request()
        req.target_pose.transform.translation.x = 6.0
        req.target_pose.transform.translation.y = 1.0
        req.target_pose.transform.translation.z = 4.0
        req.target_pose.transform.rotation.x = 0.0
        req.target_pose.transform.rotation.y = 0.0
        req.target_pose.transform.rotation.z = 0.0
        req.target_pose.transform.rotation.w = 1.0
        


def main(args=None):
    rclpy.init(args=args)

    node = image_analisys()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()
