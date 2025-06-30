#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
    
    # Launch configuration variables
    use_sim_time = LaunchConfiguration('use_sim_time')
    frame_id = LaunchConfiguration('frame_id')
    scan_cloud_topic = LaunchConfiguration('scan_cloud_topic')
    rviz = LaunchConfiguration('rviz')
    rtabmap_viz = LaunchConfiguration('rtabmap_viz')
    imu_topic = LaunchConfiguration('imu_topic')
    
    # Get package directory
    pkg_share = FindPackageShare('turtlebot3_rtabmap_slam')
    
    return LaunchDescription([
        
        # Launch arguments
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
            'rtabmap_viz',
            default_value='false',  # Disabled by default to avoid crashes
            description='Launch RTAB-Map visualization'
        ),
        
        DeclareLaunchArgument(
            'imu_topic',
            default_value='/imu',
            description='IMU topic name'
        ),
        
        # Include RTAB-Map launch file with improved parameters
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('rtabmap_launch'),
                    'launch',
                    'rtabmap.launch.py'
                ])
            ]),
            launch_arguments={
                'use_sim_time': use_sim_time,
                'frame_id': frame_id,
                'subscribe_scan': 'false',
                'subscribe_scan_cloud': 'true',
                'scan_cloud_topic': scan_cloud_topic,
                'subscribe_odom_info': 'true',
                'subscribe_user_data': 'false',
                'approx_sync': 'true',
                'wait_imu_to_init': 'false',
                'imu_topic': imu_topic,
                'odom_topic': '/odom',
                'rtabmap_viz': rtabmap_viz,
                # Disable RGB-D and visual subscriptions for pure 3D LiDAR
                'subscribe_rgb': 'false',
                'subscribe_depth': 'false',
                'subscribe_rgbd': 'false',
                'subscribe_stereo': 'false',
                'rgbd_odometry': 'false',
                # Optimized RTAB-Map parameters for 3D LiDAR SLAM
                'args': '--delete_db_on_start ' + 
                       'Reg/Strategy 1 ' +
                       'Reg/Force3DoF true ' +
                       'Grid/3D true ' +
                       'Grid/RayTracing true ' +
                       'Grid/RangeMax 20.0 ' +
                       'Grid/FromDepth false ' +
                       'Icp/VoxelSize 0.05 ' +
                       'Icp/MaxCorrespondenceDistance 0.1 ' +
                       'Icp/Strategy 1 ' +
                       'Mem/IncrementalMemory true ' +
                       'RGBD/OptimizeFromGraphEnd false ' +
                       'Vis/MinInliers 15 ' +
                       'Vis/InlierDistance 0.1 ' +
                       'Rtabmap/TimeThr 0 ' +
                       'Mem/RehearsalSimilarity 0.30 ' +
                       'Optimizer/Slam2D true ' +
                       'Grid/NoiseFilteringRadius 0.0 ' +
                       'Grid/NoiseFilteringMinNeighbors 5'
            }.items()
        ),
        
        # Launch RViz2 with custom config
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', PathJoinSubstitution([
                pkg_share, 'rviz', 'rtabmap_slam.rviz'
            ])],
            parameters=[{'use_sim_time': use_sim_time}],
            condition=IfCondition(rviz),
            respawn=True,  # Restart if crashes
            respawn_delay=2.0
        )
    ])