"""Start a development-only ROS 2 state node (no camera, motors or cmd_vel)."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='mars_rover', executable='rover_dev', name='rover_dev', output='screen'),
    ])
