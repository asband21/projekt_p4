# generate a python script that makes a function return data within a set time limit with a ferquncy of 30hz

# from roboticstoolbox.tools.trajectory import mstraj
# import numpy as np
# from klampt.io import 

# viapoints = np.array([[0,0,0],[1,1,1],[2,2,2]])

# f= mstraj(viapoints, 1/30,0.01,0.5)

# for i in range(len(f.q)):
#     print(f.q[i])

# from klampt.model import trajectory

# milestones = [[0,0,0],[.5,.5,.5],[.2,.2,0]]

# traj = trajectory.Trajectory(milestones=milestones)

# from klampt import vis

# vis.add("point",[0,0,0])
# # vis.animate("point",traj)
# # vis.add("traj",traj)
# # vis.spin(float('inf'))   #show the window until you close it



# traj2 = trajectory.HermiteTrajectory()
# traj2.makeSpline(traj)

# # vis.animate("point",traj2)
# # vis.add("traj2",traj2)
# # vis.spin(float('inf'))




# traj_timed = trajectory.path_to_trajectory(traj,vmax=0.5,amax=0.5)

# print("q",traj_timed.eval(0.5))
# print("dq",traj_timed.deriv(0.5))

# #next, try this line instead
# #traj_timed = trajectory.path_to_trajectory(traj,timing='sqrt-L2',speed='limited',vmax=2,amax=4)
# #or this line
# #traj_timed = trajectory.path_to_trajectory(traj2.discretize(0.1),timing='sqrt-L2',speed=0.3)
# vis.animate("point",traj_timed)
# vis.spin(float('inf'))



# via_points = [[0,0,0]]*3
# print(via_points)
from klampt.model import trajectory

# milestones = [[0,0,0],[0.02,0,0],[1,0,0],[2,0,1],[2.2,0,1.5],[3,0,1],[4,0,-0.3]]
milestones = [[0,0,0],[0,-0.9,0],[0,0,1],[0,1,0]]

traj = trajectory.Trajectory(milestones=milestones)


#prints milestones 0-5
print(0,":",traj.eval(0))
print(1,":",traj.eval(1))
print(2,":",traj.eval(2))
print(3,":",traj.eval(3))
print(4,":",traj.eval(4))
print(5,":",traj.eval(5))
print(6,":",traj.eval(6))
#print some interpolated points
print(0.5,":",traj.eval(0.5))
print(2.5,":",traj.eval(2.5))
#print some stuff after the end of trajectory
print(7,":",traj.eval(7))
print(100.3,":",traj.eval(100.3))
print(-2,":",traj.eval(-2))




from klampt import vis

vis.add("point",[0,0,0])
# vis.animate("point",traj)
# vis.add("traj",traj)
# vis.spin(float('inf'))   #show the window until you close it





traj2 = trajectory.HermiteTrajectory()
traj2.makeSpline(traj)

vis.animate("point",traj2)
vis.add("traj2",traj2)
vis.spin(float('inf'))




# traj_timed = trajectory.path_to_trajectory(traj,vmax=2,amax=4)
#next, try this line instead
traj_timed = trajectory.path_to_trajectory(traj,velocities='minimum-jerk',endvel=0,startvel=0,speed='limited',vmax=0.3,amax=0.3)
#or this line
#traj_timed = trajectory.path_to_trajectory(traj2.discretize(0.1),timing='sqrt-L2',speed=0.3)
vis.animate("point",traj_timed)
vis.spin(float('inf'))

import time
from klampt.math import vectorops

for i in range(len(traj_timed.milestones)):
        if i == 0:
            pt = 0
        else:
            pt = traj_timed.times[i-1]

        ct = traj_timed.times[i]
        print("ct",ct)

        vel2 = vectorops.sub(traj_timed.milestones[i+1],traj_timed.milestones[i])
        # vel = traj_timed.deriv(ct,'loop')
        # print("vel",vel)
        if i == 0:
            print("vel2",[vel2[0],vel2[1],vel2[2]])
        else:
            print("vel2",[vel2[0]/(ct-pt),vel2[1]/(ct-pt),vel2[2]/(ct-pt)])
        time.sleep(ct-pt)






