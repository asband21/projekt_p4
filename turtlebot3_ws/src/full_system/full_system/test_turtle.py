import rclpy

from rclpy.node import Node

from personal_interface.srv import StateChanger, TakePicture, Tf

from geometry_msgs.msg import Twist

from std_srvs.srv import SetBool

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf_transformations as tf

from geometry_msgs.msg import TransformStamped


import numpy as np
import time

class testTurtle(Node):

    def __init__(self):
        super().__init__('test_turtle')
        self.get_logger().info("test_turtle node has been started")
        self.current_vicon2turtle = TransformStamped()
        self.drive_velocity = 0.1
        self.node_turtle_follower = rclpy.create_node("node_turtle_follower")



        self.cli_turtle = self.node_turtle_follower.create_client(StateChanger,"state_changer")
        self.cli_power_motors = self.node_turtle_follower.create_client(SetBool,"motor_power")

        self.srv_analisys = self.create_service(TakePicture,"calculate_target_pose",self.srv_take_pic)



        self.pub_turtle = self.create_publisher(Twist,'/cmd_vel',10)

        self.tf_buffer = Buffer(cache_time=rclpy.duration.Duration(seconds=10))
        self.tf_listener = TransformListener(self.tf_buffer,self,spin_thread=True)
        


        self.power_motors(True)



        print(self.tf_buffer.can_transform("vicon","turtle",rclpy.time.Time())) # True
        self.timeout = 0.5
        self.drive_stright()
        self.drive_velocity = 0.1



 

    def power_motors(self,bool):
        while not self.cli_power_motors.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("motor_power service not available, waiting again...")
        
        request = SetBool.Request()
        request.data = bool
        future = self.cli_power_motors.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()


    def send_tf_request(self):
        while not self.cli_turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("state_changer service not available, waiting again...")
        
        request = Tf.Request()
        future = self.cli_turtle.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()

    def drive_stright(self):
        # drive 1 meter
        
        # wait til the self.current_vicon2turtle is available
        # while self.current_vicon2turtle == None:
        #     time.sleep(1/30)
            

        start_transform = self.tf_buffer.lookup_transform("vicon","turtle",rclpy.time.Time(),rclpy.duration.Duration(seconds=0.5))
        self.get_logger().info("start_transform1234: " + str(start_transform)) 


        drive_distance = 0.5 # unit meter


        
        start_x = start_transform.transform.translation.x
        start_y = start_transform.transform.translation.y
        start_z = start_transform.transform.translation.z

    


        cmd_vel = Twist()

        cmd_vel.linear.x = self.drive_velocity
        cmd_vel.linear.y = self.drive_velocity
        cmd_vel.linear.z = self.drive_velocity
        self.pub_turtle.publish(cmd_vel)
        # time.sleep(4)
        current_transform = self.tf_buffer.lookup_transform("vicon","turtle",rclpy.time.Time(),rclpy.duration.Duration(seconds=0.5))
        self.get_logger().info("current_transform1234: " + str(current_transform)) 
        current_x = start_x
        current_y = start_y
        current_z = start_z
        
        distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
        while distance < drive_distance:
            
            can = self.tf_buffer.can_transform("vicon","turtle",rclpy.time.Time())
            self.get_logger().info("can: " + str(can)) 
            
            current_transform = self.tf_buffer.lookup_transform("vicon","turtle",rclpy.time.Time(),rclpy.duration.Duration(seconds=0.5))
            # log the current transform values

            self.get_logger().info("start_transform: " + str(start_transform)) 
            self.get_logger().info("current_transform: " + str(current_transform)) 


            # print("current_transform: ",current_transform)

            current_x = current_transform.transform.translation.x
            current_y = current_transform.transform.translation.y
            current_z = current_transform.transform.translation.z

            distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
            self.get_logger().info("distance: " + str(distance))


            time.sleep(1/30)

        cmd_vel.linear.x = 0.0
        self.pub_turtle.publish(cmd_vel)


    def srv_take_pic(self,request,response):
        self.get_logger().info("srv_take_pic has been called")
        time.sleep(5)
        response.success = True
        
        # send_request_result = self.send_request()
        # self.get_logger().info("send_request_result: " + str(send_request_result))

        return response

    def send_request(self):
        while not self.cli_turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        request = StateChanger.Request()
        request.state = "continue"

        future = self.cli_turtle.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower,future)

        while future.result() == None:
            time.sleep(1/30)
            
        return future.result()




def main(args=None):
    rclpy.init(args=args)

    node = testTurtle()

    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()