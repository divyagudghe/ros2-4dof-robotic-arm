# ROS2 4DOF Robotic Arm Simulation

This project demonstrates a 4 Degree of Freedom (4DOF) robotic arm modeled using URDF and visualized in RViz using ROS2.

## Features
- 4 DOF robotic arm
- URDF robot description
- STL mesh integration
- TF transformations
- RViz visualization
- ROS2 launch file

## Technologies
- ROS2
- URDF
- RViz
- TF
- Ubuntu Linux

## Project Structure

src/
 └── dof4_arm_description
      ├── urdf
      ├── meshes
      ├── launch
      ├── CMakeLists.txt
      └── package.xml

## Run the Project

Clone the repository:

git clone https://github.com/divyagudghe/ros2-4dof-robotic-arm.git

Build workspace:

colcon build

Launch visualization:

ros2 launch dof4_arm_description display.launch.py

## Author
Divya Gudgh
