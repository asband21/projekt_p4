import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticTF(Node):

    def __init__(self) -> None:
        super().__init__("static_tf")

        self._tf_broadcaster = TransformBroadcaster(self)


        self._tf_timer = self.create_timer(0.1, self._tf_callback)

    def _tf_callback(self) -> None:

        tfA = TransformStamped()
        tfA.header.stamp = self.get_clock().now().to_msg()
        tfA.header.frame_id = "world"
        tfA.child_frame_id = "A"
        tfA.transform.translation.x = 1.0
        tfA.transform.translation.y = 0.0
        tfA.transform.translation.z = 0.0
        tfA.transform.rotation.x = 0.0
        tfA.transform.rotation.y = 0.0
        tfA.transform.rotation.z = 0.0
        tfA.transform.rotation.w = 1.0

        self._tf_broadcaster.sendTransform(tfA)
        

        tfB = TransformStamped()
        tfB.header.stamp = self.get_clock().now().to_msg()
        tfB.header.frame_id = "A"
        tfB.child_frame_id = "B"
        tfB.transform.translation.x = 1.0
        tfB.transform.translation.y = 0.0
        tfB.transform.translation.z = 0.0
        tfB.transform.rotation.x = 0.0
        tfB.transform.rotation.y = 0.0
        tfB.transform.rotation.z = 0.0
        tfB.transform.rotation.w = 1.0

        self._tf_broadcaster.sendTransform(tfB)

        tfC = TransformStamped()
        tfC.header.stamp = self.get_clock().now().to_msg()
        tfC.header.frame_id = "B"
        tfC.child_frame_id = "C"
        tfC.transform.translation.x = 1.0
        tfC.transform.translation.y = 0.0
        tfC.transform.translation.z = 0.0
        tfC.transform.rotation.x = 0.0
        tfC.transform.rotation.y = 0.0
        tfC.transform.rotation.z = 0.0
        tfC.transform.rotation.w = 1.0

        self._tf_broadcaster.sendTransform(tfC)




def main(args=None):
    rclpy.init(args=args)

    static_tf = StaticTF()

    rclpy.spin(static_tf)

    static_tf.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()