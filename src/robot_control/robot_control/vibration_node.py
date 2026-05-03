#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import math


class VibrationNode(Node):

    def __init__(self):
        super().__init__('vibration_node')

        self.pub = self.create_publisher(String, '/sensor/vibration', 10)
        self.timer = self.create_timer(1.0, self.update)

        self.t = 0
        self.threshold = 5.0

    def update(self):
        self.t += 1
        phase = (self.t + 8) % 30  # phase shift vs temperature

        if phase < 20:
            value = 2.5 + 2.0 * math.sin(phase * 0.3)     # mostly normal
        else:
            value = 7.5 + 1.5 * math.sin((phase - 20) * 0.6)  # abnormal window

        value = round(value, 2)
        state = 'abnormal' if value >= self.threshold else 'normal'

        msg = String()
        msg.data = f"{value},{state}"
        self.pub.publish(msg)

        self.get_logger().info(f"[VIB] {value} → {state}")


def main(args=None):
    rclpy.init(args=args)
    node = VibrationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
