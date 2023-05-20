import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class MySubscriber(Node):
    def __init__(self):
        super().__init__("drone_volisty_error")
        self.subscription_ = self.create_subscription(Float32MultiArray, "drone_volisty_error", self.callback, 10)
        self.publisher_ = self.create_publisher(Twist, "drone_rc", 10)
        self.i_x = 1
        self.i_y = 1
        self.i_z = 1
        self.i_w = 0
        
        self.d_x = 0
        self.d_y = 0
        self.d_z = 0
        self.d_w = 0

    def callback(self, msg):
        array = msg.data
        array[8] = array[8]/1000000000
        array[4] = self.transfer_fun_x(array[4], array[8])
        array[5] = self.transfer_fun_y(array[5], array[8])
        array[6] = self.transfer_fun_z(array[6], array[8])
        array[7] = self.transfer_fun_w(array[7], array[8])
        #self.get_logger().info(f"Received: {array}")

        self.pub_rc(array)

    def transfer_fun_x(self, val, tids_delta):
        self.i_x = self.i_x + val*tids_delta
        d = (val - self.d_x)/tids_delta
        self.d_x = val
        kp = 200
        return kp*val + self.i_x

    def transfer_fun_y(self, val, tids_delta):
        self.i_y = self.i_y + val
        d = (val - self.d_y)/tids_delta
        self.d_y = val
        kp = 200
        return kp*val + self.i_y

    def transfer_fun_z(self, val, tids_delta):
        self.i_z = self.i_z + val
        d = (val - self.d_z)/tids_delta
        self.d_z = val
        kp = 200
        return kp*val

    def transfer_fun_w(self, val, tids_delta):
        self.i_w = self.i_w + val
        d = (val - self.d_w)/tids_delta
        self.d_w = val
        kp = -50
        return kp*val

    def pub_rc(self,array):

        twist_msg = Twist()

        twist_msg.linear.x = self.float_min_max_100(array[4])# clamp value between -100 and 100
        twist_msg.linear.y = self.float_min_max_100(array[5])# clamp value between -100 and 100
        twist_msg.linear.z = self.float_min_max_100(array[6])# clamp value between -100 and 100

        # Set the angular component of the Twist message
        twist_msg.angular.z = float(array[7])
        twist_msg.angular.y = 0.0
        twist_msg.angular.x = 0.0
        
        self.publisher_.publish(twist_msg)
        

    def float_min_max_100(self, tal):
        if tal > 100:
            return 100.0
        if tal < -100:
            return -100.0
        return float(tal)


def main(args=None):
    rclpy.init(args=args)
    node = MySubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

