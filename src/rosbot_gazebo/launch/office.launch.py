#!/usr/bin/env python3
# world: husarion_office.sdf

# Copyright 2026 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
UI-launchable ROSbot XL simulation entrypoint (ETGAH "Worlds" panel).

The ETGAH Worlds panel only discovers `*.launch.py` files, so this wraps the
existing `simulation.yaml` (world + robot spawn + bridge + controllers + EKF)
as a single Python launch file the panel can list and run in one click -
no terminal command required. Equivalent to running by hand:

  ros2 launch rosbot_gazebo simulation.yaml \
      robot_model:=rosbot_xl configuration:=autonomy gz_world:=husarion_office \
      x:=0.0 y:=0.0 z:=0.1 rviz:=False

Defaults are pinned to this course's setup (ROSbot XL, autonomy sensor suite,
husarion_office world, spawn pose matching config/nav2_params.yaml's AMCL
initial pose). Override any of them from the Worlds panel's launch-argument
fields the same way you would with `key:=value` on the command line.

RViz is deliberately never auto-launched here - every chapter gives its own
explicit `ros2 launch rosbot_description rviz.yaml` command instead, so
students always know exactly which RViz config (if any) they're looking at.
"""

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    simulation_yaml = PathJoinSubstitution(
        [FindPackageShare("rosbot_gazebo"), "launch", "simulation.yaml"]
    )

    simulation = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(simulation_yaml),
        launch_arguments={
            "robot_model": "rosbot_xl",
            "configuration": "autonomy",
            "gz_world": "husarion_office",
            "x": "0.0",
            "y": "0.0",
            "z": "0.1",
            "rviz": "False",
        }.items(),
    )

    return LaunchDescription([simulation])
