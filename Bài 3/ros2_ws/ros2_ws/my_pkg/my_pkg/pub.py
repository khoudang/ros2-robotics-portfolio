import rclpy
from rclpy.node import Node
from std_msgs.msg import String


from my_interfaces.msg import Nhom4

import json

class MinimalPublisher(Node):
    # Tạo một node publisher, kế thừa từ lớp Node
    def __init__(self):
        super().__init__('bai2_pub1')
        # Khởi tạo node với tên là nhom4

        self.publisher_ = self.create_publisher(Nhom4, 'bai2', 20)
        # Tạo publisher gửi dữ liệu kiểu Nhom4 lên topic nhom4, hàng đợi 10 message

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # Cứ mỗi 0.5 giây sẽ gọi hàm timer_callback để gửi dữ liệu

        self.i = 0

    def timer_callback(self):
        msg = Nhom4()
        # Tạo một message mới theo định dạng Nhom4

        msg.name = "Example Student B"
        msg.email = "student_b@example.com"
        msg.mssv = 10000002
        # Gán thông tin cá nhân vào message

        self.publisher_.publish(msg)
        # Gửi message lên topic nhom4

        self.get_logger().info(
            'Ho va ten:%s, email:%s, mssv:%d ' %
            (msg.name, msg.email, msg.mssv)
        )
        # In log ra terminal để kiểm tra dữ liệu đã gửi

        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    # Giữ cho node chạy liên tục để tiếp tục gửi dữ liệu

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
