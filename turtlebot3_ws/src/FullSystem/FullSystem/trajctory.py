import rclpy
from rclpy.node import Node

import numpy as np

from std_srvs.srv import Empty
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


from OwnSrvAndMsg import TargetPose, TakePicture, ContinuePath

import time

import tf_transformations as tf


tf.quaternion_matrix()







class trajectory(Node):
    def __init__(self):
        super().__init__("trajectory") 
        self.targetPose = self.create_service(TargetPose, 'target_pose', self.FindAtoB)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)


    def trajectory(self,t, pos_q0, pos_qf):


        G = np.zeros((4,4))
        B = np.zeros((4,1))
        x = np.zeros((4,1))


        t0 = t[0]
        tf = t[1]

        G[0, 0] = 1
        G[0, 1] = t0
        G[0, 2] = np.power(t0,2)
        G[0, 3] = np.power(t0,3)

        G[1, 0] = 0
        G[1, 1] = 1
        G[1, 2] = np.multiply(2,t0)
        G[1, 3] = np.multiply(3, np.power(t0,2))

        G[2, 0] = 1
        G[2, 1] = tf
        G[2, 2] = np.power(tf,2)
        G[2, 3] = np.power(tf,3)

        G[3, 0] = 0
        G[3, 1] = 1
        G[3, 2] = np.multiply(2,tf)
        G[3, 3] = np.multiply(3, np.power(tf,2))


        B[0, 0] = pos_q0
        B[1, 0] = 0
        B[2, 0] = pos_qf
        B[3, 0] = 0

        X_inv = np.linalg.inv(G)
        result = X_inv.dot(B)

        return result

    def AxisTrajectory(self, A, B):
        t = np.zeros((2,1))
        t[0] = 0
        t[1] = 1

        while True:
            axis = np.zeros((4,1))
            axis[0] = self.trajectory(t, A[0], B[0])
            axis[1] = self.trajectory(t, A[1], B[1])
            axis[2] = self.trajectory(t, A[2], B[2])
            axis[3] = self.trajectory(t, A[3], B[3])

            axis_max = np.zeros((4,1))
            axis_max[0]=-axis[0,2]/(2*axis[0,3])
            axis_max[1]=-axis[1,2]/(2*axis[1,3])
            axis_max[2]=-axis[2,2]/(2*axis[2,3])
            axis_max[3]=-axis[3,2]/(2*axis[3,3])

            if axis_max.any > 0.9:
                t[1] += 0.5
            else:
                break

        return axis

    def pos(self, dt, axis):

        pos_x = axis[0,0] + axis[0,1]*dt + axis[0,2]*np.power(dt,2) + axis[0,3]*np.power(dt,3)
        pos_y = axis[1,0] + axis[1,1]*dt + axis[1,2]*np.power(dt,2) + axis[1,3]*np.power(dt,3)
        pos_z = axis[2,0] + axis[2,1]*dt + axis[2,2]*np.power(dt,2) + axis[2,3]*np.power(dt,3)
        yaw_z = axis[3,0] + axis[3,1]*dt + axis[3,2]*np.power(dt,2) + axis[3,3]*np.power(dt,3)

        pose = np.zeros((4,1))
        pose[0] = pos_x
        pose[1] = pos_y
        pose[2] = pos_z
        pose[3] = yaw_z



    def oariantationDifference(self, q1, q2):
        
        q1.orientation.x
        q1.orientation.y
        q1.orientation.z
        q1.orientation.w

        q2.target_pose.pose.orientation.x
        q2.target_pose.pose.orientation.y
        q2.target_pose.pose.orientation.z
        q2.target_pose.pose.orientation.w



    def FindAtoB(self,request,response):
        telloTransform = self.tf_buffer.lookup_transform('tello','world')
        
        x_drone = telloTransform.position.x 
        y_drone = telloTransform.position.y
        z_drone = telloTransform.position.z

        x_target = request.target_pose.pose.position.x
        y_target = request.target_pose.pose.position.y
        z_target = request.target_pose.pose.position.z



        





    start_time = rclpy.time.time()

    while rclpy.time.time() - start_time < 5.0:

        dt = rclpy.time.time() - start_time
        pos = pos(dt)

        self.pub.publish(pos)

        time.sleep(1/30)


        

