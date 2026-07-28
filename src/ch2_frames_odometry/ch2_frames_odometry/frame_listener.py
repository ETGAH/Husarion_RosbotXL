import rclpy
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class FrameListener(Node):
    """Looks up odom -> laser once a second, a transform nobody publishes directly.

    TF2 chains it from the two links odom_broadcaster and static_sensor_frames each
    publish on their own.
    """

    def __init__(self):
        super().__init__('frame_listener')
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        try:
            t = self.tf_buffer.lookup_transform('odom', 'laser', Time())
        except TransformException as ex:
            self.get_logger().info(f'Cannot see odom -> laser yet: {ex}')
            return

        x = t.transform.translation.x
        y = t.transform.translation.y
        z = t.transform.translation.z
        self.get_logger().info(
            f'laser is at  x={x:+.2f}  y={y:+.2f}  z={z:+.2f}  in the odom frame'
        )


def main():
    rclpy.init()
    node = FrameListener()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
