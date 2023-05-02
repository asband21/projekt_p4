import rclpy
from rclpy.node import Node




from djitellopy import Tello


from personal_robotics_interfaces.srv import TakePicture

class SimulatedDrone(Node):
    def __init__(self):
        super().__init__("simulated_drone") 


        self.drone = Tello()

        self.drone.connect()

        self.create_service(TakePicture,"take_picture",self.take_picture)




    def take_picture(self, request, response):
        
        response