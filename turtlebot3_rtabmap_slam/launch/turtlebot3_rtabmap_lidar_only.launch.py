#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    frame_id = LaunchConfiguration('frame_id')
    scan_cloud_topic = LaunchConfiguration('scan_cloud_topic')
    rviz = LaunchConfiguration('rviz')
    imu_topic = LaunchConfiguration('imu_topic')

    pkg_share = FindPackageShare('turtlebot3_rtabmap_slam')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        DeclareLaunchArgument(
            'frame_id',
            default_value='base_link',
            description='Robot base frame'
        ),
        DeclareLaunchArgument(
            'scan_cloud_topic',
            default_value='/velodyne_points',
            description='3D LiDAR point cloud topic'
        ),
        DeclareLaunchArgument(
            'rviz',
            default_value='true',
            description='Launch RViz2 for visualization'
        ),
        DeclareLaunchArgument(
            'imu_topic',
            default_value='/imu',
            description='IMU topic name'
        ),
        Node(
            package='rtabmap_ros',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'frame_id': frame_id,
                'subscribe_scan': False,
                'subscribe_scan_cloud': True,
                'scan_cloud_topic': scan_cloud_topic,
                'subscribe_odom_info': True,
                'subscribe_user_data': False,
                'approx_sync': True,
                'wait_imu_to_init': False,
                'imu_topic': imu_topic,
                'odom_topic': '/odom',
                # Optimized RTAB-Map parameters for 3D LiDAR SLAM
                'Reg/Strategy': 1,  # ICP registration
                'Reg/Force3DoF': True,  # 2D SLAM constraint
                'Grid/3D': True,  # 3D occupancy grid
                'Grid/RayTracing': True,  # Ray tracing for grid
                'Grid/RangeMax': 20.0,  # Max sensor range
                'Grid/FromDepth': False,  # Use LiDAR not depth
                'Icp/VoxelSize': 0.05,  # ICP voxel size
                'Icp/MaxCorrespondenceDistance': 0.1,
                'Icp/Strategy': 1,  # Point-to-plane ICP
                'Mem/IncrementalMemory': True,  # Mapping mode
                'RGBD/OptimizeFromGraphEnd': False,  # Optimization setting
                'Vis/MinInliers': 15,  # Visual features threshold
                'Vis/InlierDistance': 0.1,  # Visual inlier distance
                'Rtabmap/TimeThr': 0,  # No time limit for loop detection
                'Mem/RehearsalSimilarity': 0.30,  # Memory management
                'Optimizer/Slam2D': True,  # 2D optimization
                'Grid/NoiseFilteringRadius': 0.0,  # Noise filtering
                'Grid/NoiseFilteringMinNeighbors': 5
            }],
            remappings=[
                ('/scan_cloud', scan_cloud_topic),
                ('/odom', '/odom')
            ]
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([
                pkg_share, 'rviz', 'rtabmap_slam.rviz'
            ])],
            parameters=[{'use_sim_time': use_sim_time}],
            condition=None
        )
    ])
