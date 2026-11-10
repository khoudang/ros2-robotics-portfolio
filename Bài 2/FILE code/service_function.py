from my_interfaces.srv import AddThreeInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddThreeInts, 'Nhom8', self.add_three_ints_callback)
        self.group_members = [
            {"name": "student_a", "id": 10000001},
            {"name": "student_b", "id": 10000002},
            {"name": "student_c", "id": 10000003},
        ]

    def add_three_ints_callback(self, request, response):
        for member in self.group_members:
            if request.name == member["name"] and request.id == member["id"]:
                response.result = "OK"
                return response

        response.result = "Not found"
        return response


def main():
    rclpy.init()

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
