import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty

from personal_interface.srv import StateChanger
import time


class turtle_follower(Node):
    def __init__(self):
        super().__init__("turtle_follower") 

        self.tarck_length = 5
        self.state = "idle"
        self.meters_driven = 0

        self.sub_node_turtle_follower = rclpy.create_node("sub_node_turtle_follower")

        self.sub_cli_analisys = self.sub_node_turtle_follower.create_client(Empty,"calculate_target_pose")
        self.srv_state_changer = self.create_service(StateChanger,"state_changer",self.state_changer_callback)

        self.state_controller()


    def state_changer_callback(self,request,response):
        self.state = request.state
        if self.state == "continue":
            response.success = True
        else:
            response.success = False
                    
        return response


    def send_request(self,request):
        while not self.sub_cli_analisys.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        future = self.sub_cli_analisys.call_async(request)
        rclpy.spin_until_future_complete(self.sub_node_turtle_follower,future)
        return future.result()



    def turn(self, turn_way):

        if turn_way == "left":
            deleteme = int
            # turn left 90 degrees
        elif turn_way == "right":
            deleteme = int
            # turn right 180 degrees



    def drive_stright(self):
        deleteme = int
        # drive 1 meter

    def state_controller(self):

        while True:

            if self.meters_driven > self.tarck_length:
                break

            # drive 1 meter 
            self.drive_stright()

            self.meters_driven += 1
            # turn left 90 degrees
            self.turn("left")

            # send request to image analisys

            while True:
                if self.state == "continue":
                    break
                time.sleep(1/30)

            # turn right 180 degrees
            self.turn("right")


            # send request to image analisys
            

            while True:
                if self.state == "continue":
                    break
                time.sleep(1/30)
        
            # turn left 90 degrees
            self.turn("left")






def main(args=None):
    rclpy.init(args=args)

    node = turtle_follower()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()


