





import pickle
import os

import numpy as np
# Read data from pickle file and print it



# Open the pickle file
with open("/home/ubuntu/tests/turtleTest/calibration_turtle2cam.pkl", 'rb') as f:
    data = pickle.load(f)


ids, transforms = data



vicon2turtle = transforms[0]
vicon2ref_object = transforms[1]


# find the inverse of vicont2turtle
turtle2vicon = np.linalg.inv(vicon2turtle)

# find the transform from turtle to ref_object
turtle2ref_object = np.matmul(turtle2vicon, vicon2ref_object)


# find the transform from ref_object to marker. 
ref_object2marker = np.eye(4)
ref_object2marker[0:3,3] = [23.0196, -18.5049, -4.73885] # unit mm: This data is taken from the vicon object list, where you can see the position of the marker to the given object you are looking at.
ref_object2marker[0:3,3] = ref_object2marker[0:3,3]/1000 # change unit mm to m 


# find the transform from turtle to marker
turtle2marker = np.matmul(turtle2ref_object, ref_object2marker)

marker2cam = np.eye(4)
marker2cam[0,3] = 0.024 # unit m


# find the transform from turtle to cam
turtle2cam = np.matmul(turtle2marker, marker2cam)


print(turtle2ref_object)











# ([1, 2], [array([[ 9.99996136e-01,  2.48599654e-03,  1.24398257e-03,
#         -8.09872785e-01],
#        [-2.48607377e-03,  9.99996908e-01,  6.05430663e-05,
#         -4.74903976e-02],
#        [-1.24382821e-03, -6.36354648e-05,  9.99999224e-01,
#          1.59064212e-01],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]]), array([[ 0.99634353,  0.00137544, -0.08542645, -0.87943978],
#        [ 0.06945205,  0.56929085,  0.81919737,  0.01820458],
#        [ 0.04975925, -0.82213505,  0.56711373,  0.21016282],
#        [ 0.        ,  0.        ,  0.        ,  1.        ]])])
# <class 'tuple'>