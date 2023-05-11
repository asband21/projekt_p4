import rclpy

from rclpy.node import Node

from personal_interface.srv import StateChanger, TakePicture

import time

class testTurtle(Node):

    def __init__(self):
        super().__init__('test_turtle')
        self.get_logger().info("test_turtle node has been started")

        self.node_turtle_follower = rclpy.create_node('node_turtle_follower')

        self.cli_turtle = self.node_turtle_follower.create_client(StateChanger,"state_changer")

        self.srv_analisys = self.create_service(TakePicture,"calculate_target_pose",self.srv_take_pic)



    def srv_take_pic(self,request,response):
        self.get_logger().info("srv_take_pic has been called")
        time.sleep(5)
        response.success = True
        
        # send_request_result = self.send_request()
        # self.get_logger().info("send_request_result: " + str(send_request_result))

        return response

    def send_request(self):
        while not self.cli_turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        request = StateChanger.Request()
        request.state = "continue"

        future = self.cli_turtle.call_async(request)
        rclpy.spin_until_future_complete(self.node_turtle_follower,future)

        while future.result() == None:
            time.sleep(1/30)
            
        return future.result()




def main(args=None):
    rclpy.init(args=args)

    node = testTurtle()

    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()