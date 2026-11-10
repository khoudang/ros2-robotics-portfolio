import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class gui_toaDo(Node):

    def __init__(self):
        super().__init__('nhom2_send_hehe')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def lay_input(self):
        print("\nNhap toa do muon:")
        x = input("x [-1,1]: ")
        y = input("y [-1,1]: ")
        z = input("z [-1,1]: ")
        return x, y, z

    def xu_ly_gia_tri(self, v):
        return max(min(float(v), 1.0), -1.0)

    def tao_msg(self, x, y, z):
        msg = Twist()

        msg.linear.x = self.xu_ly_gia_tri(x)
        msg.linear.y = self.xu_ly_gia_tri(y)
        msg.angular.z = self.xu_ly_gia_tri(z)

        return msg

    def gui_lenh(self, msg):

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Da gui: x={msg.linear.x}, y={msg.linear.y}, theta={msg.angular.z}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = gui_toaDo()

    while rclpy.ok():

        x, y, z = node.lay_input()

        msg = node.tao_msg(x, y, z)

        node.gui_lenh(msg)

        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
