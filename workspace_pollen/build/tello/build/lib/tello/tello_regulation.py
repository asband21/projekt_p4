

from rclpy.node import Node

from geometry_msgs.msg import Twist



class tello_regulation(Node):

    def __init__(self) -> None:
        super().__init__("tello_regulation")

        self.create_subscription(Twist, 'trajectory', self.velocity_callback, 1)


    def velocity_callback(self, msg):
        self.velocity = msg
        lin_x = self.velocity.linear.x
        lin_y = self.velocity.linear.y
        lin_z = self.velocity.linear.z
        ang_z = self.velocity.angular.z


    # def stabeliser(self,msg):
        
    #     # if the self.viconTransform is within 0.01 of the msg.transform.header.stamp then return.
    #     # if 0.01 < abs(self.viconTransform.header.stamp- msg.header.stamp):
    #     #     return

        
    #     time = self.get_clock().now().to_msg()
    #     vel = [msg.transform.translation.x,msg.transform.translation.y,msg.transform.translation.z]

    #     lookuptransform = self._tf_buffer.lookup_transform('desired_pose', 'vicon',0,Duration(seconds=0, nanoseconds=1))

    #     print("lookuptransform",lookuptransform)
    #     a = 0.05

    #     kx = a * lookuptransform.translation.x - 0.01
    #     ky = a * lookuptransform.translation.y - 0.01
    #     kz = a * lookuptransform.translation.z - 0.01

    #     if [kx,ky,kz] > [0,0,0]:
    #         vel[0] = vel[0] + 0.1*kx
    #         vel[1] = vel[1] + 0.1*ky
    #         vel[2] = vel[2] + 0.1*kz

    #     print("vel",vel)
    #     self.tello.send_rc_control(int(vel[0]*100), int(vel[1]*100), int(vel[2]*100), 0)


