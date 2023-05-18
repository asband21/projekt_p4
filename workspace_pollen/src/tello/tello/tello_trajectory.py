import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

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
        # vis.add("point",[0,0,0])
        # vis.animate("point",traj_timed)
        # vis.add("traj_timed",traj_timed)
        # vis.spin(float('inf'))   #show the window until you close it


    
        return traj_timed

class tello_trajectory(Node):

    def __init__(self):
        super().__init__('tello_trajectory')

        #rclpy.time.Duration(seconds=1.0)
        # self._tf_buffer = Buffer( )
        # self._tf_listener = TransformListener(self._tf_buffer, self)
        # self._tf_broadcaster = TransformBroadcaster(self)

        self.create_client(String, 'takeoff')
        

        self.pub_velocities = self.create_publisher(Twist, 'control', 1)
        self.pub_takeoff = self.create_publisher(String, 'takeoff', 1)
        self.pub_land = self.create_publisher(String, 'land', 1)
        self.sub_tf = self.create_subscription(TFMessage, 'tf_test', self.tf_callback, 10)

        self.pub_trajectory = self.create_publisher(Twist, 'trajectory', 1)

        self.create_service(String, 'takeoff', )
        self.create_timer(2, self.timer_callback)

        self.viconTransform = TransformStamped()
        self.viconTransform.header.stamp = builtin_interfaces.msg.Time(sec=0, nanosec=0)

        self.stop = False




    def tf_callback(self, msg):
        '''Callback function for the tf message.
        It just saves the curent transform of a desired path'''
        self.transform = msg.transforms


    def timer_callback(self):
        if self.stop == True:
            return

        try:


            self.pub_takeoff.publish(String(data="takeoff"))

            # tfDesired = TransformStamped()


            traject = computeTrajectory(self.transform, 0.9, 3)

            
            
            for i in range(len(traject.milestones)):
                if i == 0:
                    pt = 0
                else:
                    pt = traject.times[i-1]

                ct = traject.times[i]
                # print("ct",ct)

                
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

                print("vel",vel)
                # self.tello.send_rc_control(int(vel[0]*100), int(vel[1]*100), int(vel[2]*100), 0)
                self.pub_velocities.publish(vel)

                # tfDesired.header.stamp = self.get_clock().now().to_msg()
                # tfDesired.header.frame_id = "vicon"
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
            # self.tello.land()
            self.pub_land.publish(String(data="land"))

        except Exception as e:
            print(e)
            pass



        

    



def main(args=None):
    rclpy.init(args=args)

    tellotrajectory = tello_trajectory()

    rclpy.spin(tellotrajectory)

    tellotrajectory.destroy_node()


    rclpy.shutdown()


if __name__ == '__main__':
    main()




