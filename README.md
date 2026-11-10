# CDRBvAI | Robotics & ROS 2

**Portfolio thực hành robot của [@khoudang](https://github.com/khoudang)** — từ giao tiếp giữa các node ROS 2, thiết kế message/service, đến điều khiển robot và mô phỏng mê cung với LiDAR trên Gazebo.

`Python` · `ROS 2` · `Gazebo` · `LiDAR` · `Robot control` · `Raspberry Pi`

## Những gì tôi đã thực hiện

### 01 — Giao tiếp publisher/subscriber

Xây dựng node phát và nhận dữ liệu, đóng gói thành ROS 2 package và sử dụng launch để khởi động nhiều node.

**Mã nguồn:** [Bài 1](Bài%201/ros2_khoi1/src/khoipkg)

### 02 — Custom message và service

Định nghĩa cấu trúc dữ liệu riêng bằng `.msg` và `.srv`; xây dựng publisher/subscriber và client/server để truyền và xử lý dữ liệu.

**Mã nguồn:** [Bài 2](Bài%202/FILE%20code)

### 03 — Điều khiển robot qua ROS 2

Truyền lệnh vận tốc bằng `geometry_msgs/Twist`, triển khai giao tiếp service và xử lý lệnh điều khiển robot. Phần điều khiển sử dụng NumPy và GPIO trên Raspberry Pi.

**Mã nguồn:**
- [Node gửi lệnh vận tốc](Bài%203/ros2_ws/ros2_ws/src/nhom2_pkg/nhom2_pkg/pub.py)
- [Node nhận lệnh và điều khiển](Bài%203/ros2_ws/ros2_ws/src/nhom2_pkg/nhom2_pkg/sub.py)
- [Service điều khiển](Bài%203/ros2_ws/ros2_ws/src/nhom2_pkg/nhom2_pkg/server.py)
- [Định nghĩa interface](Bài%203/ros2_ws/ros2_ws/src/nhom2_interfaces)

### 04 — Mô hình robot trên Gazebo

Mô tả robot bằng SDF để sử dụng trong môi trường mô phỏng.

**Mã nguồn:** [mecanum5.sdf](Bài%204/Code_Tuan4/mecanum5.sdf)

### 06 — Robot LiDAR di chuyển trong mê cung

Xây dựng môi trường mê cung và mô hình robot LiDAR bằng world/Xacro. Node Python đọc `LaserScan`, phân tích khoảng cách phía trước và bên trái, phát lệnh `Twist` để tránh vật cản và bám tường trái với hiệu chỉnh PD.

```text
LaserScan → Phân tích khoảng cách → Quyết định hướng đi → Twist
                                     ↑
                            Hiệu chỉnh bám tường PD
```

**Mã nguồn:**
- [Thuật toán bám tường trái](Bài%206/letrai.py)
- [Môi trường mê cung](Bài%206/maze.world)
- [Mô hình robot LiDAR](Bài%206/robot_lidar.urdf.xacro)

## Cấu trúc

```text
Bài 1/  ROS 2 publisher, subscriber, launch
Bài 2/  Custom message, service, client/server
Bài 3/  Workspace ROS 2 và điều khiển robot
Bài 4/  Mô hình SDF
Bài 6/  Mê cung, robot LiDAR, bám tường trái
```

## Môi trường

- ROS 2 và công cụ build `colcon`.
- Python với `rclpy`, các message package và interface tương ứng từng bài.
- Gazebo và Xacro cho các mô hình mô phỏng.
- NumPy, gpiozero và Raspberry Pi cho phần điều khiển GPIO ở Bài 3.

Đây là tập hợp các bài thực hành độc lập, không phải một ứng dụng cài đặt bằng một lệnh. Bố cục mã nguồn gốc được giữ để tiện đối chiếu từng bài.

## Kiểm tra bản công khai

- Đã kiểm tra cú pháp toàn bộ 35 file Python.
- Đã kiểm tra khả năng phân tích XML của 8 file XML/SDF/world/Xacro.
- Chưa xác minh lại build và chạy ROS 2/Gazebo trong môi trường công khai này; các kiểm tra trên không thay thế thử nghiệm robot hoặc mô phỏng.
- Bài 2 là các file ví dụ, cần bổ sung package/workspace để build interface.
- Bài 3 có package `my_pkg` nằm ngoài `src`; một số entry point trong package này còn tham chiếu module không có trong bản nguồn.
- Bài 6 sử dụng định danh `maze_robot`; bridge/launch bên ngoài cần dùng cùng tên và topic.

## Ghi chú

Thông tin cá nhân trong dữ liệu mẫu được thay bằng dữ liệu giả. Repo không chứa báo cáo, file nén hoặc thư mục build/log/cache. License và thông báo bản quyền có sẵn được giữ nguyên trong từng package.

**An toàn:** các node điều khiển GPIO có thể tác động lên phần cứng. Chỉ chạy trên robot thật sau khi kiểm tra cấu hình chân, hướng quay và cơ chế dừng.
