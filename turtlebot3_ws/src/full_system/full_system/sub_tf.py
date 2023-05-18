import rclpy

from rclpy.node import Node 

from tf2_msgs.msg import TFMessage 


class sub_tf(Node):

    def __init__(self):
        super().__init__('sub_tf')
        self.get_logger().info("sub_tf node has been started")

        self.sub_vicon2turtle = self.create_subscription(TFMessage, 'tf', self.sub_vicon2turtle, 10 )


    # def sub_vicon2turtle(self,msg):
    #     self.current_vicon2turtle = msg
    #     print(self.current_vicon2turtle)
        

    def sub_vicon2turtle(self, msg):

        source_frame_id = 'vicon'
        target_frame_id = 'turtle'
        self.get_logger().info("msg: " + str(msg.transforms))
        for transform in msg.transforms:
            if (transform.header.frame_id == source_frame_id and transform.child_frame_id == target_frame_id
            ):
                # Found the desired transform
                self.current_vicon2turtle = transform
                self.get_logger().info("current_vicon2turtle: " + str(self.current_vicon2turtle))
                break


def main(args=None):    
    rclpy.init(args=args)
    node = sub_tf()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()