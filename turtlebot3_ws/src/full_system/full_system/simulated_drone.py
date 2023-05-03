import rclpy
from rclpy.node import Node


from geometry_msgs.msg import Twist


from djitellopy import Tello


from personal_interface.srv import TakePicture

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__("simulated_drone") 


        self.drone = Tello()

        self.drone.connect()

        self.create_service(TakePicture,"take_picture",self.take_picture)

        self.create_subscription(Twist,"drone_rc",self.callback)





    def take_picture(self, request, response):
        
        response