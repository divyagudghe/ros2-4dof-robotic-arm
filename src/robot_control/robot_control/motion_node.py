#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState


JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']

WAYPOINTS = [
    (0.00, 0.30, -0.20, 0.00, 15),
    (0.55, 0.50, -0.40, 0.00, 20),
    (0.55, 0.80, -0.75, 0.00, 20),
    (0.55, 0.80, -0.75, 0.60, 15),
    (0.55, 0.50, -0.40, 0.60, 20),
    (-0.55, 0.50, -0.40, 0.60, 25),
    (-0.55, 0.80, -0.75, 0.60, 20),
    (-0.55, 0.80, -0.75, -0.10, 15),
    (-0.55, 0.40, -0.25, 0.00, 20),
    (0.00, 0.30, -0.20, 0.00, 15),
]

SPEED_FAST = 20
SPEED_SLOW = 70
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState


JOINT_NAMES = ['joint1', 'joint2', 'joint3', 'joint4']

WAYPOINTS = [
    ( 0.00, -0.80,  0.60,  0.00, 20),
    ( 0.90, -0.50,  0.40,  0.00, 20),
    ( 0.90, -0.20,  0.90,  0.00, 20),
    ( 0.90, -0.20,  0.90,  1.57, 15),
    ( 0.90, -0.70,  0.50,  1.57, 20),
    (-0.90, -0.70,  0.50,  1.57, 25),
    (-0.90, -0.20,  0.90,  1.57, 20),
    (-0.90, -0.20,  0.90,  0.00, 15),
    (-0.90, -0.80,  0.60,  0.00, 20),
    ( 0.00, -0.80,  0.60,  0.00, 15),
]

FAST = 20
SLOW = 60


class MotionNode(Node):

    def __init__(self):
        super().__init__('motion_node')

        self.create_subscription(String, '/system_action', self.action_cb, 10)
        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        self.action = 'RUNNING'

        self.i = 0
        self.next_i = 1
        self.hold = 0
        self.move = 0

        self.pos = list(WAYPOINTS[0][:4])
        self.freeze = list(self.pos)

        # 🔥 FIXED TIMING (was 0.1 → now stable)
        self.timer = self.create_timer(0.15, self.update)

    def action_cb(self, msg):
        new = msg.data.strip()

        if new == self.action:
            return

        self.action = new

        if self.action == 'STOP SYSTEM':
            self.freeze = list(self.pos)

    def update(self):

        if self.action == 'STOP SYSTEM':
            self.publish(self.freeze)
            return

        speed = SLOW if self.action == 'WARNING' else FAST

        wp = WAYPOINTS[self.i]
        nxt = WAYPOINTS[self.next_i]

        if self.hold < wp[4]:
            self.hold += 1
            self.publish(wp[:4])
            return

        self.move += 1
        t = min(self.move / speed, 1.0)

        self.pos = [
            wp[j] + (nxt[j] - wp[j]) * t
            for j in range(4)
        ]

        if t >= 1.0:
            self.i = self.next_i
            self.next_i = (self.next_i + 1) % len(WAYPOINTS)
            self.move = 0
            self.hold = 0

        self.publish(self.pos)

    def publish(self, pos):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = JOINT_NAMES
        msg.position = pos
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
