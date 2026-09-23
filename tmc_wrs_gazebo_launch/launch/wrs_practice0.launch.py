#!/usr/bin/env python3
# -*-encoding:UTF-8-*-
"""WRS2020 practice field #0 (seed=1) with open source stacks. See include/wrs_common.launch.py."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    wrs_common_path = os.path.join(
        get_package_share_directory("tmc_wrs_gazebo_launch"),
        "launch", "include", "wrs_common.launch.py",
    )

    return LaunchDescription([
        DeclareLaunchArgument("seed", default_value="1"),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(wrs_common_path),
            launch_arguments={"seed": LaunchConfiguration("seed")}.items(),
        ),
    ])
