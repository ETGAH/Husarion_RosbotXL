import math

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

RADIUS = 1.0
PERIOD = 20.0
OMEGA = 2.0 * math.pi / PERIOD


class OdomBroadcaster(Node):
    """Fakes odometry: publishes a moving odom -> base_link, tracing a 1 m circle every 20 s.

    Stands in for what robot_localization publishes for real in Phase B.
    """

    def __init__(self):
        super().__init__('odom_broadcaster')
        self.broadcaster = TransformBroadcaster(self)
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.02, self.broadcast_transform)
        self.get_logger().info(
            'Broadcasting a moving odom -> base_link (robot driving in a circle)'
        )

    def broadcast_transform(self):
        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9
        angle = OMEGA * elapsed
        yaw = angle + math.pi / 2.0

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = RADIUS * math.cos(angle)
        t.transform.translation.y = RADIUS * math.sin(angle)
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(yaw / 2.0)
        t.transform.rotation.w = math.cos(yaw / 2.0)
        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = OdomBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
