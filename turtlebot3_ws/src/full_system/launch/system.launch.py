# my_launch_file.launch.py

import launch
import launch_ros.actions

def generate_launch_description():
    # Define the node to start up
    drone = launch_ros.actions.Node(
        package='full_system',
        executable='drone',
        name='drone',
        output='screen'
    )
    desired_position = launch_ros.actions.Node(
        package='full_system',
        executable='desired_position',
        name='desired_position',
        output='screen'
    )
    trajectory = launch_ros.actions.Node(
        package='full_system',
        executable='trajectory',
        name='trajectory',
        output='screen'
    )
    simulation_vi = launch_ros.actions.Node(
        package='full_system',
        executable='simulation_vi',
        name='simulation_vi',
        output='screen'
    )



    # Create the launch description
    ld = launch.LaunchDescription()

    # Add the node to the launch description
    ld.add_action(drone)
    ld.add_action(desired_position)
    ld.add_action(trajectory)
    ld.add_action(simulation_vi)

    return ld