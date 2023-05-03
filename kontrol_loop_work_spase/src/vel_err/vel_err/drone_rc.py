import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class MySubscriber(Node):
    def __init__(self):
        super().__init__("drone_rc")
        self.subscription_ = self.create_subscription(Float32MultiArray, "drone_rc", self.callback, 10)

    def callback(self, msg):
        array = msg.data
        for i in array:
            self.get_logger().info(f"rc: {i}")

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

