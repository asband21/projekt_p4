#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from costom_interface.msg import ViconInfo
from costom_interface.srv import Velocities
from std_msgs.msg import Float32MultiArray

class MyNode(Node):

    def __init__(self):
        super().__init__("one_node")
        self.sub_one_node = rclpy.create_node("sub_one_node")
        self.cli_subnode = self.sub_one_node.create_client(Velocities, "/srv/Velocities")
        self.sub_vel = self.create_subscription(ViconInfo, "vicon_info", self.callback_velocities_request, 10)


    def callback_velocities_request(self, msg):
        print("callback")
        while not self.cli_subnode.wait_for_service(1.0):
            self.get_logger().warn("wating for service")

        request = Velocities.Request()
        request.position.linear.x = msg.position.linear.x
        request.position.linear.y = msg.position.linear.y
        request.position.linear.z = msg.position.linear.z
        request.position.angular.z = msg.position.angular.z
        request.velocity.linear.x = msg.velocity.linear.x
        request.velocity.linear.y = msg.velocity.linear.y 
        request.velocity.linear.z = msg.velocity.linear.z
        request.velocity.angular.z = msg.velocity.angular.z

        future = self.cli_subnode.call_async(request)
        rclpy.spin_until_future_complete(self.sub_one_node,future)
        respons= future.result()

        error = respons.error_velocity.angular.z - msg.velocity.angular.z
        self.get_logger().info(f"error yor{error}")




#        if respons.success:
#            self.get_logger().info("success")
#        elif not respons.success:
#            self.get_logger().info("failure")




def main(args=None):    
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__== '__name__':
    main()
