import rclpy
from rclpy.node import Node
import numpy as np
from gpiozero import PWMLED
from nhom2_interfaces.srv import Nhom2


in1_a = PWMLED(17);  in1_b = PWMLED(27)
in4_a = PWMLED(23); in4_b = PWMLED(24)
in3_a = PWMLED(20); in3_b = PWMLED(21)
in2_a = PWMLED(19);  in2_b = PWMLED(16)


l = [0.088, 0.088, 0.088, 0.088]
r = 0.024
pi = np.pi

alpha = [0.739, -0.739, -2.401, 2.401]
beta  = [0.831, -0.831, 0.831, -0.831]
gama  = np.array([-pi/4, pi/4, -pi/4, pi/4])


J1 = np.array([
    [np.sin(alpha[0]+beta[0]+gama[0]), -np.cos(alpha[0]+beta[0]+gama[0]), -l[0]*np.cos(beta[0]+gama[0])],
    [np.sin(alpha[1]+beta[1]+gama[1]), -np.cos(alpha[1]+beta[1]+gama[1]), -l[1]*np.cos(beta[1]+gama[1])],
    [np.sin(alpha[2]+beta[2]+gama[2]), -np.cos(alpha[2]+beta[2]+gama[2]), -l[2]*np.cos(beta[2]+gama[2])],
    [np.sin(alpha[3]+beta[3]+gama[3]), -np.cos(alpha[3]+beta[3]+gama[3]), -l[3]*np.cos(beta[3]+gama[3])]
])

J2 = r * np.diag(np.cos(gama))


class server_nhom2(Node):

    def __init__(self):
        super().__init__('nhom2_server')

        self.srv = self.create_service(Nhom2, 'van_toc', self.xu_ly_request)

        self.watchdog_timeout = 2.0

        self.watchdog = self.create_timer(
            self.watchdog_timeout, self.dungXe
        )

        self.get_logger().info('Start')

    def dieu_khien_banh(self, pwm, led_a, led_b):

        val = min(abs(float(pwm)), 1.0)

        if pwm >= 0:
            led_a.value = 0.0
            led_b.value = val
        else:
            led_a.value = val
            led_b.value = 0.0

    def dk_xee(self, p1, p2, p3, p4):

        self.dieu_khien_banh(p1, in1_a, in1_b)
        self.dieu_khien_banh(p2, in2_a, in2_b)
        self.dieu_khien_banh(p3, in3_a, in3_b)
        self.dieu_khien_banh(p4, in4_a, in4_b)

    def tinh_van_toc_banh(self, vx, vy, w):

        VR = np.array([vx, w, vy])

        phi_dot = np.linalg.inv(J2) @ J1 @ VR

        return phi_dot

    def xu_ly_request(self, request, response):

        self.watchdog.cancel()

        vx = request.x
        vy = -request.y
        w  = -request.theta

        phi = self.tinh_van_toc_banh(vx, vy, w)

        self.dk_xee(phi[0], phi[1], phi[2], phi[3])

        self.get_logger().info(
            f'Value x:{vx}, y:{vy}, theta:{w}'
        )

        self.watchdog = self.create_timer(
            self.watchdog_timeout, self.dungXe
        )

        response.success = True

        return response

    def dungXe(self):

        self.dk_xee(0, 0, 0, 0)

        self.get_logger().warn('Overtime: Stop!!!')

        self.watchdog.cancel()


def main(args=None):

    rclpy.init(args=args)

    node = server_nhom2()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.dk_xee(0, 0, 0, 0)

        node.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
