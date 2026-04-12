import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import random
import csv
import time

class MotionNode(Node):

    def __init__(self):
        super().__init__('motion_node')

        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.02, self.publish_joint_states)

        self.step = 0

        # INITIAL SENSOR VALUES
        self.temperature = 30.0
        self.load = 5.0
        self.vibration = 0.2

        # PLC STATE
        self.robot_enabled = True
        self.cooldown_counter = 0

        # CSV LOGGING
        self.file = open('sensor_data.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['time','temperature','load','vibration','status'])
        self.start_time = time.time()

        self.joint_names = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'left_finger_joint',
            'right_finger_joint'
        ]

    def update_sensors(self):
        # REALISTIC SENSOR CHANGE
        self.temperature += random.uniform(-0.5, 0.5)
        self.load += random.uniform(-0.2, 0.2)
        self.vibration += random.uniform(-0.05, 0.05)

        # LIMIT VALUES
        self.temperature = max(20, min(self.temperature, 70))
        self.load = max(2, min(self.load, 12))
        self.vibration = max(0.1, min(self.vibration, 1.0))

    def plc_logic(self):

        if self.temperature > 55 and self.robot_enabled:
            self.get_logger().info("⚠️ High Temp → STOP")
            self.robot_enabled = False
            self.cooldown_counter = 100

        if self.load > 10 and self.robot_enabled:
            self.get_logger().info("⚠️ Overload → STOP")
            self.robot_enabled = False
            self.cooldown_counter = 100

        if self.vibration > 0.8 and self.robot_enabled:
            self.get_logger().info("⚠️ High Vibration → STOP")
            self.robot_enabled = False
            self.cooldown_counter = 100

        # COOL DOWN
        if not self.robot_enabled:
            self.cooldown_counter -= 1

            if self.cooldown_counter <= 0:
                self.get_logger().info("✅ System Normal → START")
                self.robot_enabled = True

    def publish_joint_states(self):

        # UPDATE SENSOR
        self.update_sensors()

        # APPLY LOGIC
        self.plc_logic()

        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        # DETERMINE STATUS FOR CSV
        status = "normal"
        if not self.robot_enabled:
            status = "failure"

        current_time = round(time.time() - self.start_time, 2)

        self.writer.writerow([
            current_time,
            round(self.temperature,2),
            round(self.load,2),
            round(self.vibration,2),
            status
        ])

        # STOP CONDITION
        if not self.robot_enabled:
            msg.position = [0.0, 0.2, 1.0, 0.0, 0.04, 0.04]
            self.publisher_.publish(msg)
            return

        # NORMAL MOTION
        if self.step < 40:
            msg.position = [0.0, 0.2, 1.0, 0.0, 0.04, 0.04]

        elif self.step < 80:
            msg.position = [0.0, 0.5, 1.1, 0.0, 0.04, 0.04]

        elif self.step < 120:
            msg.position = [0.0, 0.7, 0.8, 0.0, 0.04, 0.04]

        elif self.step < 150:
            msg.position = [0.0, 0.7, 0.8, 0.0, 0.0, 0.0]

        elif self.step < 190:
            msg.position = [0.0, 0.4, 1.1, 0.0, 0.0, 0.0]

        elif self.step < 230:
            msg.position = [0.5, 0.4, 1.1, 0.0, 0.0, 0.0]

        elif self.step < 260:
            msg.position = [0.5, 0.4, 1.1, 0.0, 0.04, 0.04]

        elif self.step < 300:
            msg.position = [0.0, 0.2, 1.0, 0.0, 0.04, 0.04]

        else:
            self.step = 0
            return

        self.publisher_.publish(msg)
        self.step += 1


def main(args=None):
    rclpy.init(args=args)
    node = MotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
