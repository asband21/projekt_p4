import rclpy
from rclpy.node import Node



from tf2_ros.transform_broadcaster import TransformBroadcaster

from geometry_msgs.msg import TransformStamped


from personal_interface.srv import TargetPose

class SimulatedVicon(Node):
    def __init__(self):
        super().__init__("simulated_vicon") 

        self.sub_node_simulated_vicon = rclpy.create_node("sub_node_simulated_vicon")

        self.sub_cli_simulated_vicon = self.create_client(TargetPose,"go_to_target_pose")

        self.tf_broadcaster = TransformBroadcaster(self)

        hz=1/30
        self.create_timer(hz,self.drone_pose)
        self.create_timer(hz,self.turtle_pose)


    def drone_pose(self):
        drone = TransformStamped()

        drone.header = self.get_clock().now().to_msg()
        drone.header.frame_id = "world"
        drone.child_frame_id = "drone"

        drone.transform.translation.x = 0
        drone.transform.translation.y = 0
        drone.transform.translation.z = 0

        drone.transform.rotation.x = 0
        drone.transform.rotation.y = 0
        drone.transform.rotation.z = 0
        drone.transform.rotation.w = 1

        self.tf_broadcaster.sendTransform(drone)


    def turtle_pose(self):
        turtle = TransformStamped()

        turtle.header = self.get_clock().now().to_msg()
        turtle.header.frame_id = "world"
        turtle.child_frame_id = "turtle"

        turtle.transform.translation.x = 0
        turtle.transform.translation.y = 0
        turtle.transform.translation.z = 0

        turtle.transform.rotation.x = 0
        turtle.transform.rotation.y = 0
        turtle.transform.rotation.z = 0
        turtle.transform.rotation.w = 1

        self.tf_broadcaster.sendTransform(turtle)

    
    def send_request(self):
        req = TargetPose.Request()
        while not self.sub_cli_simulated_vicon.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        req.target_pose.transform.translation.x = 1.0
        req.target_pose.transform.translation.y = 1.0
        req.target_pose.transform.translation.z = 1.0

        future = self.sub_cli_simulated_vicon.call_async(req)
        rclpy.spin_until_future_complete(self.sub_node_simulated_vicon,future)
        return future.result()




        

def main(args=None):
    rclpy.init(args=args)

    node = SimulatedVicon()
        
    rclpy.spin(node)
    if bool(input()):
        node.send_request() 

    rclpy.shutdown()


if __name__ == "__main__":
    main()


