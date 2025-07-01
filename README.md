# TurtleBot3 3‑D SLAM Workspace

> **Real‑time LiDAR‑Inertial Odometry and Dense 3‑D Mapping with LIO‑SAM on a simulated TurtleBot3**

This repository bundles everything you need to experiment with **3‑D SLAM** on a TurtleBot3 in Gazebo, combining:

* **TurtleBot3 simulation** (`turtlebot3_gazebo`, `turtlebot3_description`)
* A **3‑D LiDAR sensor plugin** mounted on the robot
* **LIO‑SAM** for real‑time LiDAR‑inertial odometry & local mapping

---

## Quick Start

> **Launch order matters!** Bring up the simulated robot **first**, then start the SLAM pipeline.

```bash
# 1 – Launch the TurtleBot3 world (must be running before anything else)
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 2 – Start LIO‑SAM (LiDAR‑Inertial Odometry & Mapping)
ros2 launch lio_sam run.launch.py
```

LIO‑SAM subscribes to `/points_raw` and `/imu/data` published by the robot **only after** the Gazebo world is up. Starting LIO‑SAM too early will cause missing‑topic errors and early shutdown.

---

## Prerequisites

| Component      | Tested Version             | Notes                                                         |
| -------------- | -------------------------- | ------------------------------------------------------------- |
| **ROS 2**      | Humble Hawksbill           | Iron & Jazzy should also work                                 |
| **Gazebo**     | Fortress (Classic)         | For Ignition users see branch `ignition`                      |
| **LIO‑SAM**    | Commit `d533c9f` (2025‑05) | Built from source in this workspace                           |
| **TurtleBot3** | Branch `foxy-devel`        | Set `export TURTLEBOT3_MODEL=burger` (or `waffle`, `burger3`) |

Install everything with:

```bash
sudo apt update && rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```

---

## 3‑D LiDAR Mount

The URDF adds an `os1_lidar` frame **15 cm** above the top plate. Adjust `description/turtlebot3_3d.urdf.xacro` if you want a different sensor or pose.

---

## Saving & Loading Maps

```bash
# Save the point‑cloud map produced by LIO‑SAM
ros2 service call /lio_sam/save_map std_srvs/srv/Trigger "{}"

# The map PCDs are written to ~/.ros/Map

# View them in RViz
rviz2 -d rviz/lio_sam_map.rviz
```

---

## Troubleshooting

| Symptom                                              | Remedy                                                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `Failed to find transform between base_link and map` | Ensure TFs are being republished by LIO‑SAM (`/tf`, `/tf_static`).                      |
| Gazebo simulation runs too slowly                    | Use headless rendering (`--headless`), or disable physics if you only need sensor data. |
| No points in RViz                                    | Check the LiDAR plugin topic: `ros2 topic echo /points_raw -n 1`.                       |

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss major changes or new features.

---

## License

Distributed under the **MIT License**. See `LICENSE` for details.

---

Happy mapping & exploring! ✨
