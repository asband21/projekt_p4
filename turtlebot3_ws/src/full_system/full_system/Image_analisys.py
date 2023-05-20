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
        self.run_number = "5"
        self.number_of_images_taken = 0

        self.destination_for_test_data = "/home/ubuntu/tests/turtleTest"


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



    def vicon2qr_code(self, cam2qrcode_transform):



        # the transformation from the vicon to the turtlebot
        
        vicon2turtle = self.send_vicon2turtle()

        vicon2turtle_translation = [vicon2turtle.transform.translation.x, vicon2turtle.transform.translation.y, vicon2turtle.transform.translation.z]

        vicon2turtle_rot_matrix = tf.quaternion_matrix([vicon2turtle.transform.rotation.x, vicon2turtle.transform.rotation.y, vicon2turtle.transform.rotation.z, vicon2turtle.transform.rotation.w]) # if rotation is bad, this might return a wrong degrees

        vicon2turtle_transform = np.eye(4)
        vicon2turtle_transform[:3, :3] = vicon2turtle_rot_matrix[:3, :3]
        vicon2turtle_transform[:3, 3] = vicon2turtle_translation


        # the transformation from turtlebot to the camera
        turtle2cam_translation = [-0.04, 0.03, 0.075]
        rotation_x = np.radians(-30)
        turtle2cam_rot_matrix = tf.euler_matrix(rotation_x, 0.0, 0.0, 'sxyz')

        self.get_logger().info(f"turtle2cam_rot_matrix: {turtle2cam_rot_matrix}")

        # turtle2cam_rot_matrix = [  [1.0,  0.0,  0.0],
        #                            [0.0,  0.8660254,  0.5],
        #                            [0.0, -0.5,  0.8660254] ]
        
        turtle2cam_transform = np.eye(4)
        turtle2cam_transform[:3, :3] = turtle2cam_rot_matrix[:3, :3]
        turtle2cam_transform[:3, 3] = turtle2cam_translation

        
        # the transformation from vice to the camera
        vicon2cam_transform = np.dot(vicon2turtle_transform, turtle2cam_transform)


        # the transformation from vicon to the qr code
        vicon2qrcode_transform = np.dot(vicon2cam_transform, cam2qrcode_transform)


        # the transformation from the qr code to the target
        target_rot_matrix = [[0.0, 0.0, -1.0],
                            [1.0,  0.0,  0.0],
                            [0.0, -1.0,  0.0]]
        target_translation = [0.0, 0.0, 0.1]

        qrcode2target_transform = np.eye(4)
        qrcode2target_transform[:3, :3] = target_rot_matrix
        qrcode2target_transform[:3, 3] = target_translation


        # the transformation from vicon to the target
        vicon2target_transform = np.dot(vicon2qrcode_transform, qrcode2target_transform)



        return vicon2qrcode_transform














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

        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

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
        qr_image = None
        
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
                image_folder_path = f"{self.destination_for_test_data}/run{self.run_number}/images"
                os.makedirs(image_folder_path, exist_ok=True)
                cv2.imwrite(self.destination_for_test_data+ f"/run{self.run_number}/images/image_no_qr_{self.number_of_images_taken}.png", qr_image)
            
                response.success = False
                self.number_of_images_taken += 1
                self.pipeline.stop()
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



            current_cam2qrcode_transforms = []
            for i in range(len(rot)):
                T = np.eye(4)
                T[:3, :3] = rot_matrix[i][0]
                T[:3, 3] = position[i]

                current_cam2qrcode_transforms.append(T)            
            

            current_vicon2qrcode = []
            for trans in current_cam2qrcode_transforms:
                current_vicon2qrcode.append(self.vicon2qr_code(trans))

            current_targets = (current_ids, current_vicon2qrcode)

                

            image_folder_path = f"{self.destination_for_test_data}/run{self.run_number}/images"
            os.makedirs(image_folder_path, exist_ok=True)
            

            folder_path = f"{self.destination_for_test_data}/run{self.run_number}/data"
            file_name = f"test{self.run_number}.pkl"
            file_path = os.path.join(folder_path, file_name)



            # Check if the file exists
            if not os.path.exists(file_path):

                #----------------------------------------------------------------------------------#
                #!!!!!!!!!!!!!! MAKE THE LOGIC HERE TO CALL TRAJECTORY NODE !!!!!!!!!!!!!!!!!!!!!!!#
                #----------------------------------------------------------------------------------#

                os.makedirs(folder_path, exist_ok=True)
                

                # Create a file and save current_targets
                with open(file_path, "wb") as file:
                    pickle.dump(current_targets, file)
                self.get_logger().info(f"File {file_name} created and saved to {folder_path}")
                self.get_logger().info("111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")

            else:
                # Read the data from the file
                self.get_logger().info("22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
                
                with open(file_path, "rb") as file:
                    previous_targets = pickle.load(file)
                
                previous_ids, previous_vicon2qrcode = previous_targets
                current_ids, current_vicon2qrcode = current_targets


                ids_in_previous = set(previous_ids).intersection(set(current_ids))
                self.get_logger().info(f"ids_in_previous {ids_in_previous}")

                new_ids = set(current_ids) - ids_in_previous
                self.get_logger().info(f"new_ids {new_ids}")

                # Check if current_targets is in the data
                if new_ids:
                    self.get_logger().info(f"seconf if QR-code {current_ids} already in the file {file_name}")
                    self.get_logger().info("33333333333333333333333333333333333333333333333333333333333333333333333333333333333333")



                    # Create a dictionary mapping IDs to their corresponding data
                    current_data_dict = dict(zip(current_ids, current_vicon2qrcode))

                    for id in new_ids:
                        previous_ids.append(id)
                        previous_vicon2qrcode.append(current_data_dict[id])

                    # for id in new_ids:
                    #     current_index = current_ids.index(id)

                    #     previous_ids.append(current_ids[current_index])
                    #     previous_vicon2qrcode.append(current_vicon2qrcode[current_index])


                    # save the qr_image in the folder ~/test/turtleTest/run{self.run_number}/images. where the qr_image name is the ids found in it
                    cv2.imwrite(self.destination_for_test_data+ f"/run{self.run_number}/images/image_{new_ids}.png", qr_image)
                    path = self.destination_for_test_data+ f"/run{self.run_number}/images/image_{new_ids}.png"
                    self.get_logger().info(f"QR-code image saved to {path}")

                    updated_targets = (previous_ids, previous_vicon2qrcode)

                    
                    # Save the stripped data back to the file
                    with open(file_path, "wb") as file:
                        pickle.dump(updated_targets, file)
                else:
                    self.get_logger().info("44444444444444444444444444444444444444444444444444444444444444444444444444444444444")
                    cv2.imwrite(self.destination_for_test_data + f"/run{self.run_number}/images/image_no_new_ids.png", qr_image)
                    path = self.destination_for_test_data+ "/images/image_no_new_ids.png"
                    self.get_logger().info(f"QR-code image saved to {path}")

                    # Save current_targets to the file
                    with open(file_path, "wb") as file:
                        # previous_targets.append(current_targets)
                        pickle.dump(current_targets, file)
                    self.get_logger().info(f"seconod else QR-code {current_targets[0]} added to the file {file_name}")







            # # compine the self.distinct_targets path with a file name
            # file_name = os.path.join(self.destination_for_test_data, f"test{self.run_number}.pkl")

            # # Read the data from the file
            # with open(file_name, 'rb') as file:
            #     previous_targets = pickle.load(file)
            # if previous_targets is None:


            #     # Save the current_targets to a file
            #     with open(file_name, 'wb') as file:
            #         pickle.dump(current_targets, file)


            #     # Read the data from the file
            #     with open(file_name, 'rb') as file:
            #         previous_targets = pickle.load(file)

            # else:


            #     # Read the data from the file
            #     with open(file_name, 'rb') as file:
            #         previous_targets = pickle.load(file)

            #     # previous_targets = np.vstack((previous_targets, current_targets))

            #     know_ids = previous_targets[0]
            #     know_transforms = previous_targets[1]

            #     # this is to check if the id is already in the know_ids
            #     for i in range(len(current_targets[0])):
            #         if current_targets[0][i] not in know_ids:
            #             know_ids.append(current_targets[0][i])
            #             know_transforms.append(current_targets[1][i])



            #     # Save the current_targets to a file
            #     with open(file_name, 'wb') as file:
            #         pickle.dump(current_targets, file)



            # print("previous_targets: ", type(previous_targets))

            
            # know_ids = previous_targets[0]
            # know_transforms = previous_targets[1]

            # print("know_ids: ", know_ids)
            # print("know_ids: ", type(know_ids))

            # print("know_transforms: ", know_transforms)
            # print("know_transforms: ", type(know_transforms))

            response.success = True 
            self.pipeline.stop()
            
            return response
        else: 

            response.success = False
            print("No QR-Code found ....") 
            self.pipeline.stop()
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
