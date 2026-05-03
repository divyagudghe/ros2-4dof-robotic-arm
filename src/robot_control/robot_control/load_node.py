#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import math


class LoadNode(Node):

    def __init__(self):
        super().__init__('load_node')

        self.pub = self.create_publisher(String, '/sensor/load', 10)
        self.timer = self.create_timer(1.0, self.update)

        self.t = 0
        self.threshold = 10.0

    def update(self):
        self.t += 1
        phase = (self.t + 18) % 45

        if phase < 30:
            value = 6.0 + 3.5 * math.sin(phase * 0.2)
        else:
            value = 12.5 + 1.5 * math.sin((phase - 30) * 0.4)

        value = round(value, 2)
        state = 'abnormal' if value >= self.threshold else 'normal'

        msg = String()
        msg.data = f"{value},{state}"
        self.pub.publish(msg)

        self.get_logger().info(f"[LOAD] {value} → {state}")


def main(args=None):
    rclpy.init(args=args)
    node = LoadNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
