# tmc_wrs_gazebo

WRS2020 (Service Robotics Partner Robot Challenge, Real Space) field for the HSR simulator.

Branches:

- `jazzy`: ROS 2 Jazzy + Gazebo Harmonic (gz-sim 8, via `ros_gz`)


## Packages

- `tmc_wrs_gazebo_worlds`: world (`wrs2020*.world`, generated from xacro at build time), models, map and the `spawn_objects` node
- `tmc_wrs_gazebo_launch`: launch files (`wrs_practice0.launch.py`, `wrs_no_objects_world.launch.py`, `include/wrs_common.launch.py`)
- `tmc_wrs_gazebo`: meta package

See `tmc_wrs_gazebo_launch/README.md` for the launch arguments.

## LICENSE

This software except object models is released under the BSD 3-Clause Clear License, see LICENSE.txt.

Regarding the license of object models, see README.md in the tmc_wrs_gazebo_worlds package.
