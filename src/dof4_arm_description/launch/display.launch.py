from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():

    urdf_path = os.path.expanduser(
        '~/ros2-4dof-robotic-arm/src/dof4_arm_description/urdf/dof4_arm.urdf'
    )

    with open(urdf_path, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_description}],
        ),

        # 🔥 THIS WAS MISSING BEFORE
        Node(
            package='robot_control',
            executable='motion_node',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        )

    ])
