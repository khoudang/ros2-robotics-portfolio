from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_pkg',
            namespace='vidu1',
            executable='talkervd1',
            name='sim1',
            output='screen',

        ),
        Node(
            package='my_pkg',
            namespace='vidu1',
            executable='listenervd1',
            name='sim2',
            output='screen',

        ),

    ])
