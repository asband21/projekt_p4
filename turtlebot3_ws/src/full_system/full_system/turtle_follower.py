import rclpy
from rclpy.node import Node
import tf_transformations as tf
from std_srvs.srv import SetBool
from geometry_msgs.msg import Twist
from personal_interface.srv import StateChanger, TakePicture, Tf
import time
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped


class turtle_follower(Node):
    def __init__(self):
        super().__init__("turtle_follower")

        self.current_vicon2turtle = TransformStamped()

        self.state = "idle"
        self.msg_state = String()
        self.previous_state = "idle"
        self.how_far_to_drive = 2
        self.meters_driven = 0

        self.drive_velocity = 0.1
        self.turn_velocity = 0.5

        self.node_turtle_follower = rclpy.create_node("node_turtle_follower")


        self.cli_tf = self.node_turtle_follower.create_client(Tf,"vicon2turtle")
        self.cli_analisys = self.node_turtle_follower.create_client(TakePicture,"calculate_target_pose")
        self.cli_power_motors = self.node_turtle_follower.create_client(SetBool,"motor_power")
        self.srv_turtle_state = self.create_service(StateChanger,"/turtle_state",self.turtle_state_callback)


        self.pub_turtle = self.create_publisher(Twist,'/cmd_vel',10)
        self.pub_state = self.create_publisher(String,'/turtle_state',10)

        self.sub_state = self.create_subscription(String,'/turtle_state',self.state_callback,10)




    def send_tf_request(self):
        while not self.cli_tf.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("calculate_target_pose service not available, waiting again...")
        
        request = Tf.Request()
        future = self.cli_tf.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()





    def power_motors(self,bool):
        while not self.cli_power_motors.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("motor_power service not available, waiting again...")
        
        request = SetBool.Request()
        request.data = bool
        future = self.cli_power_motors.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower, future)
        
        return future.result()


    def state_callback(self, msg):
        self.state = msg.data

        self.state_controller()


    def turtle_state_callback(self, request, response):
        self.state = request.state
        response.success = True
        self.get_logger().info("state changed to: " + request.state)
        self.state_controller()
        return response





    def send_request(self):
        while not self.cli_analisys.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")

        self.state = "sending_request"

        request = TakePicture.Request()
        future = self.cli_analisys.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower,future)

        return future.result()


    def get_current_yaw(self):
        transform = self.send_tf_request().tf

        quat = [transform.transform.rotation.x,
                transform.transform.rotation.y,
                transform.transform.rotation.z,
                transform.transform.rotation.w]

        yaw,_,_ = tf.euler_from_quaternion(quat, axes='rzyx')

        if yaw < 0:
            yaw = yaw + 2*np.pi

        return np.degrees(yaw)

    def turn(self, turn):
        self.power_motors(True)
        angle = self.get_current_yaw()

        max_vel = 1.0
        min_vel = 0.3

        if turn == "left":
            if angle > 270:
                angle = angle - 270
            else:
                angle = angle + 90
            
            while abs(self.get_current_yaw() - angle) > 1:
                self.get_logger().info("eroror" + str(abs(self.get_current_yaw() - angle)))
                # self.get_logger().info("angle: " + str(angle))
                # self.get_logger().info("current_yaw: " + str(self.get_current_yaw()))
                error = angle - self.get_current_yaw()
                error = error * 0.01
                # self.get_logger().info("error: " + str(error))
                cmd_vel = Twist()
                # if error > 0:
                #     cmd_vel.angular.z = self.turn_velocity
                # else:
                #     cmd_vel.angular.z = -self.turn_velocity
                
                if abs(error) > 1:
                    if error > 0:
                        cmd_vel.angular.z = -max_vel
                    else:
                        cmd_vel.angular.z = max_vel

                elif abs(error) < 0.1:
                    if error > 0:
                        cmd_vel.angular.z = -min_vel
                    else:
                        cmd_vel.angular.z = min_vel
                else:

                    cmd_vel.angular.z = error
                    

                self.get_logger().info("cmd_vel: " + str(cmd_vel.angular.z))
                self.pub_turtle.publish(cmd_vel)
            cmd_vel = Twist()
            cmd_vel.angular.z = 0.0
            self.pub_turtle.publish(cmd_vel)
        
        if turn == "right":

            if angle > 180:
                angle = angle -180
            else:
                angle = angle + 180

            while abs(self.get_current_yaw() - angle) > 1:
                self.get_logger().info("eroror" + str(abs(self.get_current_yaw() - angle)))
                # self.get_logger().info("angle: " + str(angle))
                # self.get_logger().info("current_yaw: " + str(self.get_current_yaw()))
                error = angle - self.get_current_yaw()
                error = error * 0.01
                # self.get_logger().info("error: " + str(error))
                cmd_vel = Twist()
                # if error > 0:
                #     cmd_vel.angular.z = self.turn_velocity
                # else:
                #     cmd_vel.angular.z = -self.turn_velocity

                if abs(error) > 1:
                    if error > 0:
                        cmd_vel.angular.z = max_vel
                    else:
                        cmd_vel.angular.z = -max_vel

                elif abs(error) < 0.1:
                    if error > 0:
                        cmd_vel.angular.z = min_vel
                    else:
                        cmd_vel.angular.z = -min_vel
                else:

                    cmd_vel.angular.z = error
                    

                self.get_logger().info("cmd_vel: " + str(cmd_vel.angular.z))
                self.pub_turtle.publish(cmd_vel)
            cmd_vel = Twist()
            cmd_vel.angular.z = 0.0
            self.pub_turtle.publish(cmd_vel)
        self.power_motors(False)


    def drive_stright(self):
        # drive 1 meter
            self.power_motors(True)
        

            start_transform = self.send_tf_request().tf


            drive_distance = 1.0 # unit meter


            
            start_x = start_transform.transform.translation.x
            start_y = start_transform.transform.translation.y
            start_z = start_transform.transform.translation.z

        


            cmd_vel = Twist()

            cmd_vel.linear.x = self.drive_velocity
            cmd_vel.linear.y = self.drive_velocity
            cmd_vel.linear.z = self.drive_velocity
            self.pub_turtle.publish(cmd_vel)

            current_transform = self.send_tf_request().tf

            current_x = start_x
            current_y = start_y
            current_z = start_z
            
            distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
            while distance < drive_distance:
                
                
                current_transform = self.send_tf_request().tf



                current_x = current_transform.transform.translation.x
                current_y = current_transform.transform.translation.y
                current_z = current_transform.transform.translation.z

                distance = np.sqrt((current_x - start_x)**2 + (current_y - start_y)**2 + (current_z - start_z)**2)
                self.get_logger().info("distance: " + str(distance))


                time.sleep(1/30)

            cmd_vel.linear.x = 0.0
            self.pub_turtle.publish(cmd_vel)
            self.power_motors(False)



    #Rember to look at the state aging, depenon where the state changes
    def state_controller(self):

        self.get_logger().info("state_controller started")

        if self.meters_driven > self.how_far_to_drive:
            
            self.get_logger().info("state_controller ended")
            return


        if self.state == "idle":
            self.get_logger().info("state: " + self.state)
            return
        elif self.state == "continue":
            self.previous_state = "continue"

            self.msg_state.data = "turn_left"
            self.pub_state.publish(self.msg_state)

        
        elif self.state == "drive_stright":
            self.get_logger().info("state: " + self.state)
            self.drive_stright()
            self.msg_state.data = "turn_left"


            self.previous_state = "drive_stright"
            self.meters_driven += 1
            self.pub_state.publish(self.msg_state)

            return
        

        elif self.state == "turn_right":
            self.get_logger().info("state: " + self.state)
            self.turn("right")

            self.msg_state.data = "image_analisys"

            self.previous_state = "turn_right"
            self.pub_state.publish(self.msg_state)

            return

        elif self.state == "turn_left":
            self.get_logger().info("state: " + self.state)
            self.turn("left")



            if self.previous_state == "drive_stright":
                self.msg_state.data = "image_analisys"


                self.previous_state = "turn_left"
                self.pub_state.publish(self.msg_state)
                return
            elif self.previous_state == "image_analisys":
                self.msg_state.data = "drive_stright"


                self.previous_state = "turn_left"
                self.pub_state.publish(self.msg_state)
                return
            elif self.previous_state == "continue":
                self.msg_state.data = "image_analisys"


                self.previous_state = "turn_left"
                self.pub_state.publish(self.msg_state)


            return

        elif self.state == "image_analisys":
            self.get_logger().info("state: " + self.state)
            self.send_request()
            
            
            if self.previous_state == "turn_left":

                self.msg_state.data = "turn_right"
                self.pub_state.publish(self.msg_state)
                return
            elif self.previous_state == "turn_right":
                
                self.previous_state = "image_analisys"
                self.msg_state.data = "turn_left"
                self.pub_state.publish(self.msg_state)
                return            
            
            return




        self.get_logger().info("state_controller ended")






def main(args=None):
    rclpy.init(args=args)

    node = turtle_follower()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == "__main__":
    main()





