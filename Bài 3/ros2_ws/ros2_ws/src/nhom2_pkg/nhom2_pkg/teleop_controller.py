import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopController(Node):

    def __init__(self):
        super().__init__('teleop_controller')

        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

    def cmd_callback(self, msg):

        vx = msg.linear.x
        vy = msg.linear.y
        w  = msg.angular.z

        self.get_logger().info(
            f'vx={vx:.2f}  vy={vy:.2f}  w={w:.2f}'
        )

        # ở đây có thể tính vận tốc bánh xe
        # hoặc gửi sang node driver

def main(args=None):
    rclpy.init(args=args)
    node = TeleopController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
