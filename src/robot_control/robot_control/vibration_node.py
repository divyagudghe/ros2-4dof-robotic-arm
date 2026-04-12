import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class VibrationNode(Node):
    def __init__(self):
        super().__init__('vibration_node')
        self.publisher_ = self.create_publisher(Float32, 'vibration', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.value = 1.0

    def publish_data(self):
        self.value += random.uniform(0.5, 1.5)

        if self.value > 10:
            self.value = 1.0

        msg = Float32()
        msg.data = self.value

        self.publisher_.publish(msg)
        self.get_logger().info(f"Vibration: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = VibrationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
