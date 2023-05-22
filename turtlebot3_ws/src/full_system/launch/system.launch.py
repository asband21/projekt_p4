
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'run_number',
            default_value='1',
            description='the run number'
        ),
        Node(
            package='full_system',
            executable='turtle_follower',
        ),
        Node(
            package='full_system',
            executable='image',
            parameters=[{'run_number': LaunchConfiguration('run_number')}]
        ),
        Node(
            package='full_system',
            executable='srv_tf',
        ),
        # Node(
        #     package='full_system',
        #     executable='desired_position',
        # ),
        # Node(
        #     package='full_system',
        #     executable='qr_tf_pub',
        #     # parameters=[{'run_number': LaunchConfiguration('run_number')}]

        # ),
        # # Node(
        #     package='full_system',
        #     executable='world_tag_read_tf',
        # ),

        # Node(
        #     package='full_system',
        #     executable='simulation_vi',
        # )
    ])