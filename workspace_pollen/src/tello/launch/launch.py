from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tello',
            namespace='turtlesim1',
            executable='tello_connect',
            name='sim'
        ),
        Node(
            package='tello',
            namespace='turtlesim2',
            executable='tello_trajectory',
            name='sim'
        ),
        Node(
            package='tf2_workshop',
            executable='staticTF',
            name='mimic'
        )
    ])