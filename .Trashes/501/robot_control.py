import brian.motors as motors
import brian.sensors as sensors
import robot_config
import time

class RobotControl:
    def __init__(self):
        # Initialize motors and sensors with specific classes
        self.motor_flip = motors.EV3LargeMotor(robot_config.MOTOR_PORT_FLIP_CUBE)
        self.motor_platform = motors.EV3LargeMotor(robot_config.MOTOR_PORT_ROTATE_PLATFORM)
        self.motor_arm = motors.EV3LargeMotor(robot_config.MOTOR_PORT_SENSOR_ARM)
        self.motor_flip.wait_until_ready()
        self.motor_platform.wait_until_ready()
        self.motor_arm.wait_until_ready()
        self.button = sensors.EV3.TouchSensorEV3(robot_config.BUTTON_PORT)
        self.sensor_color_1 = sensors.EV3.ColorSensorEV3(robot_config.SENSOR_PORT_COLOR_1)
        self.sensor_color_2 = sensors.EV3.ColorSensorEV3(robot_config.SENSOR_PORT_COLOR_2)
        self.sensor_color_3 = sensors.EV3.ColorSensorEV3(robot_config.SENSOR_PORT_COLOR_3)
        self.sensor_color_1.set_mode(self.sensor_color_1.Mode(4)) # set RGB_RAW mode
        self.sensor_color_2.set_mode(self.sensor_color_2.Mode(4)) # set RGB_RAW mode
        self.sensor_color_3.set_mode(self.sensor_color_3.Mode(4)) # set RGB_RAW mode
        self.sensor_color_1.wait_until_ready() # wait until sensor is ready
        self.sensor_color_2.wait_until_ready() # wait until sensor is ready
        self.sensor_color_3.wait_until_ready() # wait until sensor is ready

        print("Set motors to home positions...")
        self.button.wait_until_ready()
        print("Confirm home positions by pressing button")
        self.button.wait_for_press()
        self.motor_flip.reset_angle()
        self.motor_platform.reset_angle()
        self.motor_arm.reset_angle()
        print("Home positions set.")

    def _get_motor_angle(self, target_angle, gear_ratio):
        """Calculates the required motor angle based on gear ratio."""
        return int(target_angle * gear_ratio)

    def rotate_platform_clockwise(self):
        angle = self._get_motor_angle(robot_config.PLATFORM_TURN_90, robot_config.GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CW (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()

    def rotate_platform_counter_clockwise(self):
        angle = self._get_motor_angle(robot_config.PLATFORM_TURN_90, robot_config.GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 90 CCW (Motor Angle: -{angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(-angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()
            
    def rotate_platform_180(self):
        angle = self._get_motor_angle(robot_config.PLATFORM_TURN_180, robot_config.GEAR_RATIO_PLATFORM)
        print(f"Robot: Rotate Platform 180 (Motor Angle: {angle})")
        if self.motor_platform:
            self.motor_platform.rotate_by_angle(angle, 360)
            self.motor_platform.wait_for_movement()
            self.motor_platform.hold()

    def flip_cube(self):
        print(f"Robot: Flip Cube")
        if self.motor_flip:
            self.motor_flip.rotate_to_angle(self._get_motor_angle(robot_config.FLIPPER_FLIP_ANGLE, robot_config.GEAR_RATIO_FLIPPER), 360) 
            self.motor_flip.wait_for_movement()
            self.motor_flip.rotate_to_angle(self._get_motor_angle(robot_config.FLIPPER_RESET_ANGLE, robot_config.GEAR_RATIO_FLIPPER), 360) 
            self.motor_flip.wait_for_movement()
            self.motor_flip.hold()

    def move_sensor_arm(self, target_arm_angle):
        motor_angle = self._get_motor_angle(target_arm_angle, robot_config.GEAR_RATIO_SENSOR_ARM)
        print(f"Robot: Move Sensor Arm to {target_arm_angle} (Motor Pos: {motor_angle})")
        if self.motor_arm:
            self.motor_arm.rotate_to_angle(motor_angle, 200)
            self.motor_arm.wait_for_movement()
            self.motor_arm.hold()

    def cleanup(self):
        if self.motor_flip: self.motor_flip.close_motor()
        if self.motor_platform: self.motor_platform.close_motor()
        if self.motor_arm: self.motor_arm.close_motor()
        if self.button: self.button.close_sensor()
        if self.sensor_color_1: self.sensor_color_1.close_sensor()
        if self.sensor_color_2: self.sensor_color_2.close_sensor()
        if self.sensor_color_3: self.sensor_color_3.close_sensor()