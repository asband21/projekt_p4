import rclpy
from rclpy.node import Node


from geometry_msgs.msg import Twist


from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


from djitellopy import Tello

import time

from personal_interface.srv import TakePicture

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__("simulated_drone") 


        # self.drone = Tello()

        # self.drone.connect()

        # self.bridge = CvBridge()
        # self.publisher = self.create_publisher(Image, 'image', 10)
        # self.tello = Tello()

        self.srv_take_picture = self.create_service(TakePicture,"take_picture",self.take_picture)


        self.sub_rc = self.create_subscription(Twist,"drone_rc",self.callback_drone_rc,10)



    # def take_picture(self):
    #     self.tello.connect()
    #     self.tello.streamon()
    #     image = self.tello.get_frame_read().frame
    #     self.tello.streamoff()
    #     msg = self.bridge.cv2_to_imgmsg(image, 'bgr8')
    #     self.publisher.publish(msg)







    def callback_drone_rc(self, msg):

        self.drone.send_rc_control(msg.linear.x, msg.linear.y, msg.linear.z, msg.angular.z)






    def take_picture(self, request, response):
        
        


        


        response.success = True

        time.sleep(5)

        return response
    

def main(args=None):
    rclpy.init(args=args)

    node = SimulatedDrone()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()