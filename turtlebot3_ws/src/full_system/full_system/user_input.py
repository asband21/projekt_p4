import rclpy
from rclpy.node import Node




from std_srvs.srv import Empty, SetBool


from personal_interface.srv import StateChanger


class UserInput(Node):
    def __init__(self):
        super().__init__("user_input") 

        self.sub_node_user_input = rclpy.create_node("sub_node_user_input")

        self.cli_drone2turtle = self.sub_node_user_input.create_client(SetBool,"drone2turtle")

        self.cli_turtle_state = self.sub_node_user_input.create_client(StateChanger,"turtle_state")

        self.srv_initiation = self.create_service(Empty,"user_input",self.callback_initiation)



    def send_request(self):
        while not self.cli_drone2turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")

        req = SetBool.Request()
        req.data = True

        future = self.cli_drone2turtle.call_async(req)
        rclpy.spin_until_future_complete(self.sub_node_user_input,future)
        while future.result() == None:
            self.get_logger().info("waiting for response...")
        
        return future.result()

    def change_turtle_state(self):
        while not self.cli_turtle_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        request = StateChanger.Request()
        request.state = "continue"
        future = self.cli_turtle_state.call_async(request)
        rclpy.spin_until_future_complete(self.node_initialization,future)
        while future.result() == None:
            self.get_logger().info("waiting for response...")
        
        return future.result()



    def callback_initiation(self,request,response):
        print("initiation")
        
        user_input = input("All services are up, ready to fly into position? : ")
        
        if user_input == "y":
            # self.send_request()
            self.change_turtle_state()
        elif user_input == "n":
            print("hello")


        return response



def main(args=None):
    rclpy.init(args=args)
    
    node = UserInput()
    
    rclpy.spin(node)
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()