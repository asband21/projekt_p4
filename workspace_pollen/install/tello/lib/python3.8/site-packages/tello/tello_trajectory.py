import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Empty
from geometry_msgs.msg import Twist 
import numpy as np
import math
import time
from djitellopy import Tello
import tf2_ros as tf2

# make a class that will get input tf2 transform and compute the transformation matrix


# this class will compute the cubic trajectory for each of the 3 directions (x, y, z)
# input is a tf2 transform from the base_link to the end effector (this is the desired trajectory)
# there should be made a object of each tf2 transform, where a desired_frame is found and then find the tf2 frames between the desired_frame and the base_link

# output is a twist message that will be published to the control topic

# make an if statment that can see what time it is and then say what trajectory that should be looked at







class trajectory():

    def computeCubicCoeff(self, t0, tf, pos_q0, vec_q0, pos_qf, vec_qf):
        X = np.zeros((4, 4))
        B = np.zeros((4, 1))

        X[0, 0] = 1
        X[0, 1] = t0
        X[0, 2] = np.power(t0, 2)
        X[0, 3] = np.power(t0, 3)

        X[1, 0] = 0
        X[1, 1] = 1
        X[1, 2] = 2 * t0
        X[1, 3] = 3 * np.power(t0, 2)

        X[2, 0] = 1
        X[2, 1] = tf
        X[2, 2] = np.power(tf, 2)
        X[2, 3] = np.power(tf, 3)

        X[3, 0] = 0
        X[3, 1] = 1
        X[3, 2] = 2 * tf
        X[3, 3] = 3 * np.power(tf, 2)

        B[0, 0] = pos_q0
        B[1, 0] = vec_q0
        B[2, 0] = pos_qf
        B[3, 0] = vec_qf

        return np.dot(np.linalg.inv(X), B)
    

    def computeCubicTrajectory(self, t, t0, tf, pos_q0, vec_q0, pos_qf, vec_qf):
        # if the trajectory is not defined, return 0
        if pos_q0 == pos_qf and vec_q0 == vec_qf:
            return 0.0

        # if the trajectory is defined, compute the coefficients
        coeff = self.computeCubicCoeff(t0, tf, pos_q0, vec_q0, pos_qf, vec_qf)
        # q[i] = coeff[0] + coeff[1] * t[i] + coeff[2] * np.power(t[i], 2) + coeff[3] * np.power(t[i], 3) # this computes position
        # differtiate to get velocity
        q = coeff[1] + 2 * coeff[2] * t + 3 * coeff[3] * np.power(t, 2)

        return q

  


class tello_trajectory(Node):

    def __init__(self):
        super().__init__('tello_trajectory')

        self.trajectory_time=1

        self.publisher_control = self.create_publisher(Twist, 'control', 10)
        self.publisher_takeoff = self.create_publisher(Empty, 'takeoff', 1)
        self.publisher_land = self.create_publisher(Empty, 'land', 1)

        
        # make a variable that can hold an float
        self.current_time = 0.0

        self.timer_callback()


        

    # create a function that knows the current time in seconds
    def get_time(self):
        return time.time()


    def timer_callback(self):
        tello = Tello()

        tello.connect()
        # create a message of type Twist
        msg = Twist()
        
        # create a message of type Empty to publish to the takeoff and land topics
        empty = Empty()
        i=0
        while i <1:
            # self.publisher_takeoff.publish(empty)
            tello.takeoff()
            time.sleep(0.1)
            i +=1
            print(i)
        time.sleep(3)

        # make a vector for end effector position and velocity
        pos_q0 = [0, 0, 0]
        vec_q0 = [0, 0, 0]
        pos_qf = [0, 200, 100]
        vec_qf = [0, 0, 0]

        xdir = trajectory()
        ydir = trajectory()
        zdir = trajectory()

        msg.linear.x = float(xdir.computeCubicTrajectory(0,0, self.trajectory_time, pos_q0[0], vec_q0[0], pos_qf[0], vec_qf[0]))
        msg.linear.y = float(ydir.computeCubicTrajectory(0,0, self.trajectory_time, pos_q0[1], vec_q0[1], pos_qf[1], vec_qf[1]))
        msg.linear.z = float(zdir.computeCubicTrajectory(0,0, self.trajectory_time, pos_q0[2], vec_q0[2], pos_qf[2], vec_qf[2]))


            
        threshold = 50
        t = 0
        # while any of the linear velocities are greater or lower than threshold, add one seocond to the trajectory time and recompute the trajectory
        while t <= self.trajectory_time:
            msg.linear.x = float(xdir.computeCubicTrajectory(t,0, self.trajectory_time, pos_q0[0], vec_q0[0], pos_qf[0], vec_qf[0]))
            msg.linear.y = float(ydir.computeCubicTrajectory(t,0, self.trajectory_time, pos_q0[1], vec_q0[1], pos_qf[1], vec_qf[1]))
            msg.linear.z = float(zdir.computeCubicTrajectory(t,0, self.trajectory_time, pos_q0[2], vec_q0[2], pos_qf[2], vec_qf[2]))
            t += 0.1
            
            if msg.linear.x > threshold or msg.linear.x < -threshold or msg.linear.y > threshold or msg.linear.y < -threshold or msg.linear.z > threshold or msg.linear.z < -threshold:
                self.trajectory_time += 1
                t = 0
            self.current_time = self.get_time()

  


        i = 0
        # puplish the message to the control topic every nanosecond until the trajectory time is reached 
        while  self.get_time()- self.current_time <= self.trajectory_time:
            #print(self.get_time()-self.current_time)
            msg.linear.x = float(xdir.computeCubicTrajectory(self.get_time()-self.current_time,0, self.trajectory_time, pos_q0[0], vec_q0[0], pos_qf[0], vec_qf[0]))
            msg.linear.y = float(ydir.computeCubicTrajectory(self.get_time()-self.current_time,0, self.trajectory_time, pos_q0[1], vec_q0[1], pos_qf[1], vec_qf[1]))
            msg.linear.z = float(zdir.computeCubicTrajectory(self.get_time()-self.current_time,0, self.trajectory_time, pos_q0[2], vec_q0[2], pos_qf[2], vec_qf[2]))
            i += 0.001
            #print(self.trajectory_time)
            # print(msg.linear.x, msg.linear.y, msg.linear.z)
            # self.publisher_control.publish(msg)
            tello.send_rc_control(int(msg.linear.x), int(msg.linear.y), int(msg.linear.z), 0)
        

        # send a message of 0 velocity to the drone to stop it
        msg.linear.x = float(0.0)
        msg.linear.y = float(0.0)
        msg.linear.z = float(0.0)
        for i in range(10):
            # self.publisher_control.publish(msg)
            tello.send_rc_control(int(msg.linear.x), int(msg.linear.y), int(msg.linear.z), 0)
            print(msg.linear.x, msg.linear.y, msg.linear.z)


        time.sleep(5)
        # send the land command to the drone
        i= 0
        while i <1:
            tello.land()
            self.publisher_land.publish(empty)
            i+=1





        self.get_time()
        




def main(args=None):
    rclpy.init(args=args)

    tellotrajectory = tello_trajectory()

    rclpy.spin(tellotrajectory)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tellotrajectory.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()