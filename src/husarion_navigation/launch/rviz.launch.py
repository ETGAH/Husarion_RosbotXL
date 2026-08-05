#!/usr/bin/env python3

"""
RViz with this course's curated Nav2 view: Fixed Frame set to map, and only
the displays a chapter has actually introduced (Map, RobotModel, LaserScan,
ParticleCloud, GlobalCostmap, LocalCostmap, GlobalPlan). No docking plugin,
no downsampled_costmap, nothing left unexplained.

  ros2 launch husarion_navigation rviz.launch.py
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
            [FindPackageShare("husarion_navigation"), "rviz", "nav2.rviz"]
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
