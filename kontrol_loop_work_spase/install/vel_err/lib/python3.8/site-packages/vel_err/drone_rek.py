import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class MySubscriber(Node):
    def __init__(self):
        super().__init__("drone_error")
        self.subscription_ = self.create_subscription(Float32MultiArray, "drone_error", self.callback, 10)
        self.publisher_ = self.create_publisher(Twist, "drone_rc", 10)

    def callback(self, msg):
        my_array = msg.data
        array = my_array
        for i in range(4):
            array[i] = array[i]*2
        self.get_logger().info(f"Received: {array}")

        self.pub_rc(array)

    def pub_rc(self,array):

        twist_msg = Twist()

        twist_msg.linear.x = min(max(-100, array[0]), 100)  # clamp value between -100 and 100
        twist_msg.linear.y = min(max(-100, array[1]), 100)  # clamp value between -100 and 100
        twist_msg.linear.z = min(max(-100, array[2]), 100)  # clamp value between -100 and 100

        # Set the angular component of the Twist message
        twist_msg.angular.z = float(array[3])
        self.get_logger().info(str(array[3]))
        twist_msg.angular.y = 0.0
        twist_msg.angular.x = 0.0
        
        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

