# Industrial Robot Preventive Maintenance System (ROS2 + PLC Logic)

---

## 🚀 Overview

This project presents a *low-cost preventive maintenance system* for industrial robotic arms using ROS2 and PLC-style logic.

It simulates how real industrial systems monitor robot health and automatically respond to unsafe conditions to improve reliability and lifespan.

---

## ⚠️ Problem Statement

In small and medium-scale industries:

- Advanced monitoring systems are expensive
- Robots often run without real-time health tracking
- Failures occur unexpectedly
- Maintenance is reactive instead of preventive

This leads to:
- Reduced lifespan of robotic systems
- Increased downtime
- Higher maintenance costs

---

## 💡 Solution

This system introduces a *sensor-driven control mechanism* that continuously monitors:

- 🌡️ Temperature  
- ⚙️ Load  
- 📳 Vibration  

Based on real-time data:

- Robot *stops automatically* under unsafe conditions  
- System *waits and recovers* when conditions normalize  
- Logic mimics *industrial PLC safety interlocks*

---

## 🎯 Objectives

- Increase robotic arm lifespan  
- Reduce unexpected failures  
- Implement PLC-style industrial logic in ROS2  
- Generate data for future ML-based predictive maintenance  

---

## 🧠 System Architecture

The system consists of:

### 1. Motion Node
- Controls robotic arm movement
- Executes pick-and-place operation

### 2. Sensor Logic (Simulated)
- Generates temperature, load, vibration data
- Triggers fault conditions

### 3. Decision Logic
- Stops robot on:
  - High temperature
  - Overload
  - High vibration
- Restarts when safe

### 4. CSV Logger
- Stores real-time data
- Enables ML integration

---

## 🛠️ Technologies Used

- ROS2 (rclpy)
- Python
- URDF (Robot modeling)
- TF (Transform system)
- RViz (Visualization)
- PLC Concepts:
  - Timers
  - Interlocks
  - Conditional logic
- Ubuntu (Linux)

---

## 🎥 Demo

The working demonstration is included:

👉 final.webm

It shows:
- Normal operation
- Fault detection (temperature, load, vibration)
- Automatic stop and recovery

---

## 📊 Data Logging

Sensor data is recorded in:

👉 sensor_data.csv

This data can be used for:
- Analysis
- Machine Learning models
- Predictive maintenance systems

---

## 🔥 Real-World Impact

This project demonstrates how:

👉 *Low-cost software + basic sensing = industrial-level reliability*

It provides a scalable approach for industries that cannot afford expensive monitoring systems.

---

## 🚀 Future Scope

- Machine Learning integration for failure prediction  
- Real PLC hardware integration  
- Dashboard for live monitoring  
- IoT-based remote monitoring system  

---

## 👩‍💻 Author

*Divya Gudghe*  
Robotics & Industrial Automation | ROS2 | PLC Logic  

GitHub: https://github.com/divyagudghe
