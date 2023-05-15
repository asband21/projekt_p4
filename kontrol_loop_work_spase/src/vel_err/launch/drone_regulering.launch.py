from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='vel',
            name='vel_d'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='reg',
            name='reg_d'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='service',
            name='service_d'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='client',
            name='client_d'
        ),
         Node(
            package='vel_err',
            namespace='vel_err',
            executable='drone',
            name='drone_d'
        ),
    ])
