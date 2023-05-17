import rclpy
from rclpy.node import Node



from tf2_ros.transform_broadcaster import TransformBroadcaster

from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Header


from personal_interface.srv import TargetPose

class SimulatedVicon(Node):
    def __init__(self):
        super().__init__("simulated_vicon") 


        self.tf_broadcaster = TransformBroadcaster(self)
        self.pub = self.create_publisher(TransformStamped,"update",10)

        hz=1/30
        self.create_timer(hz,self.drone_pose)
        self.create_timer(hz,self.turtle_pose)
        self.create_timer(hz,self.update)


    def update(self):
        update = TransformStamped()
        
        self.pub.publish(update)


    def drone_pose(self):
        drone = TransformStamped()
        head = Header()
        head.frame_id = "vicon"
        head.stamp = self.get_clock().now().to_msg()

        drone.header = head
        drone.child_frame_id = "drone"

        drone.transform.translation.x = 1.0
        drone.transform.translation.y = 0.0
        drone.transform.translation.z = 2.0

        drone.transform.rotation.x = 0.0
        drone.transform.rotation.y = 0.0
        drone.transform.rotation.z = 0.0
        drone.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(drone)


    def turtle_pose(self):
        turtle = TransformStamped()

        head = Header()
        head.frame_id = "vicon"
        head.stamp = self.get_clock().now().to_msg()

        turtle.header = head
        turtle.child_frame_id = "turtle"

        turtle.transform.translation.x = 3.0
        turtle.transform.translation.y = 0.0
        turtle.transform.translation.z = 1.0

        turtle.transform.rotation.x = 0.0
        turtle.transform.rotation.y = 0.0
        turtle.transform.rotation.z = 0.0
        turtle.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(turtle)

    


        

def main(args=None):
    rclpy.init(args=args)

    node = SimulatedVicon()
        
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()


