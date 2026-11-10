import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_interfaces.msg import Nhom4


class MinimalSubscriber(Node):
    # Tạo node subscriber
    def __init__(self):
        super().__init__('bai2_sub1')
        # Khởi tạo node với tên nhom4

        self.subscription = self.create_subscription(
            Nhom4,
            'bai2',
            self.listener_callback,
            20
        )
        # Tạo subscriber:
        # - Kiểu message: Nhom4
        # - Topic: nhom4
        # - Hàm xử lý: listener_callback

        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # Hàm xử lý khi nhận được message
        self.get_logger().info(
            'Ho va ten:%s, email:%s, mssv:%d ' %
            (msg.name, msg.email, msg.mssv)
        )
        # In dữ liệu nhận được ra terminal


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    # Giữ node luôn ở trạng thái lắng nghe dữ liệu

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
