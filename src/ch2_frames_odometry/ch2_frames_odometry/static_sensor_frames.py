import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticSensorFrames(Node):
    """Publishes the LiDAR's fixed mounting position: 12 cm forward, 18 cm up, no rotation.

    Sent once, on /tf_static, which is latched — a node that starts later (RViz, Nav2)
    still receives it. A bolted-on sensor never moves relative to the body, so publishing
    it repeatedly would be pure waste.
    """

    def __init__(self):
        super().__init__('static_sensor_frames')
        self.broadcaster = StaticTransformBroadcaster(self)
        self.send_static_transform()
        self.get_logger().info(
            'Published static base_link -> laser (fires once, then latches)'
        )

    def send_static_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser'
        t.transform.translation.x = 0.12
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.18
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = StaticSensorFrames()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
