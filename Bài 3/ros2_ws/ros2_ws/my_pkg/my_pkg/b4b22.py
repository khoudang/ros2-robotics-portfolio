import rclpy
from rclpy.node import Node
from my_interfaces.srv import Nhom4Srv


class CheckClient(Node):

    def __init__(self):
        super().__init__('check_member_client')

        self.client = self.create_client(Nhom4Srv, 'check_name')

        while not self.client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Waiting for service check_name...')

        # Dữ liệu gửi (bạn có thể thay đổi theo ý)
        self.name = 'Example Student B'
        self.email = 'student_b@example.com'
        self.mssv = 10000002

        self.timer = self.create_timer(1.0, self.send_request)  # gửi mỗi 1 giây
        self.busy = False  # tránh spam khi request chưa trả về

    def send_request(self):
        if self.busy:
            return

        req = Nhom4Srv.Request()
        req.name = self.name
        req.email = self.email
        req.mssv = self.mssv

        self.get_logger().info("Sending request...")
        self.future = self.client.call_async(req)
        self.future.add_done_callback(self.response_callback)

        self.busy = True

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Result from server: {response.result}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

        self.busy = False


def main(args=None):
    rclpy.init(args=args)
    node = CheckClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

