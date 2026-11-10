import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import numpy as np
from gpiozero import PWMLED


# GIỮ NGUYÊN KHAI BÁO CHÂN
in1_a = PWMLED(17);  in1_b = PWMLED(27)
in4_a = PWMLED(23); in4_b = PWMLED(24)
in3_a = PWMLED(20); in3_b = PWMLED(21)
in2_a = PWMLED(19);  in2_b = PWMLED(16)


# THÔNG SỐ ROBOT
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


class tinhieu_Nhan(Node):

    def __init__(self):
        super().__init__('Nhan')

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.nhan_tin_hieu,
            10
        )

        self.watchdog_timeout = 2.0
        self.watchdog = self.create_timer(
            self.watchdog_timeout,
            self.dungXe
        )

        self.get_logger().info('Nhóm 2')

    # =============================
    # Motor control
    # =============================
    def dieu_khien_banh(self, pwm, led_a, led_b):

        val = min(abs(float(pwm)), 1.0)

        if pwm >= 0:
            led_a.value = 0.0
            led_b.value = val
        else:
            led_a.value = val
            led_b.value = 0.0

    def dk_xee(self, p):

        self.dieu_khien_banh(p[0], in1_a, in1_b)
        self.dieu_khien_banh(p[1], in2_a, in2_b)
        self.dieu_khien_banh(p[2], in3_a, in3_b)
        self.dieu_khien_banh(p[3], in4_a, in4_b)

    # =============================
    # Kinematics
    # =============================
    def tinh_van_toc_banh(self, vx, vy, w):

        VR = np.array([vx, w, vy])

        phi = np.linalg.inv(J2) @ J1 @ VR

        return phi

    def gioi_han_toc_do(self, phi):

        max_phi = np.max(np.abs(phi))

        if max_phi > 1.0:
            phi = phi / max_phi

        return phi

    # =============================
    # Subscriber callback
    # =============================
    def nhan_tin_hieu(self, msg):

        self.watchdog.cancel()

        vx = msg.linear.x
        vy = -msg.linear.y
        w  = -msg.angular.z

        phi = self.tinh_van_toc_banh(vx, vy, w)

        phi = self.gioi_han_toc_do(phi)

        self.dk_xee(phi)

        self.watchdog = self.create_timer(
            self.watchdog_timeout,
            self.dungXe
        )

    # =============================
    # Safety stop
    # =============================
    def dungXe(self):

        self.dk_xee([0,0,0,0])

        self.watchdog.cancel()


def main():

    rclpy.init()

    node = tinhieu_Nhan()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.dungXe()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
