#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import math


class TemperatureNode(Node):

    def __init__(self):
        super().__init__('temperature_node')

        self.pub = self.create_publisher(String, '/sensor/temperature', 10)
        self.timer = self.create_timer(1.0, self.update)

        self.t = 0
        self.threshold = 75.0

    def update(self):
        self.t += 1
        phase = self.t % 30

        if phase < 15:
            value = 55 + 15 * math.sin(phase * 0.4)
        else:
            value = 80 + 10 * math.sin((phase - 15) * 0.4)

        value = round(value, 2)
        state = 'abnormal' if value >= self.threshold else 'normal'

        msg = String()
        msg.data = f"{value},{state}"
        self.pub.publish(msg)

        self.get_logger().info(f"[TEMP] {value} → {state}")


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
