import rclpy
from rclpy.node import Node

from tf2_ros import TransformListener

from tf2_ros.buffer import Buffer



class TreeFinder(Node):
    def __init__(self):
        super().__init__('tree_finder')
        self._tf_buffer = Buffer( rclpy.time.Duration(seconds=1.0))
        self._tf_listener = TransformListener(self._tf_buffer, self)
        self._tf_timer = self.create_timer(0.1, self._tf_callback)

    def _tf_callback(self):


        self._tf_listener.tf_sub

def main(args=None):
    rclpy.init(args=args)

    tree_finder = TreeFinder()

    rclpy.spin(tree_finder)

    tree_finder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

