import rclpy
from rclpy.node import Node

from personal_interface.srv import TargetPose, TakePicture
from rclpy.publisher import Publisher
from std_srvs.srv import Empty

import numpy as np 
import pyrealsense2.pyrealsense2 as rs
import cv2

import pickle

import tf_transformations as tf
from std_msgs.msg import Header
import time

from sensor_msgs.msg import CameraInfo, Image

from personal_interface.srv import Tf

import os

class image_analisys(Node):
    def __init__(self):
        super().__init__("image_analisys") 
        self.test_number = "1"

        self.distination_for_test_data = "~/test_data/test_data_1/"


        self.node_image_analisys = rclpy.create_node("node_image_analisys")

        self.cli_trajectory = self.create_client(TargetPose,"go_to_target_pose")

        self.srv_calulate_target_pose = self.create_service(TakePicture,"calculate_target_pose",self.srv_take_aligment_picture) 
        self.cli_vicon2turtle = self.node_image_analisys.create_client(Tf,"vicon2turtle")
       

    def send_vicon2turtle(self):
        while not self.cli_vicon2turtle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service vicon2turtle not available, waiting again...")
        request = Tf.Request()
        future = self.cli_vicon2turtle.call_async(request)
        rclpy.spin_until_future_complete(self.node_image_analisys, future)
        return future.result().tf



    def transformations(self):


            target_rot_matrix = [[0.0, -0.0, -1.0],
                                [1.0,  0.0,  0.0],
                                [0.0, -1.0,  0.0]]
            target_translation = [0.0, 0.0, 0.1]

            self.target_transform = np.eye(4)
            self.target_transform[:3, :3] = target_rot_matrix
            self.target_transform[:3, 3] = target_translation




            self.camera_transform = np.eye(4)
            self.camera_transform[:3, :3] = np.array([[0.0, 0.0, 1.0],
                                                    [-1.0, 0.0, 0.0],
                                                    [0.0, -1.0, 0.0]])
            self.camera_transform[:3, 3] = np.array([0.0, 0.0, 0.0])






    def target_to_vicon(self):

        return np.dot(self.camera_transform, self.target_transform)




    def convert_depth_frame_to_pointcloud(self, depth_image, camera_intrinsics):
        """
        Convert the depthmap to a 3D point cloud
        Parameters:
        -----------
        depth_frame 	 	 : rs.frame()
                            The depth_frame containing the depth map
        camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed
        Return:
        ----------
        x : array
            The x values of the pointcloud in meters
        y : array
            The y values of the pointcloud in meters
        z : array
            The z values of the pointcloud in meters
        """

        [height, width] = depth_image.shape

        nx = np.linspace(0, width-1, width)
        ny = np.linspace(0, height-1, height)
        u, v = np.meshgrid(nx, ny)
        x = (u.flatten() - camera_intrinsics.ppx)/camera_intrinsics.fx
        y = (v.flatten() - camera_intrinsics.ppy)/camera_intrinsics.fy

        z = depth_image.flatten() / 1000
        x = np.multiply(x,z)
        y = np.multiply(y,z)

       
        x = np.reshape(x,(height,width))
        y = np.reshape(y,(height,width))
        z = np.reshape(z,(height,width))


        return x,y,z 

    def initial_camera(self): 
        self.pipeline = rs.pipeline()
        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs.config()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        profile = self.pipeline.start(config) 

        profile_depth = profile.get_stream(rs.stream.depth) # Fetch stream profile for depth stream
        self.camera_intrinsics  = profile_depth.as_video_stream_profile().get_intrinsics() # Downcast to video_stream_profile and fetch intrinsics

        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        align_to = rs.stream.color
        self.align = rs.align(align_to)  
        self.detector = cv2.QRCodeDetector()

        time.sleep(2) # Give the camera time to warm up



    def srv_take_aligment_picture(self, request, response):
        self.initial_camera()

        print(self.camera_intrinsics)

        distorsion = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

        #Selected coordinate points for each corner of QR code.
        qr_edges = np.array([[0,0,0],
                            [0,1,0],
                            [1,1,0],
                            [1,0,0]], dtype = 'float32').reshape((4,1,3))

        # Intel RealSense D435 intrinsic parameters
        width = 640
        height = 480
        # fx = 617.173
        # fy = 617.173
        # cx = 328.964
        # cy = 240.157

        fx = self.camera_intrinsics.fx
        fy = self.camera_intrinsics.fy
        cx = self.camera_intrinsics.ppx
        cy = self.camera_intrinsics.ppy

        # Create the camera matrix
        camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]], dtype=np.float32)


        # # We will be removing the background of objects more than
        # clipping_distance_in_meters = 2  # Unit: meter
        # clipping_distance = clipping_distance_in_meters / self.depth_scale
    
        break_count = 0
        see_qr = False
        where_qr = None

        
        while True:
            no_id = False
            # Get frameset of color and depth
            frames = self.pipeline.wait_for_frames()
            # frames.get_depth_frame() is a 640x360 depth image

            # Align the depth frame to color frame
            aligned_frames = self.align.process(frames)

            # Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()
            # Getheringng data from the imagese 
            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())


            # Finding QR-Codes 
            qr_image =  color_image


            see_qr, ids, where_qr, info = self.detector.detectAndDecodeMulti(qr_image)
                

            if break_count > 10:
                response.success = False
                return response
            if see_qr == False:
                # print(see_qr)
                break_count += 1
                continue
            
            print("ids: ",ids)

            for id in ids:
                if id == "":
                    no_id = True
                    print("id is empty")
            
            if no_id == True:
                continue
            else:
                break

        current_ids = []
        for id in ids:
            current_ids.append( int(id))

            
        # convert the image to grayscale
        # qr_image = cv2.cvtColor(qr_image, cv2.COLOR_BGR2GRAY)


        ret = []
        rot = []
        trans = []
        for points in where_qr:
            ret.append(cv2.solvePnP(qr_edges, points, camera_matrix, distorsion)[0])
            rot.append(cv2.solvePnP(qr_edges, points, camera_matrix, distorsion)[1])
            trans.append(cv2.solvePnP(qr_edges, points, camera_matrix, distorsion)[2])

        # print("ret: ",ret)
        # print("rot: ",rot)
        # print("trans: ",trans)

        rot_matrix = []
        for rot_vec in rot:
            rot_matrix.append(cv2.Rodrigues(rot_vec))

        # print("rot_matrix: ",rot_matrix[0])

        for i in range(len(rot)):
            cv2.drawFrameAxes(qr_image,camera_matrix,distorsion,rot[i],trans[i],1,5)



        # cv2.imshow("QR Code", qr_image)
        # cv2.waitKey(0)

        # show the image that was scanned
        #cv2.waitKey(0)
        #cv2.imread('images/qr-code.png')
        
        x,y,z = self.convert_depth_frame_to_pointcloud(depth_image,self.camera_intrinsics) 
        pointcloud = np.dstack((x,y,z)) 

        if see_qr == True:  
            # set_of_qr_found_counter = 0
            x_median = np.zeros(int(where_qr.shape[0]))
            y_median = np.zeros(int(where_qr.shape[0]))
            # drawing = np.zeros((qr_image.shape[0],qr_image.shape[1]))
            for i in range(where_qr.shape[0]):  
                #Store the QR-code ceter point in median
                x_median[i] = (where_qr[i][0][0]  + where_qr[i][1][0]  + where_qr[i][2][0]  + where_qr[i][3][0])/4 
                y_median[i] = (where_qr[i][0][1]  + where_qr[i][1][1]  + where_qr[i][2][1]  + where_qr[i][3][1])/4 
                ###########################################
            #     for points in range(int(where_qr.shape[1])): 
            #         drawing=cv2.line(qr_image,(int(where_qr[i][points][0]),int(where_qr[i][points][1])),(int(where_qr[i][points][0]),int(where_qr[i][points][1])),(255,0,0),5) #Marking the conor of the QR-codes
            #     drawing=cv2.line(qr_image,(int(x_median[i]),int(y_median[i])),(int(x_median[i]),int(y_median[i])),(0,255,0),5)  # Marking the center of the QR-codes
            #     print("Center of the QR-Code = ({} , {})".format(x_median[i],y_median[i])) # Prints the centers of the QR-codes
            # print("QR-Code ::: done")
            # cv2.imwrite('~/testing_image/images/QR-code_{}.png'.format(set_of_qr_found_counter),drawing)  
            # set_of_qr_found_counter+= 1 

            position = []
            for i in range(where_qr.shape[0]):
                position.append(pointcloud[int(y_median[i]),int(x_median[i])])



            current_transforms = []
            for i in range(len(rot)):
                T = np.eye(4)
                T[:3, :3] = rot_matrix[i][0]
                T[:3, 3] = position[i]

                current_transforms.append(T)            
            
            # print("current_transforms: ",current_transforms)



            
            # multiply the target_transform with the current_transforms
            for i in range(len(current_transforms)):
                current_transforms[i] = np.dot(current_transforms[i], self.target_transform)
                # print("current_transforms: ",current_transforms[i])

            targets = (current_ids, current_transforms)
            # print("target_transform: ",target_transform)

            # make the csv file to store the targets
            

            # # store the targets in a csv file
            # with open('/home/carsten/qrcode_test/QR_code_orientation_OpenCV/QR-code.csv', 'w') as f:
            #     writer = csv.writer(f)
            #     writer.writerow(targets)
            #     f.close()


            print("targets: ",targets)



            # compine the self.distinct_targets path with a file name
            file_name = os.path.join(self.distination_for_test_data, "target1.pkl")

            # Read the data from the file
            with open(file_name, 'rb') as file:
                loaded_data = pickle.load(file)
            if loaded_data is None:


                # Save the targets to a file
                with open(file_name, 'wb') as file:
                    pickle.dump(targets, file)


                # Read the data from the file
                with open(file_name, 'rb') as file:
                    loaded_data = pickle.load(file)

            else:


                # Read the data from the file
                with open(file_name, 'rb') as file:
                    loaded_data = pickle.load(file)

                # loaded_data = np.vstack((loaded_data, targets))

                know_ids = loaded_data[0]
                know_transforms = loaded_data[1]

                # this is to check if the id is already in the know_ids
                for i in range(len(targets[0])):
                    if targets[0][i] not in know_ids:
                        know_ids.append(targets[0][i])
                        know_transforms.append(targets[1][i])



                # Save the targets to a file
                with open(file_name, 'wb') as file:
                    pickle.dump(targets, file)



            print("loaded_data: ", type(loaded_data))

            
            know_ids = loaded_data[0]
            know_transforms = loaded_data[1]

            print("know_ids: ", know_ids)
            print("know_ids: ", type(know_ids))

            print("know_transforms: ", know_transforms)
            print("know_transforms: ", type(know_transforms))

            response.success = True 
            return response
        else: 

            response.success = False
            print("No QR-Code found ....") 
            return response
            

    

    def send_request(self,point):
        while not self.cli_trajectory.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
    
        turtleTransform = self.tf_buffer.lookup_transform('vicon', 'turtle', rclpy.time.Time(), rclpy.duration.Duration(seconds=0.1))

        quaternion = [0, 0, 0, 1]
        turtleTransform.transform.rotation.x = quaternion[0]
        turtleTransform.transform.rotation.y = quaternion[1]
        turtleTransform.transform.rotation.z = quaternion[2]
        turtleTransform.transform.rotation.w = quaternion[3]

        rotationMatrix = tf.quaternion_matrix(quaternion)

        # Create homogeneous transformation matrix
        T = np.eye(4)
        T[:3, :3] = rotationMatrix
        T[:3, 3] = point

        
        # move 10 cm back in the y direction
        move_back = np.eye(4)
        move_back[1, 3] = -0.1 # unit is meters
        T = np.dot(T, move_back)

        srv_request = TargetPose.Request()
        srv_request.pose.position.x = T[0, 3]
        srv_request.pose.position.y = T[1, 3]
        srv_request.pose.position.z = T[2, 3]
        srv_request.pose.orientation.x = quaternion[0]
        srv_request.pose.orientation.y = quaternion[1]
        srv_request.pose.orientation.z = quaternion[2]
        srv_request.pose.orientation.w = quaternion[3]

        future = self.cli_trajectory.call_async(srv_request)
        rclpy.spin_until_future_complete(self.node_image_analisys,future)

        while future.result() == None:
            time.sleep(1/30)

        return future.result()


    def convert_depth_frame_to_pointcloud(self, depth_image, camera_intrinsics):
        """
        Convert the depthmap to a 3D point cloud
        Parameters:
        -----------
        depth_frame 	 	 : rs.frame()
                            The depth_frame containing the depth map
        camera_intrinsics : The intrinsic values of the imager in whose coordinate system the depth_frame is computed
        Return:
        ----------
        x : array
            The x values of the pointcloud in meters
        y : array
            The y values of the pointcloud in meters
        z : array
            The z values of the pointcloud in meters
        """

        [height, width] = depth_image.shape

        nx = np.linspace(0, width-1, width)
        ny = np.linspace(0, height-1, height)
        u, v = np.meshgrid(nx, ny)
        x = (u.flatten() - camera_intrinsics.ppx)/camera_intrinsics.fx
        y = (v.flatten() - camera_intrinsics.ppy)/camera_intrinsics.fy

        z = depth_image.flatten() / 1000
        x = np.multiply(x,z)
        y = np.multiply(y,z)

       
        x = np.reshape(x,(height,width))
        y = np.reshape(y,(height,width))
        z = np.reshape(z,(height,width))


        return x,y,z 

def main(args=None):
    rclpy.init(args=args)

    node = image_analisys()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()
