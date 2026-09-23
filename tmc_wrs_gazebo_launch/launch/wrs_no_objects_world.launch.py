#!/usr/bin/env python3
# -*-encoding:UTF-8-*-
"""WRS2020 field without task objects. See include/wrs_common.launch.py."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    wrs_common_path = os.path.join(
        get_package_share_directory("tmc_wrs_gazebo_launch"),
        "launch", "include", "wrs_common.launch.py",
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(wrs_common_path),
            launch_arguments={"spawn_objects": "false"}.items(),
        ),
    ])
