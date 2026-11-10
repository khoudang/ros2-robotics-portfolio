#!/usr/bin/env python3
import math
from typing import Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class LeftWallFollower(Node): 
    # --- Hằng số Cấu hình ---
    left_wall = 0.05
    front_dist = 0.25
    x_speed = 0.5
    z_speed = 0.5

    # --- Hệ số PID (PD) ---
    KP = 4.0
    KD = 1.0

    def __init__(self) -> None:
        super().__init__('left_wall_follower')
 
        self._scan_sub = self.create_subscription(
            LaserScan,
            '/maze_robot/scan',
            self._scan_callback,
            10
        )
        self._cmd_pub = self.create_publisher(
            Twist,
            '/model/maze_robot/cmd_vel',
            10
        )
 
        self._timer = self.create_timer(0.1, self._navigate)
 
        self._latest_scan: Optional[LaserScan] = None
        self._prev_error: float = 0.0

    def _scan_callback(self, msg: LaserScan) -> None: 
        self._latest_scan = msg

    def _get_range_at_angle(self, scan: LaserScan, angle_deg: float) -> float: 
        angle_rad = math.radians(angle_deg)
        index = int((angle_rad - scan.angle_min) / scan.angle_increment)

        if not (0 <= index < len(scan.ranges)):
            return float('inf')

        value = scan.ranges[index]

        if math.isinf(value) or math.isnan(value):
            return scan.range_max

        return value

    def min_dist(self, scan: LaserScan, start_deg: int, end_deg: int) -> float: 
        return min(
            (self._get_range_at_angle(scan, angle) for angle in range(start_deg, end_deg)),
            default=float('inf')
        )

    def _navigate(self) -> None: 
        if self._latest_scan is None:
            return

        scan = self._latest_scan
        cmd = Twist()
 
        dist_front = self.min_dist(scan, -25, 25)
        dist_left = self.min_dist(scan, 50, 130)
         
        dist_front_left = min(
            self._get_range_at_angle(scan, 25),
            self._get_range_at_angle(scan, 45)
        )
 
        if dist_front < self.front_dist: 
            cmd.linear.x = 0.05
            cmd.angular.z = -self.z_speed

        elif dist_left > 0.1: 
            cmd.linear.x = 0.1
            cmd.angular.z = 0.9

        else: 
            current_error = dist_left - self.left_wall
            derivative = current_error - self._prev_error
            self._prev_error = current_error

            correction = (self.KP * current_error) + (self.KD * derivative)

            cmd.linear.x = self.x_speed
            cmd.angular.z = correction
 
            if dist_front_left < 0.22:
                cmd.angular.z -= 0.5
 
            cmd.angular.z = max(-1, min(1, cmd.angular.z)) 
        self._cmd_pub.publish(cmd)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = LeftWallFollower()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt: 
        pass
    finally:
        node.destroy_node() 
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
