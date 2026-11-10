import rclpy
from rclpy.node import Node
from nhom2_interfaces.srv import Nhom2


class vanToc_nhan(Node):

    def __init__(self):
        super().__init__('nhom2_service_client')

        self.cli = self.create_client(Nhom2, 'van_toc')

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Cho Server...')

    def nhap_toa_do(self):
        x = float(input("x [-1,1]: "))
        y = float(input("y [-1,1]: "))
        theta = float(input("theta [-1,1]: "))

        return (
            max(min(x, 1.0), -1.0),
            max(min(y, 1.0), -1.0),
            max(min(theta, 1.0), -1.0)
        )

    def tao_request(self, x, y, theta):
        req = Nhom2.Request()
        req.x = x
        req.y = y
        req.theta = theta
        return req

    def goi_service(self, request):
        return self.cli.call_async(request)


def main():

    rclpy.init()
    node = vanToc_nhan()

    while rclpy.ok():

        x, y, theta = node.nhap_toa_do()

        request = node.tao_request(x, y, theta)

        future = node.goi_service(request)

        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            print(f"Pi?: Success = {future.result().success}")
        else:
            print("Service loi!")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
