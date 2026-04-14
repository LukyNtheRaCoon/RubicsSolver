import brian.motors as motors
from robot_config import (
    MOTOR_PORT_FLIP_CUBE,
    MOTOR_PORT_ROTATE_PLATFORM,
    MOTOR_PORT_SENSOR_ARM,
    GEAR_RATIO_PLATFORM,
    GEAR_RATIO_FLIPPER,
    GEAR_RATIO_SENSOR_ARM,
    PLATFORM_TURN_90,
    PLATFORM_TURN_180,
    FLIPPER_ACTION_ANGLE,
    HOMING_SPEED_FLIP,
    HOMING_SPEED_PLATFORM,
    HOMING_SPEED_ARM,
    ENABLE_HOMING_ON_STARTUP
)
import time

class RobotArmControl:
    def __init__(self):
        # Initialize motors with specific classes as per documentation
        self.motor_flip = motors.EV3MediumMotor(MOTOR_PORT_FLIP_CUBE)
        self.motor_platform = motors.EV3LargeMotor(MOTOR_PORT_ROTATE_PLATFORM)
        self.motor_arm = motors.EV3LargeMotor(MOTOR_PORT_SENSOR_ARM)

        if ENABLE_HOMING_ON_STARTUP:
            print("Starting Homing Sequence...")
            self.home_motors()
            print("Homing Complete.")

    def _init_motor(self, motor_class, port, name):
        try:
            m = motor_class(port)
            if m.wait_until_ready(timeout_ms=2000):
                return m
            print(f"Warning: Motor {name} not ready on port {port}.")
            return None
        except Exception as e:
            print(f"Error initializing {name}: {e}")
            return None

    def _home_single_motor(self, motor, speed, name):
        """
        Moves motor at 'speed' until it stalls, then resets angle to 0.
        Positive speed = forward, Negative speed = backward.
        """
        if not motor:
            return

        print(f"Homing {name}...")
        # Run blindly
        motor.wait_until_ready()
        motor.run_at_speed(speed)
        
        # Wait until stalled
        stalled_count = 0
        while True:
            if motor.is_stalled():
                stalled_count += 1
            else:
                stalled_count = 0
            
            # Require persistent stall to avoid noise
            if stalled_count > 5:
                break
            time.sleep(0.05)
        
        motor.hold()
        motor.reset_angle(0)
        print(f"  {name} Homed.")

    def home_motors(self):
        # NOTE: Adjust signs (-/+) depending on where your physical stops are!
        # Currently assuming 'backward' (negative speed) is the home position.
        
        # 1. Home Arm first (to move it out of the way if needed)
        self._home_single_motor(self.motor_arm, -HOMING_SPEED_ARM, "Sensor Arm")
        
        # 2. Home Flipper
        self._home_single_motor(self.motor_flip, -HOMING_SPEED_FLIP, "Flipper")
        
        # 3. Platform usually doesn't have a stop, but if it does:
        # self._home_single_motor(self.motor_platform, -HOMING_SPEED_PLATFORM, "Platform")
        # For now, we assume Platform 0 is wherever it started, or we just reset it:
        if self.motor_platform:
            self.motor_platform.reset_angle(0)
            print("  Platform Zeroed (Current Pos).")

    def _get_motor_angle(self, target_angle, gear_ratio):
        """Calculates the required motor angle based on gear ratio."""
        return int(target_angle * gear_ratio)

    def rotate_platform_clockwise(self):
        angle = self._get_motor_angle(PLATFORM_TURN_90, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CW (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()

    def rotate_platform_counter_clockwise(self):
        angle = self._get_motor_angle(PLATFORM_TURN_90, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CCW (Motor Angle: -{angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(-angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()
            
    def rotate_platform_180(self):
        angle = self._get_motor_angle(PLATFORM_TURN_180, GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 180 (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()

    def flip_cube(self):
        angle = self._get_motor_angle(FLIPPER_ACTION_ANGLE, GEAR_RATIO_FLIPPER)
        print(f"Robot: Flip Cube (Motor Angle: {angle})")
        if self.motor_flip:
            self.motor_flip.rotate_by_angle(angle, 360) 
            self.motor_flip.wait_for_movement()
            self.motor_flip.hold()

    def move_sensor_arm(self, target_arm_angle):
        # Assuming target_arm_angle is absolute physical angle (0, 30, 60...)
        motor_angle = self._get_motor_angle(target_arm_angle, GEAR_RATIO_SENSOR_ARM)
        print(f"Robot: Move Sensor Arm to {target_arm_angle} (Motor Pos: {motor_angle})")
        if self.motor_arm:
            self.motor_arm.rotate_to_angle(motor_angle, 200)
            self.motor_arm.wait_for_movement()
            self.motor_arm.hold()

    def cleanup(self):
        if self.motor_flip: self.motor_flip.close_motor()
        if self.motor_platform: self.motor_platform.close_motor()
        if self.motor_arm: self.motor_arm.close_motor()