from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Load URDF file
    robot_description = ParameterValue(
        Command([
            'cat ',
            PathJoinSubstitution([
                FindPackageShare('dof4_arm_description'),
                'urdf',
                'dof4_arm.urdf'
            ])
        ]),
        value_type=str
    )

    return LaunchDescription([

        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description
            }]
        ),

        # Joint State Publisher GUI
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
            parameters=[{
                'robot_description': robot_description
            }]
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            output='screen'
        ),
    ])
