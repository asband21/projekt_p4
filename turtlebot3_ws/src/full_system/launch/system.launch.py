
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='full_system',
            executable='turtle_follower',
        ),
        Node(
            package='full_system',
            executable='image',
        ),
        Node(
            package='full_system',
            executable='srv_tf',
        ),
        # Node(
        #     package='full_system',
        #     executable='simulation_vi',
        # )
    ])