from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='vel',
            name='vel'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='reg',
            name='reg'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='service',
            name='service'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='publish',
            name='publish'
        ),
    ])
