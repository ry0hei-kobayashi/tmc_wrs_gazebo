#!/usr/bin/env python3
# -*-encoding:UTF-8-*-
"""
Common launch description for the WRS2020 HSR simulator (ROS 2 Jazzy / Gazebo Harmonic).

This is the ROS 2 counterpart of the ROS 1
``hsrb_wrs_gazebo_launch/launch/include/wrs_common.xml``.
It is meant to be included from thin wrapper launch files that only set default
argument values (e.g. ``wrs_practice0.launch.py`` here and
``hsrb_wrs_gazebo_launch/launch/wrs_practice*_tmc.launch.py``).

Launch arguments (in addition to the standard ones from ``hsrb_launch_utils``):
  fast_physics  : use the ``_fast`` world variant (less precise, faster physics)
  highrtf       : use the ``_highrtf`` world variant (run faster than real time)
  with_handle   : use the ``_knob`` world variant (trofast drawers with knobs)
  seed          : random seed for object placement
  per_category  : objects per category in task 1
  obstacles     : number of obstacles in task 2a
  per_row       : objects per row in task 2
  spawn_objects : whether to run the ``spawn_objects`` node at all
"""

import os

from ament_index_python.packages import get_package_share_directory

from hsrb_launch_utils.hsrb_launch_utils import declare_launch_arguments

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# Robot start pose in the WRS2020 field (same as ROS 1 "-x -2.1 -y 1.2 -z 0 -Y -1.57").
ROBOT_POSE = {
    "robot_pos_x": "-2.1",
    "robot_pos_y": "1.2",
    "robot_pos_z": "0.0",
    "robot_rpy_Y": "-1.57",
}


def declare_arguments():
    declared_arguments = declare_launch_arguments()

    declared_arguments.append(
        DeclareLaunchArgument("highrtf", default_value="false",
                              description="Run the simulator faster than real time"))
    declared_arguments.append(
        DeclareLaunchArgument("with_handle", default_value="true",
                              description="Use trofast drawers with knobs (_knob world)"))
    declared_arguments.append(
        DeclareLaunchArgument("seed", default_value="1",
                              description="Random seed for object placement"))
    declared_arguments.append(
        DeclareLaunchArgument("per_category", default_value="6",
                              description="Objects per category in task 1"))
    declared_arguments.append(
        DeclareLaunchArgument("obstacles", default_value="4",
                              description="Number of obstacles in task 2a"))
    declared_arguments.append(
        DeclareLaunchArgument("per_row", default_value="6",
                              description="Objects per row in task 2"))
    declared_arguments.append(
        DeclareLaunchArgument("spawn_objects", default_value="true",
                              description="Spawn task objects into the world"))

    return declared_arguments


def _is_true(context, name):
    return context.perform_substitution(LaunchConfiguration(name)).lower() in ("true", "1")


def launch_gazebo(context):
    """Select the world from fast_physics/highrtf/with_handle and include hsrb_gazebo_common."""
    suffix = ""
    if _is_true(context, "fast_physics"):
        suffix += "_fast"
    if _is_true(context, "highrtf"):
        suffix += "_highrtf"
    if _is_true(context, "with_handle"):
        suffix += "_knob"

    worlds_dir = get_package_share_directory("tmc_wrs_gazebo_worlds")
    world_name = os.path.join(worlds_dir, "worlds", f"wrs2020{suffix}.world")

    hsrb_gazebo_common_path = os.path.join(
        get_package_share_directory("hsrb_gazebo_launch"),
        "launch", "include", "hsrb_gazebo_common.launch.py",
    )

    return [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(hsrb_gazebo_common_path),
            launch_arguments={
                **ROBOT_POSE,
                "map": os.path.join(worlds_dir, "maps", "wrs2020", "map.yaml"),
                "world_name": world_name,
            }.items(),
        ),
    ]


def generate_launch_description():
    # Bridge the gz world services so that spawn_objects (and users) can use
    # /spawn_entity, /delete_entity and /set_entity_pose from ROS 2.
    # The world in wrs2020.world.xacro is named "default".
    bridge_spawn_entity_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="bridge_spawn_entity",
        output="screen",
        arguments=[
            "/world/default/create@ros_gz_interfaces/srv/SpawnEntity",
            "/world/default/remove@ros_gz_interfaces/srv/DeleteEntity",
            "/world/default/set_pose@ros_gz_interfaces/srv/SetEntityPose",
        ],
        remappings=[
            ("/world/default/create", "/spawn_entity"),
            ("/world/default/remove", "/delete_entity"),
            ("/world/default/set_pose", "/set_entity_pose"),
        ],
    )

    spawn_objects_node = Node(
        package="tmc_wrs_gazebo_worlds",
        executable="spawn_objects",
        name="spawn_objects",
        output="screen",
        arguments=[
            "--seed", LaunchConfiguration("seed"),
            "--percategory", LaunchConfiguration("per_category"),
            "--obstacles", LaunchConfiguration("obstacles"),
            "--perrow", LaunchConfiguration("per_row"),
        ],
        condition=IfCondition(LaunchConfiguration("spawn_objects")),
    )

    # NOTE: The ROS 1 version additionally launched task evaluator nodes from
    # tmc_gazebo_task_evaluators (object_in_box_detector for trofast_1/2/3,
    # wrc_stair_like_drawer, wrc_container_a/b, wrc_tray_1/2, wrc_bin_green/black,
    # wrc_frame and person_standing*, undesired_contact_detector, wrs_score_counter,
    # wrs_camera_controller). No ROS 2 / Gazebo Sim port of that package exists,
    # so they are not launched here. See hsrb_wrs_gazebo_launch (ROS 1 master branch)
    # launch/include/wrs_common.xml for the exact parameters if you port them.

    return LaunchDescription(
        declare_arguments()
        + [
            OpaqueFunction(function=launch_gazebo),
            bridge_spawn_entity_node,
            spawn_objects_node,
        ]
    )
