import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperatureNode(Node):
    def __init__(self):
        super().__init__('temperature_node')
        self.publisher_ = self.create_publisher(Float32, 'temperature', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.value = 25.0

    def publish_data(self):
        self.value += random.uniform(1.0, 5.0)

        if self.value > 80:
            self.value = 20.0

        msg = Float32()
        msg.data = self.value

        self.publisher_.publish(msg)
        self.get_logger().info(f"Temperature: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = TemperatureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
