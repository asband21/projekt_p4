import rclpy
from rclpy.node import Node

from personal_interface.srv import TargetPose, TakePicture
from rclpy.publisher import Publisher
from std_srvs.srv import Empty

import numpy as np 
import pyrealsense2.pyrealsense2 as rs
import cv2

import tf2_ros as tf2
import tf_transformations as tf
from tf2_ros import TransformListener
from tf2_ros.buffer import Buffer
from std_msgs.msg import Header
import time

from sensor_msgs.msg import CameraInfo, Image


class image_analisys(Node):
    def __init__(self):
        super().__init__("image_analisys") 

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer,self)

        self.node_image_analisys = rclpy.create_node("sub_node_image_analisys")

        self.cli_trajectory = self.create_client(TargetPose,"go_to_target_pose")

        self.srv_calulate_target_pose = self.create_service(TakePicture,"calculate_target_pose",self.srv_take_aligment_picture) 
        self.initial_camera() 

        self.publisher_intrinsics = self.node_image_analisys.create_publisher(CameraInfo,"/stereo/left/camera_info",10)
        self.publisher_rgb = self.node_image_analisys.create_publisher(Image,"/stereo/left/image_rect_color",10)


        print("camrea : ", self.camera_intrinsics)
        hz = 1/3
        self.timer = self.create_timer(hz,self.publish_intrincis_and_rgb)



    def initial_camera(self): 
        self.pipeline = rs.pipeline()
        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs.config()

        config.enable_stream(rs.stream.depth, 80, 60, rs.format.z16, 5)

        config.enable_stream(rs.stream.color, 320, 240, rs.format.bgr8, 10)

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


    def publish_intrincis_and_rgb(self):


        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        color_image = np.asanyarray(color_frame.get_data())
        # Publish the data
        msg_intrinsics = CameraInfo()
        msg_intrinsics.header.frame_id = "camera_link"
        msg_intrinsics.header.stamp = self.get_clock().now().to_msg()
        # msg_intrinsics.height = self.camera_intrinsics.height
        # msg_intrinsics.width = self.camera_intrinsics.width
        # msg_intrinsics.distortion_model = "plumb_bob"
        # msg_intrinsics.d = self.camera_intrinsics.coeffs
        # msg_intrinsics.k = self.camera_intrinsics.K
        # msg_intrinsics.r = self.camera_intrinsics.R
        # msg_intrinsics.p = self.camera_intrinsics.p


        self.msg_intrinsics = CameraInfo()
        self.msg_intrinsics.width = self.camera_intrinsics.width
        self.msg_intrinsics.height = self.camera_intrinsics.height
        self.msg_intrinsics.distortion_model = 'plumb_bob'
        self.msg_intrinsics.d = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.msg_intrinsics.k = [self.camera_intrinsics.fx, 0.0, self.camera_intrinsics.ppx, 0.0, self.camera_intrinsics.fy, self.camera_intrinsics.ppy, 0.0, 0.0, 1.0]
        self.msg_intrinsics.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        self.msg_intrinsics.p = [self.camera_intrinsics.fx, 0.0, self.camera_intrinsics.ppx, 0.0, 0.0, self.camera_intrinsics.fy, self.camera_intrinsics.ppy, 0.0, 0.0, 0.0, 1.0, 0.0]
    

        self.publisher_intrinsics.publish(msg_intrinsics)

        msg_rgb = Image()
        msg_rgb.header.frame_id = "camera_link"
        msg_rgb.header.stamp = self.get_clock().now().to_msg()
        msg_rgb.height = color_image.shape[0]
        msg_rgb.width = color_image.shape[1]
        msg_rgb.encoding = "rgb8"
        msg_rgb.data = color_image.tostring()
        self.publisher_rgb.publish(msg_rgb)


       



    def srv_take_aligment_picture(self, request, response):
        # We will be removing the background of objects more than
        clipping_distance_in_meters = 2  # Unit: meter
        clipping_distance = clipping_distance_in_meters / self.depth_scale
    
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

        # Remove background - Set pixels further than clipping_distance to white
        background = 255
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), background, color_image) 


        # Finding QR-Codes 
        qr_image =  bg_removed
        #cv2.imread('images/qr-code.png')
        see_qr,where_qr = self.detector.detectMulti(qr_image)
        x,y,z = self.convert_depth_frame_to_pointcloud(depth_image,self.camera_intrinsics) 
        pointcloud = np.dstack((x,y,z)) 

        if see_qr == True:  
            set_of_qr_found_counter = 0
            x_median = np.zeros(int(where_qr.shape[0]))
            y_median = np.zeros(int(where_qr.shape[0]))
            drawing = np.zeros((qr_image.shape[0],qr_image.shape[1]))
            for i in range(where_qr.shape[0]):  
                #Store the QR-code ceter point in median
                x_median[i] =(where_qr[i][0][0]  + where_qr[i][1][0]  + where_qr[i][2][0]  + where_qr[i][3][0])/4 
                y_median[i] = (where_qr[i][0][1]  + where_qr[i][1][1]  + where_qr[i][2][1]  + where_qr[i][3][1])/4 
                ###########################################
                for points in range(int(where_qr.shape[1])): 
                    drawing=cv2.line(qr_image,(int(where_qr[i][points][0]),int(where_qr[i][points][1])),(int(where_qr[i][points][0]),int(where_qr[i][points][1])),(255,0,0),5) #Marking the conor of the QR-codes
                drawing=cv2.line(qr_image,(int(x_median[i]),int(y_median[i])),(int(x_median[i]),int(y_median[i])),(0,255,0),5)  # Marking the center of the QR-codes
                print("Center of the QR-Code = ({} , {})".format(x_median[i],y_median[i])) # Prints the centers of the QR-codes
            print("QR-Code ::: done")
            cv2.imwrite('~/testing_image/images/QR-code_{}.png'.format(set_of_qr_found_counter),drawing)  
            set_of_qr_found_counter+= 1 


            for i in range(where_qr.shape[0]):
                point = pointcloud[y_median[i],x_median[i]]
                self.send_request(point)
            
            response.success = True 
            return response
        else: 

            response.success = False
            print("No QR-Code found ....") 
            return response

                

    
    

    def send_request(self,point):
        while not self.cli_trajectory.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
    
        turtleTransform = self.tf_buffer.lookup_transform('world', 'turtle', rclpy.time.Time(), rclpy.duration.Duration(seconds=0.1))

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
