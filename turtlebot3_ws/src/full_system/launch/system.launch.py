# my_launch_file.launch.py

import launch
import launch_ros.actions

def generate_launch_description():
    # Define the node to start up
    my_node = launch_ros.actions.Node(
        package='full_system',
        executable='drone',
        name='my_node',
        output='screen'
    )

    # Create the launch description
    ld = launch.LaunchDescription()

    # Add the node to the launch description
    ld.add_action(my_node)

    return ld
