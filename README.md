# tmc_wrs_gazebo

WRS2020 (Service Robotics Partner Robot Challenge, Real Space) field for the HSR simulator.

Branches:

- `jazzy`: ROS 2 Jazzy + Gazebo Harmonic (gz-sim 8, via `ros_gz`)
- `ignition/humble`: ROS 2 Humble + Gazebo Sim (Fortress)
- `classic/humble`: ROS 2 Humble + Gazebo Classic
- `master`: ROS 1

## Packages

- `tmc_wrs_gazebo_worlds`: world (`wrs2020*.world`, generated from xacro at build time), models, map and the `spawn_objects` node
- `tmc_wrs_gazebo_launch`: launch files (`wrs_practice0.launch.py`, `wrs_no_objects_world.launch.py`, `include/wrs_common.launch.py`)
- `tmc_wrs_gazebo`: meta package

## Usage with hsr-jazzy-docker

The `jazzy` branch is verified with https://github.com/ry0hei-kobayashi/hsr-jazzy-docker .
Mount this repository (and optionally `hsrb_wrs_gazebo_launch`) under `/hsr_ros2_ws/src/additional_pkg/`
(see `docker-compose.yml` there); the entrypoint runs `rosdep install` + `colcon build` for it at startup.

```bash
docker exec -it hsrb_jazzy bash
source /hsr_ros2_ws/install/setup.bash
ros2 launch tmc_wrs_gazebo_launch wrs_practice0.launch.py
```

See `tmc_wrs_gazebo_launch/README.md` for the launch arguments.

## LICENSE

This software except object models is released under the BSD 3-Clause Clear License, see LICENSE.txt.

Regarding the license of object models, see README.md in the tmc_wrs_gazebo_worlds package.
