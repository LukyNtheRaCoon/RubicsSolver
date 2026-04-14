# robot_arm_control.py

from brian.motors import Motor, MotorPort
from robot_config import (
    MOTOR_PORT_FLIP_CUBE,
    MOTOR_PORT_ROTATE_PLATFORM,
    MOTOR_PORT_SENSOR_ARM
)

class RobotArmControl:
    """
    Manages the physical motor movements for the Rubik's Cube robot
    based on the user-specified 3-motor configuration:
    1. Flipping the cube
    2. Rotating the cube platform
    3. Moving the color sensor arm
    """

    DEFAULT_SPEED = 360  # degrees per second, adjust as needed for physical robot
    FLIP_ANGLE = 180     # degrees for a cube flip
    PLATFORM_ROTATION_ANGLE_90 = 90 # degrees for a 90-degree platform rotation

    # Sensor arm positions would be very specific to the robot's mechanical design.
    # These are placeholders and need actual values based on calibration.
    # Example: positions to scan 3x3 stickers on a face.
    SENSOR_ARM_POSITION_1 = 0
    SENSOR_ARM_POSITION_2 = 30
    SENSOR_ARM_POSITION_3 = 60 # Hypothetical angles

    def __init__(self):
        """
        Initializes motor objects.
        """
        self.motor_flip_cube = None
        self.motor_rotate_platform = None
        self.motor_sensor_arm = None

        self._initialize_motors()

    def _initialize_motors(self):
        """
        Attempts to initialize motors connected to the defined ports.
        """
        try:
            self.motor_flip_cube = Motor(MOTOR_PORT_FLIP_CUBE)
            print(f"Motor Flip Cube initialized on port {MOTOR_PORT_FLIP_CUBE.name}")
        except Exception as e:
            print(f"Could not initialize Motor Flip Cube on port {MOTOR_PORT_FLIP_CUBE.name}: {e}")

        try:
            self.motor_rotate_platform = Motor(MOTOR_PORT_ROTATE_PLATFORM)
            print(f"Motor Rotate Platform initialized on port {MOTOR_PORT_ROTATE_PLATFORM.name}")
        except Exception as e:
            print(f"Could not initialize Motor Rotate Platform on port {MOTOR_PORT_ROTATE_PLATFORM.name}: {e}")

        try:
            self.motor_sensor_arm = Motor(MOTOR_PORT_SENSOR_ARM)
            print(f"Motor Sensor Arm initialized on port {MOTOR_PORT_SENSOR_ARM.name}")
        except Exception as e:
            print(f"Could not initialize Motor Sensor Arm on port {MOTOR_PORT_SENSOR_ARM.name}: {e}")

    def _wait_for_motor_readiness(self, motor: Motor, name: str):
        """
        Waits for a motor to become ready.
        """
        if motor and not motor.is_ready():
            print(f"Waiting for {name} motor to be ready...")
            if not motor.wait_until_ready(timeout_ms=5000): # 5 second timeout
                print(f"Warning: {name} motor not ready after timeout.")
                return False
        return True

    def flip_cube(self):
        """
        Flips the entire cube (e.g., 180 degrees around its X or Y axis).
        This would effectively change the 'Up' face to 'Down' and 'Front' to 'Back', etc.
        """
        print("Executing Cube Flip (180 degrees)")
        if self._wait_for_motor_readiness(self.motor_flip_cube, "Flip Cube"):
            self.motor_flip_cube.rotate_by_angle(self.FLIP_ANGLE, self.DEFAULT_SPEED)
            self.motor_flip_cube.wait_for_movement()

    def rotate_platform_clockwise(self):
        """
        Rotates the cube holding platform clockwise by 90 degrees.
        This effectively rotates the entire cube (similar to a 'Y' move in cubing notation).
        """
        print("Executing Platform Rotation Clockwise (90 degrees)")
        if self._wait_for_motor_readiness(self.motor_rotate_platform, "Rotate Platform"):
            self.motor_rotate_platform.rotate_by_angle(self.PLATFORM_ROTATION_ANGLE_90, self.DEFAULT_SPEED)
            self.motor_rotate_platform.wait_for_movement()

    def rotate_platform_counter_clockwise(self):
        """
        Rotates the cube holding platform counter-clockwise by 90 degrees.
        (Similar to a 'Y'' move).
        """
        print("Executing Platform Rotation Counter-Clockwise (90 degrees)")
        if self._wait_for_motor_readiness(self.motor_rotate_platform, "Rotate Platform"):
            self.motor_rotate_platform.rotate_by_angle(-self.PLATFORM_ROTATION_ANGLE_90, self.DEFAULT_SPEED)
            self.motor_rotate_platform.wait_for_movement()

    def rotate_platform_180(self):
        """
        Rotates the cube holding platform by 180 degrees.
        (Similar to a 'Y2' move).
        """
        print("Executing Platform Rotation 180 degrees")
        if self._wait_for_motor_readiness(self.motor_rotate_platform, "Rotate Platform"):
            self.motor_rotate_platform.rotate_by_angle(2 * self.PLATFORM_ROTATION_ANGLE_90, self.DEFAULT_SPEED)
            self.motor_rotate_platform.wait_for_movement()

    def move_sensor_arm_to_position(self, target_angle: int):
        """
        Moves the sensor arm to a specific absolute angle to position the sensors.
        The `target_angle` will depend on the physical calibration of the arm
        and where it needs to be to read specific stickers.
        """
        print(f"Moving sensor arm to angle: {target_angle} degrees")
        if self._wait_for_motor_readiness(self.motor_sensor_arm, "Sensor Arm"):
            # Using rotate_to_angle assuming the arm has a known zero position
            self.motor_sensor_arm.rotate_to_angle(target_angle, self.DEFAULT_SPEED)
            self.motor_sensor_arm.wait_for_movement()

    def cleanup(self):
        """
        Releases all motor resources.
        """
        print("Cleaning up motor resources.")
        if self.motor_flip_cube:
            self.motor_flip_cube.close_motor()
        if self.motor_rotate_platform:
            self.motor_rotate_platform.close_motor()
        if self.motor_sensor_arm:
            self.motor_sensor_arm.close_motor()


# Example Usage (for testing purposes, if run directly)
if __name__ == "__main__":
    # This block assumes you have actual motors connected as per robot_config.py
    # and a CircuitPython environment. Running this without actual hardware
    # will likely result in initialization errors.
    print("Initializing Robot Arm Control for testing...")
    robot_control = RobotArmControl()

    # Example movements
    # robot_control.flip_cube()
    # robot_control.rotate_platform_clockwise()
    # robot_control.move_sensor_arm_to_position(robot_control.SENSOR_ARM_POSITION_1)

    print("Testing complete (no actual moves executed in this example).")
    robot_control.cleanup()
