import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage

class MinimalSubscriber(Node):
    
        def __init__(self):
            super().__init__('minimal_subscriber')
            self.subscription = self.create_subscription(
                TFMessage,
                '/tf_test',
                self.listener_callback,
                10)
            self.subscription  # prevent unused variable warning
    
        def listener_callback(self, msg):
            length = len(msg.transforms)
            self.get_logger().info('I heard: "%s"' % length)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()




    # [INFO] [1681135571.634897191] [minimal_subscriber]: I heard: "
    # tf2_msgs.msg.TFMessage(
    #      transforms=
    #      [geometry_msgs.msg.TransformStamped(
    #      header=std_msgs.msg.Header(
    #      stamp=builtin_interfaces.msg.Time(sec=1681135571, nanosec=624541398), frame_id='B'), 
    #      child_frame_id='C', 
    #      transform=geometry_msgs.msg.Transform(translation=geometry_msgs.msg.Vector3(x=1.0, y=0.0, z=0.0), 
    #                                            rotation=geometry_msgs.msg.Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)))])"