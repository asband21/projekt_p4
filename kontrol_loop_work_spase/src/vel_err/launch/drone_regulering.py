from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='vel',
            name='ll'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='rc',
            name='ll_reg'
        ),
    ])
