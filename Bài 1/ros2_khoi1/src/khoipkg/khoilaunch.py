from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='khoipkg',
            namespace='khoi1',
            executable='talker',
            name='sim',
            arguments=['--ros-args', '--log-level', 'info']
        ),
        Node(
            package='khoipkg',
            namespace='khoi1',
            executable='listener',
            name='sim',
            arguments=['--ros-args', '--log-level', 'info']
        ),
        
    ])
