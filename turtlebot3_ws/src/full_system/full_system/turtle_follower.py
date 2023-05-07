import rclpy
from rclpy.node import Node

from std_srvs.srv import Empty

from personal_interface.srv import StateChanger


class turtle_follower(Node):
    def __init__(self):
        super().__init__("turtle_follower") 

        self.state = "idle"
        self.looking = "none"
        self.meters_driven = 0

        self.sub_node_turtle_follower = rclpy.create_node("sub_node_turtle_follower")

        self.sub_cli_analisys = self.sub_node_turtle_follower.create_client(Empty,"calculate_target_pose")
        self.srv_state_changer = self.create_service(StateChanger,"state_changer",self.state_changer_callback)

        self.turtle_follower()


    def state_changer_callback(self,request,response):

        self.state = request.state
        if self.state == "idle" and self.looking == "left":
            self.state = "turn_right_180"
        elif self.state == "idle" and self.looking == "right":
            self.state = "turn_left_90_again"

        response.success = True
        return response


    def send_request(self,request):
        while not self.sub_cli_analisys.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        future = self.sub_cli_analisys.call_async(request)
        rclpy.spin_until_future_complete(self.sub_node_turtle_follower,future)
        return future.result()




    def turtle_follower(self):
        req = Empty.Request()
        self.send_request(req)
        return

    def state_controller(self):

        while True:        
            if self.state == "idle":
                continue
            elif self.meters_driven > 5:
                self.get_logger().info("turtle_follower: I have driven 5 meters, I am done")
                break
            
            elif self.state == "drive_stright":
                # turtle script to drive stright 1 meter

                self.state = "turn_left_90"
                self.meters_driven += 1
            
            elif self.state == "turn_left_90":
                # turtle script to turn left 90 degrees


                req = Empty.Request()
                self.send_request(req)
                self.state = "idle"
                self.looking = "left"
            
            elif self.state == "turn_right_180":
                # turtle script to turn right 180 degrees

                self.state = "idle"
                self.looking = "right"

            elif self.state == "turn_left_90_again":
                # turtle script to turn left 90 degrees

                self.state = "drive_stright"

        



def main(args=None):
    rclpy.init(args=args)

    node = turtle_follower()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()


