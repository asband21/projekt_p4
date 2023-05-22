
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    run_number = 1
    return LaunchDescription([
        Node(
            package='full_system',
            executable='turtle_follower',
        ),
        Node(
            package='full_system',
            executable='image',
            parameters=[{'run_number': run_number}]
        ),
        Node(
            package='full_system',
            executable='srv_tf',
        ),
        Node(
            package='full_system',
            executable='desired_position',
        ),
        Node(
            package='full_system',
            executable='qr_tf_pub',
            parameters=[{'run_number': run_number}]
        ),
        Node(
            package='full_system',
            executable='world_tag_read_tf',
        ),

        # Node(
        #     package='full_system',
        #     executable='simulation_vi',
        # )
    ])