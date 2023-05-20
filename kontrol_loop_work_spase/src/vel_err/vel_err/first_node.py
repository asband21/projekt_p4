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
        self.publisher = self.create_publisher(Float32MultiArray, "drone_volisty_error", 10)

        #save error
        self.filename_error = "error.csv"
        self.error_fil = open(self.filename_error, 'w')

        #disherder
        self.filename_dis = "disherder.csv"
        self.dis_fil = open(self.filename_dis, 'w')

        #volosty
        self.filename_vol = "volosty.csv"
        self.vol_fil = open(self.filename_vol, 'w')

        #tis
        self.filename_tid = "tids_delta.csv"
        self.vol_tid = open(self.filename_tid, 'w')

#    def __del__(self):
#        self.dis_pos_fil.close()

    def save_error_vector(self, vector):
        #formatted_vector = [f"{value:8.5f}," for value in vector]
        #self.dis_pos_fil.write(f'{formatted_vector}\n')
        self.error_fil.write(f'{vector}\n')

    def save_disherder(self, disherder):
        self.dis_fil.write(f'{disherder.position.linear.x},{disherder.position.linear.y},{disherder.position.linear.z},{disherder.position.angular.z},{disherder.velocity.linear.x},{disherder.velocity.linear.y},{disherder.velocity.linear.z},{disherder.velocity.angular.z}\n')
    
    def save_volsty(self, disherder):
        #self.vol_fil.write(f'{disherder.linear.x},{disherder.linear.y},{disherder.linear.z},{disherder.angular.z}\n')
        self.vol_fil.write(f'{disherder.error_position.linear.x},{disherder.error_position.linear.y},{disherder.error_position.linear.z},{disherder.error_position.angular.z},{disherder.error_velocity.linear.x},{disherder.error_velocity.linear.y},{disherder.error_velocity.linear.z},{disherder.error_velocity.angular.z}\n')
    
    def save_tid(self, tid):
        self.vol_tid.write(f'{tid}\n')

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

        error = [0,0,0,0,0,0,0,0,0]
        # pos error
        error[0] = float(respons.error_position.linear.x - msg.position.linear.x)
        error[1] = float(respons.error_position.linear.y - msg.position.linear.y)
        error[2] = float(respons.error_position.linear.z - msg.position.linear.z)
        error[3] = float(respons.error_position.angular.z - msg.position.angular.z)

        # vel error
        error[4] = float(respons.error_velocity.linear.x - msg.velocity.linear.x)
        error[5] = float(respons.error_velocity.linear.y - msg.velocity.linear.y)
        error[6] = float(respons.error_velocity.linear.z - msg.velocity.linear.z)
        error[7] = float(respons.error_velocity.angular.z - msg.velocity.angular.z)
        
        error[8] = msg.velocity.angular.y

        self.save_tid(msg.velocity.angular.y)
        self.save_error_vector(error)
        self.save_disherder(msg)
        self.save_volsty(respons)
        #self.get_logger().info(f"error yor{error}")
        msg = Float32MultiArray(data=error)
        self.publisher.publish(msg)

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
