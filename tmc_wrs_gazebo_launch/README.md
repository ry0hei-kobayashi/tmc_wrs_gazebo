# tmc_wrs_gazebo_launch

Launch files for the HSR simulator with the WRS2020 field (ROS 2 Jazzy / Gazebo Harmonic).

```bash
ros2 launch tmc_wrs_gazebo_launch wrs_practice0.launch.py            # field + task objects (seed=1)
ros2 launch tmc_wrs_gazebo_launch wrs_no_objects_world.launch.py     # field only
```

Both files include `launch/include/wrs_common.launch.py`, which

- selects the world variant `wrs2020{_fast}{_highrtf}{_knob}.world` from `fast_physics`, `highrtf`, `with_handle`,
- includes `hsrb_gazebo_launch/launch/include/hsrb_gazebo_common.launch.py` (gz sim, HSR spawn, navigation, manipulation, teleop, rviz),
- bridges the gz world services to `/spawn_entity`, `/delete_entity`, `/set_entity_pose` (`ros_gz_interfaces`),
- runs `tmc_wrs_gazebo_worlds/spawn_objects`.

## Launch arguments

| argument | default | description |
|---|---|---|
| `seed` | 1 | random seed for object placement |
| `per_category` | 6 | objects per category in task 1 |
| `obstacles` | 4 | number of obstacles in task 2a |
| `per_row` | 6 | objects per row in task 2 |
| `spawn_objects` | true | set `false` to skip spawning task objects |
| `fast_physics` | false | use the `_fast` world (faster, less precise physics) |
| `highrtf` | false | use the `_highrtf` world (run faster than real time) |
| `with_handle` | true | use the `_knob` world (trofast drawers with knobs) |
| `rviz`, `use_navigation`, `use_manipulation`, `use_teleop`, `use_joy_node`, ... | | standard `hsrb_launch_utils` arguments, passed through to `hsrb_gazebo_common.launch.py` |

Example:

```bash
ros2 launch tmc_wrs_gazebo_launch wrs_practice0.launch.py seed:=10 fast_physics:=true highrtf:=true use_joy_node:=false
```

## Notes

- The task evaluator nodes of the ROS 1 version (`tmc_gazebo_task_evaluators`) have no ROS 2 / Gazebo Sim port and are not launched.
  `common.launch.py` references `hsrb_gazebo_task_evaluators`, which is not publicly available; it is kept for reference only.
- `config/hsr.rviz` is an RViz 1 (ROS 1) configuration kept from the original package and is not used by any launch file.
