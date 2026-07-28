from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ch2_frames_odometry',
            executable='odom_broadcaster',
            name='odom_broadcaster',
            output='screen',
        ),
        Node(
            package='ch2_frames_odometry',
            executable='static_sensor_frames',
            name='static_sensor_frames',
            output='screen',
        ),
        Node(
            package='ch2_frames_odometry',
            executable='frame_listener',
            name='frame_listener',
            output='screen',
        ),
    ])
