from costom_interface.srv import Velocities
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist



class MinimalService(Node):


    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Velocities, "/srv/Velocities", self.callback)
        self.time  = self.get_clock().now()
        self.get_logger().info(f"time:{self.time}")
        
        self.time_start =self.time.nanoseconds + 1000000000*10

    def step_pos(self):
        #time_nu = self.get_clock().now()
        desired = [3, 5, 6, 3]

        error = [0, 0, 0, 0]
        error[0] = desired[0] - self.position[0]
        error[1] = desired[1] - self.position[1]
        error[2] = desired[2] - self.position[2]
        error[3] = desired[3] - self.position[3]


        return error


        #if(time_nu.nanoseconds < self.time_start):
        #    return [0,0,0,0]
        #else:
        #    return [0,0,0,0]

    def step_vel(self):
        #time_nu = self.get_clock().now()
        desired = [3, 5, 6, 3]

        error = [0, 0, 0, 0]
        error[0] = desired[0] - self.velocity[0]
        error[1] = desired[1] - self.velocity[1]
        error[2] = desired[2] - self.velocity[2]
        error[3] = desired[3] - self.velocity[3]


        return error

        
        #if(time_nu.nanoseconds < self.time_start):
        #    return [0,0,0,0]
        #else:
        #    return [0,0,0,1]
            
    def callback(self, request, respons):

        position = [0,0,0,0]
        position[0] = request.position.linear.x
        position[1] = request.position.linear.y
        position[2] = request.position.linear.z
        position[3] = request.position.angular.z   

        velocity = [0,0,0,0]
        velocity[0] = request.velocity.linear.x
        velocity[1] = request.velocity.linear.y
        velocity[2] = request.velocity.linear.z
        velocity[3] = request.velocity.angular.z    

        print("position : ", position)
        print("velocity : ", velocity)
        
        req_pos = self.step_pos()
        req_vel = self.step_vel()

        #respons = Velocities()
        respons.error_position.linear.x =  float(req_pos[0])
        respons.error_position.linear.y =  float(req_pos[1]) 
        respons.error_position.linear.z =  float(req_pos[2]) 
        respons.error_position.angular.z = float(req_pos[3])    


        respons.error_velocity.linear.x =  float(req_vel[0]) 
        respons.error_velocity.linear.y =  float(req_vel[1]) 
        respons.error_velocity.linear.z =  float(req_vel[2]) 
        respons.error_velocity.angular.z = float(req_vel[3]) 

        print("vel z angle: ", respons.error_velocity.angular.z)

        #respons.error_position.linear.x = req_pos[0] 
        #respons.error_velocity = self.step_vel()
        return respons

    

def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
