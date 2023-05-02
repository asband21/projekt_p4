import rclpy
from rclpy.node import Node



from tf2_ros.transform_broadcaster import TransformBroadcaster

from geometry_msgs.msg import TransformStamped




class SimulatedVicon(Node):
    def __init__(self):
        super().__init__("simulated_vicon") 


        self.tf_broadcaster = TransformBroadcaster(self)

        hz=1/30
        self.create_timer(hz,self.drone_pose)
        self.create_timer(hz,self.turtle_pose)


    def drone_pose(self):
        drone = TransformStamped()

        drone.header = self.get_clock().now().to_msg()
        drone.header.frame_id = "world"
        drone.child_frame_id = "drone"

        drone.transform.translation.x = 0
        drone.transform.translation.y = 0
        drone.transform.translation.z = 0

        drone.transform.rotation.x = 0
        drone.transform.rotation.y = 0
        drone.transform.rotation.z = 0
        drone.transform.rotation.w = 1

        self.tf_broadcaster.sendTransform(drone)


    def turtle_pose(self):
        turtle = TransformStamped()

        turtle.header = self.get_clock().now().to_msg()
        turtle.header.frame_id = "world"
        turtle.child_frame_id = "turtle"

        turtle.transform.translation.x = 0
        turtle.transform.translation.y = 0
        turtle.transform.translation.z = 0

        turtle.transform.rotation.x = 0
        turtle.transform.rotation.y = 0
        turtle.transform.rotation.z = 0
        turtle.transform.rotation.w = 1

        self.tf_broadcaster.sendTransform(turtle)
        

def main(args=None):
    rclpy.init(args=args)

    node = SimulatedVicon()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()


