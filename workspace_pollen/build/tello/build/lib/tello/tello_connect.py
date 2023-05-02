import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import String

from djitellopy import Tello

class tello_connecter(Node):
    def __init__(self):
        self.tello = Tello()

        self.tello.connect()

        self.sub_velocity = self.create_subscription(Twist, 'control', self.velocity_callback, 10)        
        self.sub_land = self.create_subscription(String, 'land', self.land_callback, 1)
        self.sub_takeoff = self.create_subscription(String, 'takeoff', self.takeoff_callback, 1)
        self.create_service(String, 'takeoff', self.takeoff_callback)

        self.pub_takeoff = self.create_publisher(String, 'takeoff', 1)
        self.pub_land = self.create_publisher(String, 'land', 1)

    def velocity_callback(self, msg):
        '''This is the callback function that listens to the control topic.
        The unit it accepts is m/s. It converts it to cm/s and sends it to the drone'''
        self.velocity = msg
        x = int(self.velocity.linear.x) * 100
        y = int(self.velocity.linear.y) * 100
        z = int(self.velocity.linear.z) * 100
        z = int(self.velocity.angular.z) * 100

        self.tello.send_rc_control(x, y, z, z)

    def takeoff_callback(self, msg):
        self.tello.takeoff()
        # send a message that the drone has taken off
        self.pub_takeoff.publish('lift')
    
    
    def land_callback(self, msg):
        
        self.tello.land()
        
        # send a message that the drone has landed
        self.pub_land.publish('landed')



def main(args=None):
    rclpy.init(args=args)

    tello_connecter = tello_connecter()

    rclpy.spin(tello_connecter)

    tello_connecter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()