import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool

class PLCNode(Node):
    def __init__(self):
        super().__init__('plc_node')

        self.temp = 0
        self.load = 0
        self.vibration = 0

        self.create_subscription(Float32, 'temperature', self.temp_cb, 10)
        self.create_subscription(Float32, 'load', self.load_cb, 10)
        self.create_subscription(Float32, 'vibration', self.vib_cb, 10)

        self.publisher_ = self.create_publisher(Bool, 'robot_stop', 10)

        self.timer = self.create_timer(1.0, self.logic)

    def temp_cb(self, msg):
        self.temp = msg.data

    def load_cb(self, msg):
        self.load = msg.data

    def vib_cb(self, msg):
        self.vibration = msg.data

    def logic(self):
        stop_msg = Bool()

        if self.temp > 70 or self.load > 80 or self.vibration > 5:
            stop_msg.data = True
            self.get_logger().info("CRITICAL → STOP")
        elif self.temp > 50 or self.load > 60 or self.vibration > 2:
            stop_msg.data = False
            self.get_logger().info("WARNING → RUN SLOW")
        else:
            stop_msg.data = False
            self.get_logger().info("NORMAL → RUN")

        self.publisher_.publish(stop_msg)


def main(args=None):
    rclpy.init(args=args)
    node = PLCNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
