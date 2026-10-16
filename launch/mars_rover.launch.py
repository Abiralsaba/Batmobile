"""Launch the development Mars Rover stack without hardware actuation."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    mission_control_node = Node(
        package='mars_rover',
        executable='mission_control_node',
        name='mission_control',
        output='screen',
        emulate_tty=True,
    )

    return LaunchDescription([
        mission_control_node,
    ])
