from brian.motors import MotorPort
from brian.sensors import SensorPort

# --- Motor Configuration ---
MOTOR_PORT_FLIP_CUBE = MotorPort.B
MOTOR_PORT_ROTATE_PLATFORM = MotorPort.A
MOTOR_PORT_SENSOR_ARM = MotorPort.C

# --- Sensor Configuration ---
SENSOR_PORT_COLOR_1 = SensorPort.S1
SENSOR_PORT_COLOR_2 = SensorPort.S2
SENSOR_PORT_COLOR_3 = SensorPort.S3

# --- Calibration / Mechanical Setup ---

# Gear Ratios
# Ratio = (Motor Degrees) / (Output Degrees)
GEAR_RATIO_PLATFORM = 1.0
GEAR_RATIO_FLIPPER = 1.0
GEAR_RATIO_SENSOR_ARM = 1.0

# Base Angles (Output/Physical degrees)
PLATFORM_TURN_90 = 90
PLATFORM_TURN_180 = 180
FLIPPER_ACTION_ANGLE = 180

# --- Homing / Initialization Configuration ---
HOMING_SPEED_FLIP = 20      # Degrees per second
HOMING_SPEED_PLATFORM = 20
HOMING_SPEED_ARM = 20

# If true, the robot will try to move motors against a physical stop to find zero
# Be careful: This requires physical hard stops!
ENABLE_HOMING_ON_STARTUP = True
