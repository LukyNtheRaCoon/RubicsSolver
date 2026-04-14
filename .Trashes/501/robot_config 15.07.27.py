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
BUTTON_PORT = SensorPort.S4

# --- Calibration / Mechanical Setup ---

# Gear Ratios
# Ratio = (Motor Degrees) / (Output Degrees)
GEAR_RATIO_PLATFORM = 3.0
GEAR_RATIO_FLIPPER = 1.0
GEAR_RATIO_SENSOR_ARM = 3.0

# Base Angles (Output/Physical degrees)
PLATFORM_TURN_90 = 90
PLATFORM_TURN_180 = 180

FLIPPER_FLIP_ANGLE = 225
FLIPPER_RESET_ANGLE = 0
FLIPPER_HOLD_ANGLE = 90

SENSOR_SCAN1_ANGLE = 175
SENSOR_SCAN2_ANGLE = 140

