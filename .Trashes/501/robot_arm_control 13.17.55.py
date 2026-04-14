from brian.motors import Motor
from robot_config import (
    MOTOR_PORT_FLIP_CUBE,
    MOTOR_PORT_ROTATE_PLATFORM,
    MOTOR_PORT_SENSOR_ARM,
    GEAR_RATIO_PLATFORM,
    GEAR_RATIO_FLIPPER,
    GEAR_RATIO_SENSOR_ARM,
    PLATFORM_TURN_90,
    PLATFORM_TURN_180,
    FLIPPER_ACTION_ANGLE
)
import time

class RobotArmControl:
    def __init__(self):
        self.motor_flip = self._init_motor(MOTOR_PORT_FLIP_CUBE, "Flip")
        self.motor_platform = self._init_motor(MOTOR_PORT_ROTATE_PLATFORM, "Platform")
        self.motor_arm = self._init_motor(MOTOR_PORT_SENSOR_ARM, "Sensor Arm")

    def _init_motor(self, port, name):
        try:
            m = Motor(port)
            if m.wait_until_ready(timeout_ms=2000):
                return m
            print(f"Warning: Motor {name} not ready.")
            return None
        except Exception as e:
            print(f"Error initializing {name}: {e}")
            return None

    def _get_motor_angle(self, target_angle, gear_ratio):
        """Calculates the required motor angle based on gear ratio."""
        return int(target_angle * gear_ratio)

    def rotate_platform_clockwise(self):
        angle = self._get_motor_angle(PLATFORM_TURN_90, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CW (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()

    def rotate_platform_counter_clockwise(self):
        angle = self._get_motor_angle(PLATFORM_TURN_90, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CCW (Motor Angle: -{angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(-angle, 360)
            self.motor_platform.wait_for_movement()
            
    def rotate_platform_180(self):
        angle = self._get_motor_angle(PLATFORM_TURN_180, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 180 (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()

    def flip_cube(self):
        angle = self._get_motor_angle(FLIPPER_ACTION_ANGLE, GEAR_RATIO_FLIPPER)
        print(f"Robot: Flip Cube (Motor Angle: {angle})")
        if self.motor_flip:
            self.motor_flip.rotate_by_angle(angle, 360) 
            self.motor_flip.wait_for_movement()

    def move_sensor_arm(self, target_arm_angle):
        # Assuming target_arm_angle is absolute physical angle (0, 30, 60...)
        motor_angle = self._get_motor_angle(target_arm_angle, GEAR_RATIO_SENSOR_ARM)
        print(f"Robot: Move Sensor Arm to {target_arm_angle} (Motor Pos: {motor_angle})")
        if self.motor_arm:
            self.motor_arm.rotate_to_angle(motor_angle, 200)
            self.motor_arm.wait_for_movement()

    def cleanup(self):
        if self.motor_flip: self.motor_flip.close_motor()
        if self.motor_platform: self.motor_platform.close_motor()
        if self.motor_arm: self.motor_arm.close_motor()