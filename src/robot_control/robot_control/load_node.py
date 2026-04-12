import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class LoadNode(Node):
    def _init_(self):
        super()._init_('load_node')
        self.publisher_ = self.create_publisher(Float32, 'load', 10)
        self.timer = self.create_timer(1.0, self.publish_data)
        self.value = 30.0

    def publish_data(self):
        self.value += random.uniform(2.0, 6.0)

        if self.value > 100:
            self.value = 20.0

        msg = Float32()
        msg.data = self.value

        self.publisher_.publish(msg)
        self.get_logger().info(f"Load: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = LoadNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if _name_ == '__main__':
    main()
