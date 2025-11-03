from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os

def generate_launch_description():
    urdf_file = os.path.join(
        os.path.dirname(__file__), '..', 'urdf', 'turtlebot3_with_sensors.urdf'
    )
    
    urdf_content = open(urdf_file).read()
    
    # World 파일을 파라미터로 받기
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='/opt/ros/humble/share/gazebo_ros/worlds/empty.world',
        description='Gazebo world file path'
    )
    
    return LaunchDescription([
        world_arg,
        
        ExecuteProcess(
            cmd=['gzserver', LaunchConfiguration('world'), '--verbose',
                 '-s', 'libgazebo_ros_init.so',
                 '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['gzclient'],
            output='screen'
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{'robot_description': urdf_content}]
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'my_robot', '-file', urdf_file],
            output='screen'
        ),
        
        # ========== 여기부터 새로 추가 ==========
        # 3D LiDAR → 2D LaserScan 변환 + 필터링
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            parameters=[{
                'target_frame': 'base_scan',
                'transform_tolerance': 0.01,
                'min_height': 0.15,          # 바닥 제외 (15cm 이상)
                'max_height': 1.8,           # 천장 제외 (1.8m 이하)
                'angle_min': -3.14159,       # -180도
                'angle_max': 3.14159,        # +180도
                'angle_increment': 0.0087,   # 약 0.5도
                'scan_time': 0.1,
                'range_min': 0.3,            # 30cm 이하 제외
                'range_max': 30.0,           # 최대 30m
                'use_inf': True,
                'inf_epsilon': 1.0
            }],
            remappings=[
                ('cloud_in', '/velodyne_points'),  # 3D 입력
                ('scan', '/scan_filtered')         # 필터링된 2D 출력
            ],
            output='screen'
        )
        # ========== 여기까지 추가 ==========
    ])