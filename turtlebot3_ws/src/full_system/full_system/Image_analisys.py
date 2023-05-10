import rclpy
from rclpy.node import Node

from personal_interface.srv import TargetPose
from std_srvs.srv import Empty

import numpy as np 
import pyrealsense2 as rs
import cv2


class image_analisys(Node):
    def __init__(self):
        super().__init__("image_analisys") 

        self.sub_node_image_analisys = rclpy.create_node("sub_node_image_analisys")

        self.sub_cli_image_analisys = self.create_client(TargetPose,"go_to_target_pose")

        self.srv_calulate_target_pose = self.create_service(Empty,"calculate_target_pose",self.callback_srv_taget_pose) 
        self.initial_camera() 




    def send_request(self,req):
        while not self.sub_cli_simulated_vicon.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        

        future = self.sub_cli_simulated_vicon.call_async(req)
        rclpy.spin_until_future_complete(self.sub_node_image_analisys,future)
        return future.result()
    

    def callback_srv_taget_pose(self,request,response):
        
        
        return 


    def image_analisys(self):
        req = TargetPose.Request()
        req.target_pose.transform.translation.x = 6.0
        req.target_pose.transform.translation.y = 1.0
        req.target_pose.transform.translation.z = 4.0
        req.target_pose.transform.rotation.x = 0.0
        req.target_pose.transform.rotation.y = 0.0
        req.target_pose.transform.rotation.z = 0.0
        req.target_pose.transform.rotation.w = 1.0

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

    def take_aligment_picture(self):
        # We will be removing the background of objects more than
        clipping_distance_in_meters = 2  # Unit: meter
        clipping_distance = clipping_distance_in_meters / self.depth_scale

        # Streaming loop
        try:
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
            # cv2.imwrite('~/tests/test_1/images/c1.png', bg_removed)  #Rember to uncomment me!!!!!!! 
            cap = cv2.VideoCapture(bg_removed) 



            if self.detector.detect(bg_removed) == True : 
                x,y,z = self.convert_depth_frame_to_pointcloud(bg_removed, self.camera_intrinsics) 
                normal_vector = self.pythoMath(x,y,z)
             

            
            """ 
            1.  Take  a picture, with a legth of only 2 meters 
            2.  Is there any QR-code?, yes then 
            3.  Point clound of QR code 
            3.5 find the orientation and postion
            4.  !Send point to drone 
            5.  !wait for drone  
            6.  !Turn and repeat
            """
            
            


        finally:
            self.pipeline.stop()

    
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
    
    def pythoMath(self,x,y,z):
        xs = x.flatten()[::40]
        ys = y.flatten()[::40]
        zs = z.flatten()[::40]
        # Cleaning the images for black pixels
        xs = [i for i in xs if i != 0]
        ys = [i for i in ys if i != 0]
        zs = [i for i in zs if i != 0]
        if len(xs)<3:
            return
        
        # do fit
        tmp_A = []
        tmp_b = []
        for i in range(len(xs)):
            tmp_A.append([xs[i], ys[i], 1])
            tmp_b.append(zs[i])
        b = np.matrix(tmp_b).T
        A = np.matrix(tmp_A)

        # Manual solution
        fit = (A.T * A).I * A.T * b
        errors = b - A * fit
        residual = np.linalg.norm(errors)

        return fit



def main(args=None):
    rclpy.init(args=args)

    node = image_analisys()

    rclpy.spin(node)

    node.destroy_node()    
    
    rclpy.shutdown()


if __name__ == "__main__":
    main()
