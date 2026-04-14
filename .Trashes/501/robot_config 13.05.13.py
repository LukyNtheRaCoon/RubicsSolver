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
# Example: If motor turns 360 deg and output turns 180 deg, ratio is 2.0.
# If you have a 1:1 drive, keep these as 1.0.
# If you have a 3:1 gear reduction (motor spins 3x for 1 output turn), set to 3.0.
GEAR_RATIO_PLATFORM = 1.0
GEAR_RATIO_FLIPPER = 1.0
GEAR_RATIO_SENSOR_ARM = 1.0

# Base Angles (Output/Physical degrees)
# These are the target angles for the *output* mechanism.
PLATFORM_TURN_90 = 90
PLATFORM_TURN_180 = 180
FLIPPER_ACTION_ANGLE = 180  # Degrees for a full flip