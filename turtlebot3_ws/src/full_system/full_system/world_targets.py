import rclpy
from rclpy.node import Node


from tf2_ros import TransformBroadcaster, TransformStamped

from tf2_msgs.msg import TFMessage

import pickle

import tf_transformations as tf

import os

import numpy as np

class tag(Node):

    def __init__(self):
        super().__init__('tag')
        self.ids = [1,2,3,4,5,6]

        mode = ""

        if mode == "cal":
            self.file_path = "/home/ubuntu/tests/turtleTest/calibration_turtle2cam.pkl"
        else:
            self.file_path = "/home/ubuntu/tests/turtleTest/world_targets.pkl"


        self.create_subscription(TFMessage, 'tf', self.callback, 10 )    




    def callback(self, msg):

        for id in self.ids:
            source_frame_id = 'vicon'
            target_frame_id = f'tag_{id}'
            for transform in msg.transforms:
                if (transform.header.frame_id == source_frame_id and transform.child_frame_id == target_frame_id):
                    self.current_tag = transform

                    transform_pos = [transform.transform.translation.x, transform.transform.translation.y, transform.transform.translation.z]


                    transform_q = [transform.transform.rotation.x, transform.transform.rotation.y, transform.transform.rotation.z, transform.transform.rotation.w]

                    transform_matrix = tf.quaternion_matrix(transform_q)

                    transform_matrix[0,3] = transform_pos[0]
                    transform_matrix[1,3] = transform_pos[1]
                    transform_matrix[2,3] = transform_pos[2]

                    ids = [id]
                    transform_matrixs = [transform_matrix]
                    self.current_tag = (ids, transform_matrixs)



                    folder_path = "/home/ubuntu/tests/turtleTest"


                    if not os.path.exists(self.file_path):


                        os.makedirs(folder_path, exist_ok=True)
                        

                        # Create a file and save self.current_tag
                        with open(self.file_path, "wb") as file:
                            pickle.dump(self.current_tag, file)

                    else:
                        # Read the data from the file
                        with open(self.file_path, "rb") as file:
                            previous_targets = pickle.load(file)

                        # Append the new data to the list
                        previous_ids, previous_vicon2qrcode = previous_targets
                        current_ids, current_vicon2qrcode = self.current_tag


                        ids_in_previous = set(previous_ids).intersection(set(current_ids))

                        new_ids = set(current_ids) - ids_in_previous

                        # Check if current_targets is in the data
                        if new_ids:
                            # Create a dictionary mapping IDs to their corresponding data
                            current_data_dict = dict(zip(current_ids, current_vicon2qrcode))

                            for id in new_ids:
                                previous_ids.append(id)
                                previous_vicon2qrcode.append(current_data_dict[id])


                            updated_targets = (previous_ids, previous_vicon2qrcode)

                            
                            # Save the stripped data back to the file
                            with open(self.file_path, "wb") as file:
                                pickle.dump(updated_targets, file)
                    
                    break




            








def main(args=None):
    rclpy.init(args=args)
    node = tag()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()