import rclpy
from rclpy.node import Node
from my_interfaces.srv import Nhom4Srv


class CheckMemberServer(Node):

    def __init__(self):
        super().__init__('check_member_server')

        self.srv = self.create_service(
            Nhom4Srv,
            'check_name',
            self.check_callback
        )

        # Danh sách thành viên (name, mssv)
        self.members = [
            ('Example Student A', 10000001),
            ('Example Student B', 10000002),
            ('Example Student C', 10000003),
        ]

        self.get_logger().info('Check Member Server is ready.')

    def check_callback(self, request, response):
        for name, mssv in self.members:
            if request.name == name and request.mssv == mssv:
                response.result = 'OK'
                self.get_logger().info(f'Member found: {name}')
                return response

        response.result = 'Not found'
        self.get_logger().info('Member not found')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = CheckMemberServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

