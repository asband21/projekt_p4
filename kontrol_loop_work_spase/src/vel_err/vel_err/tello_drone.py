import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from djitellopy import Tello
import time

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__("simulated_drone") 

        self.til = True
#        self.til = False
        if self.til:
            self.drone = Tello()
            self.drone.connect()
            self.drone.takeoff()
            self.get_logger().info("launshet:")
        #self.drone.send_rc_control(0,0,0,0)
        
        self.sub_rc = self.create_subscription(Twist,"drone_rc",self.callback_drone_rc,10)
        self.h = 1
#    def __del__(self):
#        self.drone.send_rc_control(0,0,0,0)

    def callback_drone_rc(self, msg):
        #if self.h == 0:
        #    self.h = 1
        #    self.drone.takeoff()
        if self.til:
            #self.get_logger().info("rc :")
            self.h = self.h*-1
            if self.h > 0:
                self.drone.send_rc_control(int(msg.linear.x), int(msg.linear.y), int(msg.linear.z), int(msg.angular.z))
            #self.drone.send_rc_control(20,0,0,0)
        else:
            self.get_logger().info(f"rc x:{int(msg.linear.x)}, y:{int(msg.linear.y)}, z:{int(msg.linear.z)}, yor:{int(msg.angular.z)}")


def main(args=None):
    rclpy.init(args=args)
    node = SimulatedDrone()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
