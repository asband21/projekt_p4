import rclpy
from rclpy.node import Node

from tf2_ros import TransformListener

import builtin_interfaces.msg
from rclpy.duration import Duration

from std_msgs.msg import String, Empty
from geometry_msgs.msg import Twist 
import time
from djitellopy import Tello
from tf2_msgs.msg import TFMessage

from geometry_msgs.msg import TransformStamped

from tf2_ros.buffer import Buffer

from klampt.math import vectorops
from tf2_ros import TransformBroadcaster

from klampt.model import trajectory as KTrajectory

def computeViapoints(transforms):

    via_points = []
    for i in range(len(transforms)+1):
        via_points.append([0,0,0])


    for i in range(len(transforms)):
        if i == 0:
            via_points[i+1][0] = transforms[i].transform.translation.x
            via_points[i+1][1] = transforms[i].transform.translation.y
            via_points[i+1][2] = transforms[i].transform.translation.z

        else:
            via_points[i+1][0]  = via_points[i][0] + transforms[i].transform.translation.x 
            via_points[i+1][1]  = via_points[i][1] + transforms[i].transform.translation.y 
            via_points[i+1][2]  = via_points[i][2] + transforms[i].transform.translation.z 

    return via_points


from klampt import vis


def computeTrajectory(transforms, vmax , amax):
    
        via_points = computeViapoints(transforms)
        # via_points = [[0,0,0],[.5,.5,.5],[.2,.2,0]]
        print("via_points",via_points)
        traj = KTrajectory.Trajectory(milestones=via_points)

        traj_timed = KTrajectory.path_to_trajectory(traj,velocities='minimum-jerk',vmax=vmax,amax=amax,dt=1/30)
        vis.add("point",[0,0,0])
        vis.animate("point",traj_timed)
        vis.add("traj_timed",traj_timed)
        vis.spin(float('inf'))   #show the window until you close it


    
        return traj_timed

class tello_trajectory(Node):

    def __init__(self):
        super().__init__('tello_trajectory')

        #rclpy.time.Duration(seconds=1.0)
        # self._tf_buffer = Buffer( )
        # self._tf_listener = TransformListener(self._tf_buffer, self)


        # self._tf_broadcaster = TransformBroadcaster(self)
        # self.pub_velocities = self.create_publisher(TransformStamped, 'velocites', 1)
        # self.pub_takeoff = self.create_publisher(Empty, 'takeoff', 1)
        # self.pub_land = self.create_publisher(Empty, 'land', 1)
        self.sub_tf = self.create_subscription(TFMessage, 'tf_test', self.tf_callback, 10)
        # self.sub_velocites = self.create_subscription(TransformStamped,'velocites',self.stabeliser,1)


        self.create_timer(6, self.timer_callback)
        self.start = time.time()
        self.tello = Tello()

        self.viconTransform = TransformStamped()
        self.viconTransform.header.stamp = builtin_interfaces.msg.Time(sec=0, nanosec=0)

        self.stop = False
        # tello.connect()




    def tf_callback(self, msg):
        '''Callback function for the tf message.
        It just saves the curent transform of a desired path'''
        self.transform = msg.transforms


    def timer_callback(self):
        # if self.transform is None:
            # print("No transform recieved")
            # return
        if self.stop == True:
            return

        try:

            # self.end = time.time()
            # print("Time to call funciton: ", self.end - self.start)

            # tello.takeoff()

            # tfDesired = TransformStamped()
            # velocities = TransformStamped()


            # start = time.time()
            traject = computeTrajectory(self.transform, 0.7, 0.7)
            # end = time.time()
            # print("Time to compute trajectory: ", end - start)

            
            # start = time.time()
            # while time.time() - start < traject.duration():
            #     t = time.time() - start
            #     vel = traject.deriv(t)
            #     self.tello.send_rc_control(int(vel[0]*100), int(vel[1]*100), int(vel[2]*100), 0)
            #     time.sleep(1/30)
            
            for i in range(len(traject.milestones)):
                if i == 0:
                    pt = 0
                else:
                    pt = traject.times[i-1]

                ct = traject.times[i]
                # print("ct",ct)
                # vel = traject.deriv(ct,'loop')
                # pos = traject.milestones[i]
                if i == len(traject.milestones)-1:
                    dpos = vectorops.sub(traject.milestones[i],traject.milestones[i])
                else:
                    dpos = vectorops.sub(traject.milestones[i+1],traject.milestones[i])
                if i == 0:
                    vel = [dpos[0],dpos[1],dpos[2]]
                else:
                    vel = [dpos[0]/(ct-pt),dpos[1]/(ct-pt),dpos[2]/(ct-pt)]

                # print("vel",vel)
                # velocities.header.stamp = self.get_clock().now().to_msg()
                # velocities.transform.translation.x = vel[0]
                # velocities.transform.translation.y = vel[1]
                # velocities.transform.translation.z = vel[2]


                self.tello.send_rc_control(int(vel[0]*100), int(vel[1]*100), int(vel[2]*100), 0)
                # self.pub_velocities.publish(velocities)

                # tfDesired.header.stamp = self.get_clock().now().to_msg()
                # tfDesired.header.frame_id = "world"
                # tfDesired.child_frame_id = "desired_pose"
                # tfDesired.transform.translation.x = float(pos[0])
                # tfDesired.transform.translation.y = float(pos[1])
                # tfDesired.transform.translation.z = float(pos[2])
                # tfDesired.transform.rotation.x = 0.0
                # tfDesired.transform.rotation.y = 0.0
                # tfDesired.transform.rotation.z = 0.0
                # tfDesired.transform.rotation.w = 1.0

                # self._tf_broadcaster.sendTransform(tfDesired)
                time.sleep(ct-pt)
                self.stop = True


        except Exception as e:
            print(e)
            pass


    # def vicon(self, msg):
    #     self.viconTransform = msg.transform

    # def stabeliser(self,msg):
        
    #     # if the self.viconTransform is within 0.01 of the msg.transform.header.stamp then return.
    #     # if 0.01 < abs(self.viconTransform.header.stamp- msg.header.stamp):
    #     #     return

        
    #     time = self.get_clock().now().to_msg()
    #     vel = [msg.transform.translation.x,msg.transform.translation.y,msg.transform.translation.z]

    #     lookuptransform = self._tf_buffer.lookup_transform('desired_pose', 'vicon',0,Duration(seconds=0, nanoseconds=1))

    #     print("lookuptransform",lookuptransform)
    #     a = 0.05

    #     kx = a * lookuptransform.translation.x - 0.01
    #     ky = a * lookuptransform.translation.y - 0.01
    #     kz = a * lookuptransform.translation.z - 0.01

    #     if [kx,ky,kz] > [0,0,0]:
    #         vel[0] = vel[0] + 0.1*kx
    #         vel[1] = vel[1] + 0.1*ky
    #         vel[2] = vel[2] + 0.1*kz

    #     print("vel",vel)
    #     self.tello.send_rc_control(int(vel[0]*100), int(vel[1]*100), int(vel[2]*100), 0)


        

    



def main(args=None):
    rclpy.init(args=args)

    tellotrajectory = tello_trajectory()

    rclpy.spin(tellotrajectory)

    tellotrajectory.destroy_node()


    rclpy.shutdown()


if __name__ == '__main__':
    main()




