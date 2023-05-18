import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf2_msgs.msg import TFMessage
from rclpy.qos import QoSProfile



class StaticTF(Node):

    def __init__(self) -> None:
        super().__init__("static_tf")

        self._tf_broadcaster = TransformBroadcaster(self)

        self.pub_tf = self.create_publisher(TFMessage, "tf_test", QoSProfile(depth=100))

        self.A_tf_timer = self.create_timer(1/30, self.A_tf_callback)
        # self.B_tf_timer = self.create_timer(0.033, self.B_tf_callback)
        # self.C_tf_timer = self.create_timer(0.033, self.C_tf_callback)

    def sendTransform(self, transform):
        """
        Send a transform, or a list of transforms, to the Buffer associated with this TransformBroadcaster.

        :param transform: A transform or list of transforms to send.
        """
        if not isinstance(transform, list):
            if hasattr(transform, '__iter__'):
                transform = list(transform)
            else:
                transform = [transform]
        self.pub_tf.publish(TFMessage(transforms=transform))




    def A_tf_callback(self) -> None:

        tfA = TransformStamped()
        tfA.header.stamp = self.get_clock().now().to_msg()
        tfA.header.frame_id = "vicon"
        tfA.child_frame_id = "A"
        tfA.transform.translation.x = 0.0
        tfA.transform.translation.y = -1.0
        tfA.transform.translation.z = 0.0
        tfA.transform.rotation.x = 0.0
        tfA.transform.rotation.y = 0.0
        tfA.transform.rotation.z = 0.0
        tfA.transform.rotation.w = 1.0

        # self._tf_broadcaster.sendTransform(tfA,)
        
    # def B_tf_callback(self) -> None:

        tfB = TransformStamped()
        tfB.header.stamp = self.get_clock().now().to_msg()
        tfB.header.frame_id = "A"
        tfB.child_frame_id = "B"
        tfB.transform.translation.x = 0.1
        tfB.transform.translation.y = 1.0
        tfB.transform.translation.z = 1.0
        tfB.transform.rotation.x = 0.0
        tfB.transform.rotation.y = 0.0
        tfB.transform.rotation.z = 0.0
        tfB.transform.rotation.w = 1.0

        # self._tf_broadcaster.sendTransform(tfB)

    # def C_tf_callback(self) -> None:

        tfC = TransformStamped()
        tfC.header.stamp = self.get_clock().now().to_msg()
        tfC.header.frame_id = "B"
        tfC.child_frame_id = "C"
        tfC.transform.translation.x = 0.1
        tfC.transform.translation.y = 1.0
        tfC.transform.translation.z = -1.0
        tfC.transform.rotation.x = 0.0
        tfC.transform.rotation.y = 0.0
        tfC.transform.rotation.z = 0.0
        tfC.transform.rotation.w = 1.0

        self.sendTransform([tfA, tfB, tfC])



        # tfVicon = TransformStamped()
        # tfVicon.header.stamp = self.get_clock().now().to_msg()
        # tfVicon.header.frame_id = "vicon"
        # tfVicon.child_frame_id = "vicon"
        # tfVicon.transform.translation.x = 0.4
        # tfVicon.transform.translation.y = 0.0
        # tfVicon.transform.translation.z = 0.0
        # tfVicon.transform.rotation.x = 0.0
        # tfVicon.transform.rotation.y = 0.0
        # tfVicon.transform.rotation.z = 0.0
        # tfVicon.transform.rotation.w = 1.0



        # self._tf_broadcaster.sendTransform(tfVicon)





def main(args=None):
    rclpy.init(args=args)

    static_tf = StaticTF()

    rclpy.spin(static_tf)

    static_tf.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()