import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from djitellopy import Tello
import time

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__("simulated_drone") 
        self.drone = Tello()
        self.drone.connect()
        self.sub_rc = self.create_subscription(Twist,"drone_rc",self.callback_drone_rc,10)

    def callback_drone_rc(self, msg):
        self.drone.send_rc_control(msg.linear.x, msg.linear.y, msg.linear.z, msg.angular.z)

def main(args=None):
    rclpy.init(args=args)
    node = SimulatedDrone()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
