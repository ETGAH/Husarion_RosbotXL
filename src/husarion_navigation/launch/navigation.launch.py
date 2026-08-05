#!/usr/bin/env python3

"""
Course-owned Nav2 bring-up for Chapter 1.

Every server below is launched as its own node, pointed at its own YAML
file(s) under husarion_navigation/config/ instead of one shared
nav2_params.yaml, so each chapter can show and edit exactly the file its
topic covers. Only the servers Chapter 1 actually needs are here:
map_server, amcl, controller_server (+ local_costmap), planner_server
(+ global_costmap), smoother_server, behavior_server, and bt_navigator,
brought up by a single lifecycle_manager. collision_monitor and
waypoint_follower are not part of this file; they get added when their
own chapters (7 and 8) introduce them. velocity_smoother and
docking_server are not used anywhere in this course and are not launched
at all.

Every launch argument below has a working default, so the whole stack
comes up with no arguments required:

  ros2 launch husarion_navigation navigation.launch.py
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    husarion_navigation_share = FindPackageShare("husarion_navigation")

    declare_map = DeclareLaunchArgument(
        "map",
        default_value=PathJoinSubstitution(
            [husarion_navigation_share, "maps", "office_map.yaml"]
        ),
        description="Full path to the map YAML file to load into map_server.",
    )

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation (Gazebo) clock.",
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    lifecycle_nodes = [
        "map_server",
        "amcl",
        "controller_server",
        "smoother_server",
        "planner_server",
        "behavior_server",
        "bt_navigator",
    ]

    map_server_node = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "map_server.yaml"]),
            {"use_sim_time": use_sim_time, "yaml_filename": LaunchConfiguration("map")},
        ],
    )

    amcl_node = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "amcl.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    controller_server_node = Node(
        package="nav2_controller",
        executable="controller_server",
        name="controller_server",
        output="screen",
        parameters=[
            PathJoinSubstitution(
                [husarion_navigation_share, "config", "controller_server.yaml"]
            ),
            PathJoinSubstitution([husarion_navigation_share, "config", "local_costmap.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    smoother_server_node = Node(
        package="nav2_smoother",
        executable="smoother_server",
        name="smoother_server",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "smoother_server.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    planner_server_node = Node(
        package="nav2_planner",
        executable="planner_server",
        name="planner_server",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "planner_server.yaml"]),
            PathJoinSubstitution([husarion_navigation_share, "config", "global_costmap.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    behavior_server_node = Node(
        package="nav2_behaviors",
        executable="behavior_server",
        name="behavior_server",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "behavior_server.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    bt_navigator_node = Node(
        package="nav2_bt_navigator",
        executable="bt_navigator",
        name="bt_navigator",
        output="screen",
        parameters=[
            PathJoinSubstitution([husarion_navigation_share, "config", "bt_navigator.yaml"]),
            {"use_sim_time": use_sim_time},
        ],
    )

    lifecycle_manager_node = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager",
        output="screen",
        parameters=[
            PathJoinSubstitution(
                [husarion_navigation_share, "config", "lifecycle_manager.yaml"]
            ),
            {"use_sim_time": use_sim_time, "node_names": lifecycle_nodes},
        ],
    )

    return LaunchDescription(
        [
            declare_map,
            declare_use_sim_time,
            map_server_node,
            amcl_node,
            controller_server_node,
            smoother_server_node,
            planner_server_node,
            behavior_server_node,
            bt_navigator_node,
            lifecycle_manager_node,
        ]
    )
