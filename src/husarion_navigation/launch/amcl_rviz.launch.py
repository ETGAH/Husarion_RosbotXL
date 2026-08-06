#!/usr/bin/env python3

"""
RViz pre-configured for Chapter 4 Phase A: Fixed Frame set to map, with
Map, RobotModel, TF, ParticleCloud, and LaserScan already added, so nothing
needs adding by hand and there's no RViz topic-browser refresh race to hit.

  ros2 launch husarion_navigation amcl_rviz.launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock.",
    )

    declare_rviz_config = DeclareLaunchArgument(
        "rviz_config",
        default_value=PathJoinSubstitution(
            [FindPackageShare("husarion_navigation"), "rviz", "amcl.rviz"]
        ),
        description="Full path to the RViz config file to load.",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rviz_config")],
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}],
    )

    return LaunchDescription([declare_use_sim_time, declare_rviz_config, rviz_node])
